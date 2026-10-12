from __future__ import annotations

import argparse
import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from tools import sync_medium


def test_output_paths_are_beside_source(tmp_path: Path):
    paths = sync_medium.output_paths(tmp_path / "article.md", "20260101_010203")
    assert paths["reconciled"] == tmp_path / "article_reconciled_20260101_010203.md"
    assert paths["report"] == tmp_path / "medium_sync_report_20260101_010203.txt"


def test_extractor_removes_page_chrome_and_image_urls():
    html = """
    <html><head><title>Noise</title></head><body>
    <nav>Home Recommendations</nav><article>
      <h1>Title</h1><h2>Subtitle</h2><p>Visible paragraph.</p>
      <figure><img src="https://miro.medium.com/image.png"><figcaption>Caption</figcaption></figure>
      <blockquote>A quote.</blockquote>
    </article><footer>Claps Author bio</footer></body></html>
    """
    extracted = sync_medium.extract_medium_article(html)
    formatted = sync_medium.format_extracted(extracted)
    assert "Home" not in formatted and "Claps" not in formatted
    assert "Visible paragraph." in formatted and "Caption" in formatted
    assert "miro.medium.com" not in formatted


def test_protected_equation_and_image_are_not_lost():
    local = "<!-- metadata -->\n![fig](local.png)\n\n$$x^2$$\n"
    sync_medium.validate_reconciled_markdown(local, local + "Changed prose\n")
    with pytest.raises(sync_medium.SyncError):
        sync_medium.validate_reconciled_markdown(local, "Changed prose\n")


def test_reconcile_uses_structured_responses_and_accepts_clear_wording_change():
    local = "# Heading\n\nOriginal wording.\n"
    response = Mock(output_text=json.dumps({
        "reconciled_markdown": "# Heading\n\nEdited wording.\n",
        "change_report": "Changed one paragraph.",
        "ambiguities": [],
    }))
    client = Mock()
    client.responses.create.return_value = response
    with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}), patch(
        "openai.OpenAI", return_value=client
    ):
        result = sync_medium.reconcile(local, {"title": "Heading", "blocks": []}, "test-model")
    assert result["reconciled_markdown"].endswith("Edited wording.\n")
    assert client.responses.create.call_args.kwargs["model"] == "test-model"


def test_ambiguous_changes_are_reported_and_not_applied():
    local = "# Heading\n\nOriginal wording.\n"
    response = Mock(output_text=json.dumps({
        "reconciled_markdown": local,
        "change_report": "No clear changes applied.",
        "ambiguities": ["The second paragraph could not be matched confidently."],
    }))
    client = Mock()
    client.responses.create.return_value = response
    with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}), patch(
        "openai.OpenAI", return_value=client
    ):
        result = sync_medium.reconcile(local, {}, "test-model")
    assert result["reconciled_markdown"] == local
    assert result["ambiguities"]


def test_missing_api_key_and_malformed_url_are_clear():
    with patch.dict("os.environ", {}, clear=True), pytest.raises(sync_medium.SyncError, match="OPENAI_API_KEY"):
        sync_medium.reconcile("text", {}, "test-model")
    with pytest.raises(sync_medium.SyncError, match="medium.com"):
        sync_medium.validate_medium_url("not-a-url")


def test_run_never_modifies_source_and_dry_run_writes_nothing(tmp_path: Path):
    article = tmp_path / "article.md"
    original = "# Heading\n\nOriginal.\n"
    article.write_text(original, encoding="utf-8")
    args = argparse.Namespace(article=str(article), url="https://medium.com/@x/y", model="m", dry_run=True, keep_extracted=True, verbose=False)
    result = {"reconciled_markdown": "# Heading\n\nEdited.\n", "change_report": "Edited.", "ambiguities": []}
    with patch.object(sync_medium, "fetch_medium_html", return_value="<article><h1>Heading</h1><p>Edited.</p></article>"), patch.object(sync_medium, "extract_medium_article", return_value={"title": "Heading", "blocks": []}), patch.object(sync_medium, "reconcile", return_value=result):
        assert sync_medium.run(args) == 0
    assert article.read_text(encoding="utf-8") == original
    assert list(tmp_path.iterdir()) == [article]
