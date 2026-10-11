#!/usr/bin/env python3
"""
kwartet_notebook.py - animate a single-category Blind Kwartet game as a notebook.

Usage:
    python3 kwartet_notebook.py                              # ./post2/Figure_1_game.json -> ./post2/Figure_1.gif
    python3 kwartet_notebook.py -i game.json -o game.gif     # also writes game_moves.png
    python3 kwartet_notebook.py game.json -o game.gif        # the game file may also be positional
    python3 kwartet_notebook.py game.json -o game.gif --moves moves.png   # choose the PNG name
    python3 kwartet_notebook.py game.json -o game.gif --no-moves          # GIF only
    python3 kwartet_notebook.py game.json -o game.gif --sheet frames.png --scale 0.75
    python3 kwartet_notebook.py game.json -o game.gif --no-check     # draw even if a move is illegal

Requires: Pillow  (pip install pillow)

JSON format (players and cards may be given by label or by 1-based number):
{
  "category": "A",                       # optional, default "A"
  "players": ["P1", "P2", "P3"],         # optional, exactly 3
  "cards":   ["A1", "A2", "A3", "A4"],   # optional, exactly 4
  "first_player": "P1",                  # optional, default: asker of the first move
  "title":  "Category A: what the notebook knows",   # optional
  "banner": "The notebook never held a deal: ...",   # optional, "" hides it
  "moves": [
    {"asker": "P1", "respondent": "P2", "card": "A1", "answer": "NO"},
    {"asker": "P2", "respondent": "P3", "card": "A1", "answer": "YES"},
    {"kwartet": "P3"}                    # optional last move
  ]
}

Model: the 81 worlds are the ways the 4 cards can currently be spread over 3 players.
Rules checked for an ask X -> Y for card c:
  * it must be X's turn (YES keeps the turn, NO passes it to Y);
  * X holds at least one OTHER card of the category, and not c;
  * Y could still hold c (otherwise X already knows the answer, so the ask is illegal);
  * the answer must leave at least one world.
A kwartet by P needs a world in which P holds all four cards.
"""
import argparse
import itertools
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 800, 500
BG = (251, 250, 246)
INK = (44, 44, 42)
MUTED = (110, 108, 100)
PCOL = [(127, 119, 221), (29, 158, 117), (216, 90, 48)]   # purple, teal, coral
PTINT = [(238, 237, 254), (225, 245, 238), (250, 236, 231)]
PDARK = [(60, 52, 137), (8, 80, 65), (113, 43, 19)]
LIT = (239, 159, 39)
UNLIT = (232, 230, 220)
DEFAULT_BANNER = "The notebook never held a deal: it only shrank as things were said."

FONT_REGULAR = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "DejaVuSans.ttf", "Arial.ttf",
]
FONT_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "DejaVuSans-Bold.ttf", "Arial Bold.ttf",
]


def font(size, bold=False):
    for path in (FONT_BOLD if bold else FONT_REGULAR):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    sys.exit("No TrueType font found. Install DejaVu Sans or edit FONT_REGULAR/FONT_BOLD.")


# ---------------------------------------------------------------- game model
class GameError(Exception):
    pass


def lookup(value, labels, what):
    """Accept a label ("P2") or a 1-based number (2)."""
    if isinstance(value, int) and not isinstance(value, bool):
        if 1 <= value <= len(labels):
            return value - 1
    elif isinstance(value, str):
        if value in labels:
            return labels.index(value)
        if value.isdigit() and 1 <= int(value) <= len(labels):
            return int(value) - 1
    raise GameError("unknown %s: %r (expected one of %s)" % (what, value, labels))


def parse_answer(a):
    if isinstance(a, bool):
        return a
    if isinstance(a, str) and a.strip().upper() in ("YES", "Y", "TRUE"):
        return True
    if isinstance(a, str) and a.strip().upper() in ("NO", "N", "FALSE"):
        return False
    raise GameError("answer must be YES or NO, got %r" % (a,))


def initial_worlds():
    # (index, current owner of each card); the index keeps a world's square fixed in the grid
    return list(enumerate(itertools.product(range(3), repeat=4)))


