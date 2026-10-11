#!/usr/bin/env python3
"""
kwartet_lanes.py - draw a multi-category Blind Kwartet game as one lane per category.

Each move is a dot in the lane of the category it plays in, numbered in time order.
The written game ("Move 1: P1 asks P2 for A1, P2 answers "No"") goes to a second PNG,
in the same format as the moves PNG of kwartet_notebook.py.
Dot colour = who asks. Filled dot = YES (a card moves, the same player asks again).
Ring = NO (the turn passes). An amber line marks a move that switches category.

Usage:
    python3 kwartet_lanes.py                                   # ./post2/Figure_2_game.json -> ./post2/Figure_2.png
    python3 kwartet_lanes.py -i game.json -o lanes.png          # also writes lanes_moves.png
    python3 kwartet_lanes.py -i game.json --moves moves.png     # choose the moves PNG name
    python3 kwartet_lanes.py -i game.json --no-moves            # lanes only
    python3 kwartet_lanes.py -i game.json --no-check           # draw even if a check fails

Requires: Pillow  (pip install pillow)

JSON format (same moves as kwartet_notebook.py, plus categories):
{
  "categories": ["A", "B", "C"],
  "players":    ["P1", "P2", "P3"],
  "cards":      ["A1", ..., "A4", "B1", ..., "B4", "C1", ..., "C4"],      # 4 per category, in order
  "example_initial_deal_for_validation": {"P1": [...], "P2": [...], "P3": [...]},   # optional
  "moves": [
    {"asker": "P1", "respondent": "P2", "card": "A1", "answer": "NO"},
    ...
    {"kwartet": "P3", "category": "A"}                                    # optional, last
  ]
}

Checks (skip with --no-check): it is the asker's turn (YES keeps it, NO passes it to the
respondent); the asker never asks for a card they hold; the respondent could still hold the
card according to public knowledge, card by card; and, when an example deal is given, the
asker holds another card of the category and every answer agrees with that deal.
This is a sanity check of the example, not the full referee.
"""
import argparse
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = 800
BG = (251, 250, 246)
INK = (44, 44, 42)
MUTED = (110, 108, 100)
PCOL = [(127, 119, 221), (29, 158, 117), (216, 90, 48)]   # P1 purple, P2 teal, P3 coral
PDARK = [(60, 52, 137), (8, 80, 65), (113, 43, 19)]
LIT = (239, 159, 39)
LANE = [(244, 242, 235), (238, 236, 227)]
LINK = (190, 188, 178)
GREEN, GREEN_BG = (59, 109, 17), (234, 243, 222)

FONT_REGULAR = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf",
    "C:/Windows/Fonts/arial.ttf", "DejaVuSans.ttf", "Arial.ttf",
]
FONT_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/Library/Fonts/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf", "DejaVuSans-Bold.ttf", "Arial Bold.ttf",
]


def font(size, bold=False):
    for path in (FONT_BOLD if bold else FONT_REGULAR):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    sys.exit("No TrueType font found. Install DejaVu Sans or edit FONT_REGULAR/FONT_BOLD.")


class GameError(Exception):
    pass


def parse_answer(a):
    if isinstance(a, bool):
        return a
    if isinstance(a, str) and a.strip().upper() in ("YES", "Y", "TRUE"):
        return True
    if isinstance(a, str) and a.strip().upper() in ("NO", "N", "FALSE"):
        return False
    raise GameError("answer must be YES or NO, got %r" % (a,))


def index(value, labels, what):
    if isinstance(value, int) and not isinstance(value, bool) and 1 <= value <= len(labels):
        return value - 1
    if isinstance(value, str):
        if value in labels:
            return labels.index(value)
        if value.isdigit() and 1 <= int(value) <= len(labels):
            return int(value) - 1
    raise GameError("unknown %s: %r (expected one of %s)" % (what, value, labels))


