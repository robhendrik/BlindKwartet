#!/usr/bin/env python3
"""Reviewable, conservative reconciliation of local Markdown with Medium."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

DEFAULT_MODEL = "gpt-5-mini"
USER_AGENT = "medium-markdown-sync/1.0 (+https://platform.openai.com/)"

SYSTEM_INSTRUCTIONS = r"""
You reconcile a canonical local Markdown article with the visible text of its
published Medium version. Return JSON matching the requested schema.

The local Markdown is the canonical structural source. Import ONLY genuine,
clear editorial wording changes visible in Medium. Preserve local image paths,
Markdown image syntax, figure numbering and metadata, alt/source metadata
unless visibly changed, display math and LaTeX source, footnotes, HTML
comments, metadata and publication blocks, local paths, references/URLs unless
their visible text clearly changed, Unicode, Markdown conventions, and section
structure. Do not replace images with Medium CDN URLs, equations with rendered
text or images, normalize prose, invent content, remove local metadata, change
citation numbering, or silently resolve ambiguity.

If Medium differs only because of HTML rendering or formatting, keep local
Markdown unchanged. If matching is uncertain or a difference is ambiguous,
leave that Markdown unchanged and explain it in ambiguities. Apply a change
only when it is clearly a wording change to the matching Markdown block.