def apply_ask(worlds, x, y, c, yes, check=True, where=""):
    ok = [(i, w) for i, w in worlds
          if w[c] != x and any(w[k] == x for k in range(4) if k != c)]
    if check and not any(w[c] == y for _, w in ok):
        raise GameError("%s: illegal ask: the asker either has no other card of the category, "
                        "holds the card, or already knows the respondent does not have it" % where)
    if yes:
        out = []
        for i, w in ok:
            if w[c] == y:
                w2 = list(w)
                w2[c] = x
                out.append((i, tuple(w2)))
    else:
        out = [(i, w) for i, w in ok if w[c] != y]
    if check and not out:
        raise GameError("%s: this answer is impossible: no world is left" % where)
    return out


def apply_kwartet(worlds, p, check=True, where=""):
    out = [(i, w) for i, w in worlds if all(o == p for o in w)]
    if check and not out:
        raise GameError("%s: kwartet is impossible: no world has that player holding all four cards" % where)
    return out


def possible_owners(worlds):
    return [set(w[c] for _, w in worlds) for c in range(4)]


# --------------------------------------------------------------- move wording
# One place writes the move text, so the GIF header and the moves PNG always agree.
# A line is a list of (text, style) segments; style: "bold", "plain", "muted" or "p0".."p2"
# (a player's name, in that player's colour).
def ask_segments(k, players, cards, x, y, c, yes=None):
    segs = [("Move %d: " % k, "bold"), (players[x], "p%d" % x), (" asks ", "plain"),
            (players[y], "p%d" % y), (" for %s" % cards[c], "plain")]
    if yes is not None:
        segs += [(", ", "plain"), (players[y], "p%d" % y),
                 (" answers “%s”" % ("Yes" if yes else "No"), "plain")]
    return segs


def kwartet_segments(k, players, p):
    return [("Move %d: " % k, "bold"), (players[p], "p%d" % p), (" announces Kwartet", "plain")]


def draw_segments(d, x, y, segs, size, scale=1):
    """Draw one line of styled segments starting at (x, y); returns the end x."""
    for text, style in segs:
        if style == "bold":
            f, col = font(size * scale, True), INK
        elif style == "muted":
            f, col = font(size * scale), MUTED
        elif style[0] == "p" and style[1:].isdigit():
            f, col = font(size * scale, True), PDARK[int(style[1:])]
        else:
            f, col = font(size * scale), INK
        d.text((x, y), text, font=f, fill=col)
        x += d.textlength(text, font=f)
    return x