def load(game, check):
    """Return (players, categories, events); events carry everything needed for drawing."""
    players = game.get("players", ["P1", "P2", "P3"])
    cats = game.get("categories", ["A", "B", "C"])
    cards = game.get("cards")
    if len(players) != 3:
        raise GameError("this figure needs exactly 3 players")
    if not cards or len(cards) != 4 * len(cats):
        raise GameError("cards must list 4 cards per category, in category order")
    if len(cats) > 4:
        raise GameError("at most 4 categories fit the figure")
    cat_of = {c: i // 4 for i, c in enumerate(cards)}
    moves = game.get("moves", [])
    if not moves:
        raise GameError("no moves in the game")

    owner = None                      # true owner per card, from the example deal (optional)
    deal = game.get("example_initial_deal_for_validation")
    if deal and check:
        owner = {}
        for p, held in deal.items():
            pi = index(p, players, "player")
            for c in held:
                if c not in cat_of:
                    raise GameError("the example deal names an unknown card: %r" % c)
                owner[c] = pi
        if sorted(owner) != sorted(cards) or any(
                sum(1 for v in owner.values() if v == p) != 4 for p in range(3)):
            raise GameError("the example deal must hand each player 4 of the %d cards" % len(cards))
    possible = {c: set(range(3)) for c in cards}      # public knowledge, card by card

    first = moves[0]
    if "asker" not in first:
        raise GameError("the first move must be an ask")
    turn = index(first["asker"], players, "asker")
    events = []
    for k, m in enumerate(moves, 1):
        where = "move %d" % k
        if "kwartet" in m:
            p = index(m["kwartet"], players, "player")
            if "category" not in m:
                raise GameError("%s: give the category of the kwartet" % where)
            cat = index(m["category"], cats, "category")
            if check:
                if p != turn:
                    raise GameError("%s: %s announces a kwartet, but it is %s's turn" %
                                    (where, players[p], players[turn]))
                if owner is not None:
                    mine = [c for c in cards if cat_of[c] == cat and owner[c] == p]
                    if len(mine) != 4:
                        raise GameError("%s: %s does not hold all four %s cards" %
                                        (where, players[p], cats[cat]))
            events.append(dict(k=k, kind="kwartet", who=p, cat=cat))
            continue                  # the player keeps the turn after a kwartet
        x = index(m.get("asker"), players, "asker")
        y = index(m.get("respondent"), players, "respondent")
        if m.get("card") not in cat_of:
            raise GameError("%s: unknown card %r" % (where, m.get("card")))
        c = m["card"]
        yes = parse_answer(m.get("answer"))
        if x == y:
            raise GameError("%s: a player cannot ask themselves" % where)
        if check:
            if x != turn:
                raise GameError("%s: %s asks, but it is %s's turn" % (where, players[x], players[turn]))
            if owner is not None:
                if owner[c] == x:
                    raise GameError("%s: %s asks for %s, which they hold" % (where, players[x], c))
                if not any(owner[o] == x and cat_of[o] == cat_of[c] for o in cards if o != c):
                    raise GameError("%s: %s holds no other %s card, so cannot ask" %
                                    (where, players[x], cats[cat_of[c]]))
            possible[c].discard(x)
            if y not in possible[c]:
                raise GameError("%s: %s is already known not to hold %s" % (where, players[y], c))
            if owner is not None and (owner[c] == y) != yes:
                raise GameError("%s: the answer contradicts the example deal" % where)
            if yes:
                possible[c] = {x}
                if owner is not None:
                    owner[c] = x
            else:
                possible[c].discard(y)
        turn = x if yes else y
        events.append(dict(k=k, kind="ask", asker=x, resp=y, card=c, yes=yes, cat=cat_of[c]))
    return players, cats, events


# --------------------------------------------------------------- move wording
# Same wording and layout as the moves PNG of kwartet_notebook.py (Figure 1).
# A line is a list of (text, style) segments; style: "bold", "plain" or "p0".."p2"
# (a player's name, in that player's colour).
def move_segments(e, players):
    segs = [("Move %d: " % e["k"], "bold")]
    if e["kind"] == "ask":
        segs += [(players[e["asker"]], "p%d" % e["asker"]), (" asks ", "plain"),
                 (players[e["resp"]], "p%d" % e["resp"]), (" for %s, " % e["card"], "plain"),
                 (players[e["resp"]], "p%d" % e["resp"]),
                 (" answers \u201c%s\u201d" % ("Yes" if e["yes"] else "No"), "plain")]
    else:
        segs += [(players[e["who"]], "p%d" % e["who"]), (" announces Kwartet %s" % e["cat_name"], "plain")]
    return segs


def draw_segments(d, x, y, segs, size, scale=1):
    for text, style in segs:
        if style == "bold":
            f, col = font(size * scale, True), INK
        elif style[0] == "p" and style[1:].isdigit():
            f, col = font(size * scale, True), PDARK[int(style[1:])]
        else:
            f, col = font(size * scale), INK
        d.text((x, y), text, font=f, fill=col)
        x += d.textlength(text, font=f)
    return x


def moves_png(title, lines, path, scale=2):
    """A plain-text record of the whole game: one line per move."""
    S, row = scale, 38
    im = Image.new("RGB", (800 * S, (96 + row * len(lines) + 34) * S), BG)
    d = ImageDraw.Draw(im)
    d.text((40 * S, 28 * S), title, font=font(22 * S, True), fill=INK)
    d.line((40 * S, 68 * S, 760 * S, 68 * S), fill=(214, 212, 202), width=S)
    for i, segs in enumerate(lines):
        draw_segments(d, 40 * S, (88 + i * row) * S, segs, 20, S)
    im.save(path)


def draw(players, cats, events, scale=2):
    """The lanes: one dot per move, numbered; the written game is the moves PNG."""
    S = scale
    n = len(events)
    left, right = 150, 745
    step = min(90.0, (right - left) / max(n - 1, 1))
    xs = [left + i * step for i in range(n)]
    top, lane_h, gap = 64, 82, 4
    ys = [top + i * (lane_h + gap) + lane_h / 2 for i in range(len(cats))]
    ly = top + len(cats) * (lane_h + gap) + 12
    ly2 = ly + 26
    im = Image.new("RGB", (W * S, int(ly2 + 30) * S), BG)
    d = ImageDraw.Draw(im)

    d.text((36 * S, 24 * S), "The game, move by move, in the category each move plays in",
           font=font(18 * S, True), fill=INK)
    for i, name in enumerate(cats):
        y0 = top + i * (lane_h + gap)
        d.rounded_rectangle((36 * S, y0 * S, 770 * S, (y0 + lane_h) * S), 10 * S, fill=LANE[i % 2])
        d.text((74 * S, (y0 + 24) * S), "Category", font=font(12 * S), fill=MUTED, anchor="mm")
        d.text((74 * S, (y0 + 52) * S), name, font=font(28 * S, True), fill=INK, anchor="mm")

    # links between consecutive moves; amber when the category changes
    for i in range(n - 1):
        a, b = events[i], events[i + 1]
        switch = a["cat"] != b["cat"]
        d.line((xs[i] * S, ys[a["cat"]] * S, xs[i + 1] * S, ys[b["cat"]] * S),
               fill=LIT if switch else LINK, width=(4 if switch else 2) * S)

    # the dots
    r = max(10, min(17, step / 2 - 3))
    nf = 16 if r >= 16 else 13
    for e, x in zip(events, xs):
        cy = ys[e["cat"]]
        box = ((x - r) * S, (cy - r) * S, (x + r) * S, (cy + r) * S)
        if e["kind"] == "kwartet":
            d.rounded_rectangle(box, 7 * S, fill=GREEN_BG, outline=GREEN, width=3 * S)
            d.text((x * S, cy * S), "K", font=font(nf * S, True), fill=(39, 80, 10), anchor="mm")
        elif e["yes"]:
            d.ellipse(box, fill=PCOL[e["asker"]])
            d.text((x * S, cy * S), str(e["k"]), font=font(nf * S, True), fill=(255, 255, 255), anchor="mm")
        else:
            d.ellipse(box, fill=BG, outline=PCOL[e["asker"]], width=3 * S)
            d.text((x * S, cy * S), str(e["k"]), font=font(nf * S, True),
                   fill=PDARK[e["asker"]], anchor="mm")

    # legend
    d.ellipse((38 * S, (ly - 8) * S, 54 * S, (ly + 8) * S), fill=PCOL[1])
    d.text((62 * S, ly * S), "YES: the card moves and the same player asks again", font=font(13 * S),
           fill=INK, anchor="lm")
    c2 = 430
    d.ellipse((c2 * S, (ly - 8) * S, (c2 + 16) * S, (ly + 8) * S), fill=BG, outline=PCOL[1], width=3 * S)
    d.text(((c2 + 24) * S, ly * S), "NO: the turn passes to the respondent", font=font(13 * S),
           fill=INK, anchor="lm")
    d.line((38 * S, ly2 * S, 54 * S, ly2 * S), fill=LIT, width=4 * S)
    d.text((62 * S, ly2 * S), "the player switches category", font=font(13 * S), fill=INK, anchor="lm")
    d.text((c2 * S, ly2 * S), "colour = who asks:", font=font(13 * S), fill=INK, anchor="lm")
    x = c2 + d.textlength("colour = who asks: ", font=font(13 * S)) / S
    for p in range(3):
        d.text((x * S, ly2 * S), players[p], font=font(13 * S, True), fill=PDARK[p], anchor="lm")
        x += d.textlength(players[p] + "  ", font=font(13 * S, True)) / S
    return im


def main():
    ap = argparse.ArgumentParser(description="Draw a multi-category Blind Kwartet game as category lanes.")
    ap.add_argument("game", nargs="?", help="game JSON file (same as -i; wins if both are given)")
    ap.add_argument("-i", "--input", default="./post2/Figure_2_game.json",
                    help="game JSON file (default ./post2/Figure_2_game.json)")
    ap.add_argument("-o", "--output", default="./post2/Figure_2.png",
                    help="output PNG (default ./post2/Figure_2.png)")
    ap.add_argument("--moves", help="path of the moves PNG (default: <output>_moves.png)")
    ap.add_argument("--no-moves", action="store_true", help="do not write the moves PNG")
    ap.add_argument("--scale", type=int, default=2, help="pixel scale, 2 gives 1600 px wide (default 2)")
    ap.add_argument("--no-check", action="store_true", help="skip the legality checks")
    a = ap.parse_args()

    src = a.game or a.input
    try:
        with open(src, encoding="utf-8") as f:
            game = json.load(f)
    except OSError as e:
        sys.exit("error: cannot read the game file %s: %s" % (src, e.strerror or e))
    except json.JSONDecodeError as e:
        sys.exit("error: %s is not valid JSON: %s" % (src, e))
    try:
        players, cats, events = load(game, not a.no_check)
    except GameError as e:
        sys.exit("error: %s" % e)

    folder = os.path.dirname(a.output)
    if folder:
        os.makedirs(folder, exist_ok=True)
    draw(players, cats, events, a.scale).save(a.output)
    print("wrote %s (%d moves)" % (a.output, len(events)))

    if not a.no_moves:
        for e in events:
            e["cat_name"] = cats[e["cat"]]
        if len(cats) == 1:
            title = "Category %s: the game" % cats[0]
        else:
            title = "Categories %s and %s: the game" % (", ".join(cats[:-1]), cats[-1])
        stem = a.output[:-4] if a.output.lower().endswith(".png") else a.output
        path = a.moves or stem + "_moves.png"
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        moves_png(title, [move_segments(e, players) for e in events], path, a.scale)
        print("wrote %s" % path)


if __name__ == "__main__":
    main()