The response must contain the complete reconciled Markdown, a concise change
report, and every ambiguity or skipped difference. Never include commentary
outside those JSON fields.
""".strip()

SCHEMA = {
    "type": "object",
    "properties": {
        "reconciled_markdown": {"type": "string"},
        "change_report": {"type": "string"},
        "ambiguities": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["reconciled_markdown", "change_report", "ambiguities"],
    "additionalProperties": False,
}


class SyncError(RuntimeError):
    """A user-facing, expected failure."""


def validate_medium_url(url: str) -> None:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower().rstrip(".")
    if parsed.scheme not in {"http", "https"} or not host or not (
        host == "medium.com" or host.endswith(".medium.com")
    ):
        raise SyncError("The Medium URL must be an http(s) URL on medium.com.")


def fetch_medium_html(url: str, requests_module: Any = None) -> str:
    validate_medium_url(url)
    if requests_module is None:
        try:
            import requests as requests_module
        except ImportError as exc:
            raise SyncError("Missing dependency: install requests.") from exc
    try:
        response = requests_module.get(
            url, headers={"User-Agent": USER_AGENT}, timeout=30
        )
        response.raise_for_status()
    except Exception as exc:
        raise SyncError(f"Could not fetch Medium article: {exc}") from exc
    return response.text


def _json_ld_title(soup: Any) -> str:
    for node in soup.select('script[type="application/ld+json"]'):
        try:
            data = json.loads(node.string or node.get_text())
        except (TypeError, json.JSONDecodeError):
            continue
        items = data if isinstance(data, list) else [data]
        for item in items:
            if isinstance(item, dict) and item.get("headline"):
                return str(item["headline"]).strip()
    return ""


def extract_medium_article(html: str) -> dict[str, Any]:
    """Extract visible article blocks, deliberately excluding image URLs."""
    try:
        from bs4 import BeautifulSoup
    except ImportError as exc:
        raise SyncError("Missing dependency: install beautifulsoup4.") from exc

    soup = BeautifulSoup(html, "html.parser")
    for node in soup.select(
        "nav, header, footer, aside, form, script, style, noscript, "
        '[role="navigation"], [aria-label*="comment" i], [data-testid*="recommend" i]'
    ):
        node.decompose()
    title = ""
    title_node = soup.select_one("article h1, main h1, h1")
    if title_node:
        title = title_node.get_text(" ", strip=True)
    title = title or _json_ld_title(soup)
    subtitle_node = soup.select_one("article h2, main h2, [data-testid='subtitle']")
    subtitle = subtitle_node.get_text(" ", strip=True) if subtitle_node else ""

    root = soup.select_one("article") or soup.select_one("main") or soup.body
    if root is None:
        raise SyncError("Medium page has no readable article body.")
    blocks: list[dict[str, str]] = []
    seen: set[int] = set()
    for node in root.select("h1, h2, h3, h4, h5, h6, p, blockquote, figcaption"):
        if node is title_node or node is subtitle_node:
            continue
        # Avoid duplicate nested nodes and empty chrome remnants.
        if any(id(parent) in seen for parent in node.parents):
            continue
        text = node.get_text(" ", strip=True)
        if text:
            blocks.append({"type": node.name, "text": text})
            seen.add(id(node))
    if not blocks and not title:
        raise SyncError("Could not extract visible Medium article content.")
    return {"title": title, "subtitle": subtitle, "blocks": blocks}


def format_extracted(extracted: dict[str, Any]) -> str:
    lines = []
    if extracted.get("title"):
        lines.append(f"TITLE: {extracted['title']}")
    if extracted.get("subtitle"):
        lines.append(f"SUBTITLE: {extracted['subtitle']}")
    lines.append("CONTENT:")
    for block in extracted.get("blocks", []):
        lines.append(f"[{block['type']}] {block['text']}")
    return "\n".join(lines).rstrip() + "\n"


def _protected_fragments(markdown: str) -> list[str]:
    fragments: list[str] = []
    lines = markdown.splitlines()
    in_comment = False
    in_fence = False
    fenced: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("<!--"):
            in_comment = True
        if stripped.startswith("```"):
            in_fence = not in_fence
            fenced.append(line)
            if not in_fence:
                fragments.append("\n".join(fenced))
                fenced = []
            continue
        if in_fence:
            fenced.append(line)
        if in_comment or stripped.startswith("![") or re.match(r"^\[\^[^]]+\]:", stripped):
            fragments.append(line)
        if stripped.endswith("-->"):
            in_comment = False
    if fenced:
        fragments.append("\n".join(fenced))
    for match in re.findall(r"(?s)(\$\$.*?\$\$|\\\[.*?\\\])", markdown):
        fragments.append(match)
    return fragments


def validate_reconciled_markdown(local: str, reconciled: str) -> None:
    if not reconciled.strip():
        raise SyncError("The model returned empty reconciled Markdown.")
    for fragment in _protected_fragments(local):
        if fragment not in reconciled:
            raise SyncError(
                "Model output failed safety validation: a protected local Markdown "
                "fragment was changed or removed. No output was written."
            )
    if re.search(r"https?://(?:[^\s/]+\.)?(?:mediumcdn|cdn-images-1\.medium|miro\.medium)\.com", reconciled, re.I):
        raise SyncError(
            "Model output failed safety validation: it contains a Medium CDN image URL."
        )


def reconcile(local_markdown: str, extracted: dict[str, Any], model: str) -> dict[str, Any]:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise SyncError("Missing dependency: install openai.") from exc
    if not os.environ.get("OPENAI_API_KEY"):
        raise SyncError("OPENAI_API_KEY is not set; refusing to call the OpenAI API.")
    client = OpenAI()
    user_input = (
        "LOCAL MARKDOWN (canonical):\n---\n"
        + local_markdown
        + "\n---\nEXTRACTED MEDIUM ARTICLE:\n---\n"
        + format_extracted(extracted)
        + "---\n"
    )
    try:
        response = client.responses.create(
            model=model,
            instructions=SYSTEM_INSTRUCTIONS,
            input=user_input,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "medium_reconciliation",
                    "schema": SCHEMA,
                    "strict": True,
                }
            },
        )
        raw = response.output_text
        result = json.loads(raw)
    except Exception as exc:
        raise SyncError(f"OpenAI reconciliation failed: {exc}") from exc
    if not isinstance(result, dict):
        raise SyncError("OpenAI returned an invalid reconciliation object.")
    validate_reconciled_markdown(local_markdown, result.get("reconciled_markdown", ""))
    result.setdefault("change_report", "")
    result.setdefault("ambiguities", [])
    return result


def output_paths(article: Path, timestamp: str | None = None) -> dict[str, Path]:
    stamp = timestamp or dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = ""
    counter = 0
    while True:
        candidates = {
            "reconciled": article.with_name(f"{article.stem}_reconciled_{stamp}{suffix}.md"),
            "report": article.with_name(f"medium_sync_report_{stamp}{suffix}.txt"),
            "extracted": article.with_name(f"medium_extracted_{stamp}{suffix}.txt"),
        }
        if not any(path.exists() for path in candidates.values()):
            return candidates
        counter += 1
        suffix = f"_{counter}"


def run(args: argparse.Namespace) -> int:
    article = Path(args.article).expanduser()
    if not article.is_file():
        raise SyncError(f"Local Markdown file does not exist: {article}")
    local = article.read_text(encoding="utf-8")
    extracted = extract_medium_article(fetch_medium_html(args.url))
    result = reconcile(local, extracted, args.model)
    paths = output_paths(article)
    if args.keep_extracted and not args.dry_run:
        paths["extracted"].write_text(format_extracted(extracted), encoding="utf-8")
    if not args.dry_run:
        ambiguities = result.get("ambiguities", [])
        report = "Change report\n==============\n" + str(result.get("change_report", "")).strip()
        report += "\n\nAmbiguities / skipped differences\n=================================\n"
        report += "\n".join(f"- {item}" for item in ambiguities) or "None reported."
        paths["reconciled"].write_text(result["reconciled_markdown"], encoding="utf-8")
        paths["report"].write_text(report.rstrip() + "\n", encoding="utf-8")
    print("Reconciliation complete." if not args.dry_run else "Dry run complete; no output files written.")
    print(f"Original left untouched:\n  {article}")
    print(f"Intended reconciled version:\n  {paths['reconciled']}")
    print(f"Intended report:\n  {paths['report']}")
    if args.keep_extracted:
        print(f"Extracted Medium content:\n  {paths['extracted']}")
    print(f'\nReview with:\n  git diff --no-index "{article}" "{paths["reconciled"]}"')
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("article", help="path to the local article.md")
    parser.add_argument("url", help="public Medium article URL")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--keep-extracted", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        return run(build_parser().parse_args(argv))
    except SyncError as exc:
        print(f"sync_medium: error: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"sync_medium: error writing output: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