def wrap(d, text, f, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if cur and d.textlength(trial, font=f) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def moves_png(title, move_lines, path, scale=2):
    """A plain-text record of the whole game: one line per move."""
    S = scale
    row = 38
    w, h = 800 * S, (96 + row * len(move_lines) + 34) * S
    im = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(im)
    d.text((40 * S, 28 * S), title.split(":")[0] + ": the game", font=font(22 * S, True), fill=INK)
    d.line((40 * S, 68 * S, 760 * S, 68 * S), fill=(214, 212, 202), width=S)
    for i, segs in enumerate(move_lines):
        draw_segments(d, 40 * S, (88 + i * row) * S, segs, 20, S)
    im.save(path)


# ------------------------------------------------------------------- drawing
def draw_frame(worlds, turn, players, cards, title, move_segs, explain, learned=None,
               highlight=None, banner=None):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.text((40, 28), title, font=font(22, True), fill=INK)
    draw_segments(d, 40, 60, move_segs, 18)

    tx, ty, cw, ch = 130, 120, 100, 66
    for c in range(4):
        d.text((tx + c * cw + cw // 2, ty - 20), cards[c], font=font(18, True), fill=INK, anchor="mm")
    poss = possible_owners(worlds)
    for p in range(3):
        y = ty + p * ch
        if turn == p:
            d.polygon([(40, y + 20), (40, y + 46), (58, y + 33)], fill=INK)
        d.rounded_rectangle((66, y + 10, 112, y + 56), 8, fill=PCOL[p])
        d.text((89, y + 33), players[p], font=font(17, True), fill=(255, 255, 255), anchor="mm")
        for c in range(4):
            x = tx + c * cw
            box = (x + 5, y + 5, x + cw - 5, y + ch - 5)
            mid = ((box[0] + box[2]) // 2, (box[1] + box[3]) // 2)
            if p in poss[c]:
                if len(poss[c]) == 1:
                    d.rounded_rectangle(box, 8, fill=PCOL[p])
                    d.text(mid, "holds", font=font(17, True), fill=(255, 255, 255), anchor="mm")
                else:
                    d.rounded_rectangle(box, 8, fill=PTINT[p], outline=PCOL[p], width=2)
                    d.text(mid, "?", font=font(22, True), fill=PDARK[p], anchor="mm")
            else:
                d.rounded_rectangle(box, 8, fill=(240, 238, 230))
                d.text(mid, "x", font=font(20), fill=(176, 174, 164), anchor="mm")
    if highlight is not None:
        p, c = highlight
        x, y = tx + c * cw, ty + p * ch
        d.rounded_rectangle((x + 1, y + 1, x + cw - 1, y + ch - 1), 10, outline=INK, width=4)

    ly = ty + 3 * ch + 18
    d.polygon([(40, ly), (40, ly + 12), (50, ly + 6)], fill=MUTED)
    d.text((58, ly - 3), "= to move", font=font(14), fill=MUTED)

    # the 81 worlds: one fixed square each, lit while the world survives
    gx, gy, s = 540, 125, 24
    alive = set(i for i, _ in worlds)
    for i in range(81):
        r, col = divmod(i, 9)
        x, y = gx + col * s, gy + r * s
        d.rectangle((x, y, x + s - 3, y + s - 3), fill=LIT if i in alive else UNLIT)
    d.text((gx, gy - 28), "Worlds still possible", font=font(16, True), fill=INK)
    d.text((gx, gy + 9 * s + 4), "%d of 81" % len(alive), font=font(20, True), fill=INK)

    ey = 366
    for line in wrap(d, explain, font(20), 720):
        d.text((40, ey), line, font=font(20), fill=INK)
        ey += 28
    if learned:
        d.text((40, ey + 6), learned, font=font(18, True), fill=INK)
    if banner:
        d.rounded_rectangle((40, 452, 760, 488), 8, fill=(234, 243, 222), outline=(59, 109, 17), width=2)
        d.text((400, 470), banner, font=font(16, True), fill=(39, 80, 10), anchor="mm")
    return im


# ---------------------------------------------------------------------- main
def build(game, check, ms):
    players = game.get("players", ["P1", "P2", "P3"])
    cards = game.get("cards", ["A1", "A2", "A3", "A4"])
    if len(players) != 3 or len(cards) != 4:
        raise GameError("this model needs exactly 3 players and 4 cards")
    category = game.get("category", "A")
    title = game.get("title", "Category %s: what the notebook knows" % category)
    banner = game.get("banner", DEFAULT_BANNER)
    moves = game.get("moves", [])
    if not moves:
        raise GameError("no moves in the game")

    first = moves[0]
    if "first_player" in game:
        turn = lookup(game["first_player"], players, "player")
    elif "asker" in first:
        turn = lookup(first["asker"], players, "player")
    else:
        raise GameError("the first move must be an ask (or give first_player)")

    worlds = initial_worlds()
    frames, durs = [], []

    def add(im, t):
        frames.append(im)
        durs.append(t)

    move_lines = []
    add(draw_frame(worlds, turn, players, cards, title, [("Before the first move", "muted")],
                   "Nothing is dealt, nothing is hidden. Every card could be with anyone: "
                   "all 81 worlds are still possible."), ms["intro"])

    for k, m in enumerate(moves, 1):
        where = "move %d" % k
        if "kwartet" in m:
            if k != len(moves):
                raise GameError("%s: a kwartet must be the last move" % where)
            p = lookup(m["kwartet"], players, "player")
            before = len(worlds)
            worlds = apply_kwartet(worlds, p, check, where)
            sub = ("One world was left, so the announcement confirms what the notebook already knew."
                   if before == 1 else
                   "The announcement rules out every world where %s lacks a card." % players[p])
            segs = kwartet_segments(k, players, p)
            move_lines.append(segs)
            add(draw_frame(worlds, p, players, cards, title, segs, sub,
                           banner=banner or None), ms["end"])
            break

        x = lookup(m.get("asker"), players, "asker")
        y = lookup(m.get("respondent"), players, "respondent")
        c = lookup(m.get("card"), cards, "card")
        yes = parse_answer(m.get("answer"))
        if x == y:
            raise GameError("%s: a player cannot ask themselves" % where)
        if check and x != turn:
            raise GameError("%s: %s asks, but it is %s's turn" % (where, players[x], players[turn]))

        add(draw_frame(worlds, x, players, cards, title, ask_segments(k, players, cards, x, y, c),
                       "Waiting for the answer...", highlight=(y, c)), ms["ask"])

        before = possible_owners(worlds)
        worlds = apply_ask(worlds, x, y, c, yes, check, where)
        after = possible_owners(worlds)
        turn = x if yes else y

        if yes:
            sub = "YES: %s moves to %s, and %s keeps the turn." % (cards[c], players[x], players[x])
        else:
            sub = "NO: nothing moves, the turn passes to %s." % players[y]
        learned = []
        for cc in range(4):
            if len(before[cc]) > 1 and len(after[cc]) == 1 and not (yes and cc == c):
                learned.append("%s is with %s" % (cards[cc], players[next(iter(after[cc]))]))
        learned = ("Now known: " + ", ".join(learned) + ".") if learned else None
        segs = ask_segments(k, players, cards, x, y, c, yes)
        move_lines.append(segs)
        add(draw_frame(worlds, turn, players, cards, title, segs, sub, learned,
                       highlight=(y, c)), ms["answer"])
    return frames, durs, move_lines, title


def main():
    ap = argparse.ArgumentParser(description="Animate a single-category Blind Kwartet game.")
    ap.add_argument("game", nargs="?", help="game JSON file (same as -i; wins if both are given)")
    ap.add_argument("-i", "--input", default="./post2/Figure_1_game.json",
                    help="game JSON file (default ./post2/Figure_1_game.json)")
    ap.add_argument("-o", "--output", default="./post2/Figure_1.gif",
                    help="output GIF (default ./post2/Figure_1.gif)")
    ap.add_argument("--moves", help="path of the moves PNG (default: <output>_moves.png)")
    ap.add_argument("--no-moves", action="store_true", help="do not write the moves PNG")
    ap.add_argument("--sheet", help="also write a PNG contact sheet of all frames")
    ap.add_argument("--scale", type=float, default=1.0, help="resize factor for the GIF (default 1.0)")
    ap.add_argument("--no-check", action="store_true", help="skip rule and turn validation")
    ap.add_argument("--intro-ms", type=int, default=2600)
    ap.add_argument("--ask-ms", type=int, default=1300)
    ap.add_argument("--answer-ms", type=int, default=2200)
    ap.add_argument("--end-ms", type=int, default=4200)
    a = ap.parse_args()

    src = a.game or a.input
    try:
        with open(src, encoding="utf-8") as f:
            game = json.load(f)
    except OSError as e:
        sys.exit("error: cannot read the game file %s: %s" % (src, e.strerror or e))
    except json.JSONDecodeError as e:
        sys.exit("error: %s is not valid JSON: %s" % (src, e))
    ms = dict(intro=a.intro_ms, ask=a.ask_ms, answer=a.answer_ms, end=a.end_ms)
    try:
        frames, durs, move_lines, title = build(game, not a.no_check, ms)
    except GameError as e:
        sys.exit("error: %s" % e)

    def ensure_dir(path):
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)      # e.g. ./post2/ need not exist yet

    if not a.no_moves:
        stem = a.output[:-4] if a.output.lower().endswith(".gif") else a.output
        path = a.moves or stem + "_moves.png"
        ensure_dir(path)
        moves_png(title, move_lines, path)
        print("wrote %s" % path)
    ensure_dir(a.output)
    if a.sheet:
        ensure_dir(a.sheet)

    out = frames
    if a.scale != 1.0:
        size = (int(W * a.scale), int(H * a.scale))
        out = [f.resize(size, Image.LANCZOS) for f in frames]
    out[0].save(a.output, save_all=True, append_images=out[1:], duration=durs, loop=0, disposal=2)
    print("wrote %s (%d frames)" % (a.output, len(out)))

    if a.sheet:
        cols = 3
        rows = (len(frames) + cols - 1) // cols
        tw, th = W // 2, H // 2
        sheet = Image.new("RGB", (cols * tw, rows * th), (255, 255, 255))
        for k, f in enumerate(frames):
            sheet.paste(f.resize((tw, th)), ((k % cols) * tw, (k // cols) * th))
        sheet.save(a.sheet)
        print("wrote %s" % a.sheet)


if __name__ == "__main__":
    main()
