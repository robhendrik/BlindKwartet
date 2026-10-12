"""Figure 1 -- the game after two questions: one bit per world.

Run from the repo root:   python post2_figure_1.py
Writes:                   post2/Figure_1.png

The 34,032 worlds are enumerated for real (every deal of the 12 labelled
cards over Peter, Quinty and Robin in which nobody starts with a complete
category), the two questions are applied as constraints, and the surviving
worlds are drawn as yellow cells.
"""
from itertools import product
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

OUT = Path("post1")
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- style
BG, DARK, YELLOW = "#080a10", "#1e2433", "#ffd56b"
TEXT, MUTED, RULE = "#e8e9ee", "#8b92a8", "#2a2f40"
W, H, DPI = 1960, 962, 100          # canvas in pixels (1 data unit = 1 px)
SERIF = "DejaVu Serif"


def pt(px):
    """pixel font size -> points"""
    return px * 72 / DPI


# ------------------------------------------------------------ multiverse
# cards 0..11 = A1..A4, B1..B4, C1..C4
FULL = {tuple(range(4 * c, 4 * c + 4)) for c in range(3)}


def all_worlds():
    """Systematic list of deals, in lexicographic order of the owner string
    (owner of A1, owner of A2, ..., owner of C4) with Peter=0, Quinty=1, Robin=2."""
    for owners in product(range(3), repeat=12):
        if owners.count(0) != 4 or owners.count(1) != 4:
            continue
        hands = tuple(tuple(c for c in range(12) if owners[c] == p) for p in range(3))
        if any(h in FULL for h in hands):
            continue
        yield hands


def consistent(world):
    peter, quinty, robin = world
    # 1. Peter asks Quinty for the Electron (A1) -> "No"
    #    Peter holds another A, and neither Peter nor Quinty holds A1.
    if 0 not in robin:
        return False
    if not any(c in peter for c in (1, 2, 3)):
        return False
    # 2. Quinty asks Peter for Newton (B1), not answered yet
    #    Quinty holds another B but not B1.
    if 4 in quinty:
        return False
    if not any(c in quinty for c in (5, 6, 7)):
        return False
    return True


worlds = list(all_worlds())
alive = np.array([consistent(w) for w in worlds])
n_worlds, n_alive = len(worlds), int(alive.sum())
print(f"worlds: {n_worlds}, still possible: {n_alive}")
assert n_worlds == 34032

# ---------------------------------------------------------------- canvas
fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.axis("off")


def T(x, y, s, size, color=TEXT, weight="normal", style="normal", ha="left", **kw):
    return ax.text(x, y, s, fontsize=pt(size), color=color, fontweight=weight,
                   fontstyle=style, fontfamily=SERIF, ha=ha, va="center", **kw)


def run(x, y, segments, gap=10):
    """Several differently styled text pieces on one line."""
    renderer = fig.canvas.get_renderer()
    for s, kw in segments:
        t = T(x, y, s, **kw)
        x += t.get_window_extent(renderer).width + gap


def dotted(x0, x1, y):
    ax.plot([x0, x1], [y, y], color="#6f768c", lw=0.9, linestyle=(0, (1, 3.2)),
            dash_capstyle="round")


# ------------------------------------------------------------ left: bits
COLS, CELL = 192, 4
ROWS = -(-n_worlds // COLS)                       # 178
rgba = np.zeros((ROWS * COLS, 4))
dark_rgb = matplotlib.colors.to_rgb(DARK)
yellow_rgb = matplotlib.colors.to_rgb(YELLOW)
for i, a in enumerate(alive):
    rgba[i] = (*(yellow_rgb if a else dark_rgb), 1.0)   # padding stays transparent
rgba = rgba.reshape(ROWS, COLS, 4)

x0, y0 = 60, 130
ax.imshow(rgba, extent=(x0, x0 + COLS * CELL, y0 + ROWS * CELL, y0),
          interpolation="nearest", aspect="auto", zorder=1)
ax.set_xlim(0, W)
ax.set_ylim(H, 0)

T(60, 61, "The state of the game as bits", 34, weight="bold")
T(60, 100, f"one bit per world, {n_worlds:,} in all", 22, color=MUTED, style="italic")

# divider
ax.plot([879, 879], [130, 842], color=RULE, lw=2.2)

# ----------------------------------------------------------- right panel
X = 908
T(X, 145, "Bits", 25, weight="bold")
ax.add_patch(Rectangle((X, 181), 24, 24, color=YELLOW, lw=0))
T(944, 192, f"{n_alive:,} worlds still possible", 22)
ax.add_patch(Rectangle((X, 221), 24, 24, color=DARK, lw=0))
T(944, 232, f"{n_worlds - n_alive:,} worlds ruled out", 22)

T(X, 335, "Names so far", 25, weight="bold")

columns = [
    (908, "A", "Elementary particles", ["Electron", "", "", ""]),
    (1228, "B", "Physicists", ["Newton", "", "", ""]),
    (1548, "C", "", ["", "", "", ""]),
]
for cx, letter, title, names in columns:
    T(cx, 388, letter, 21, color=MUTED, weight="bold")
    if title:
        T(cx + 30, 388, title, 22, weight="bold")
    else:
        dotted(cx + 30, cx + 292, 396)
    ax.plot([cx, cx + 290], [410, 410], color="#3a4054", lw=1.2)
    for k, name in enumerate(names):
        y = 439 + 40 * k
        T(cx, y, f"{letter}{k + 1}", 18, color=MUTED)
        if name:
            T(cx + 40, y, name, 23, style="italic")
        else:
            dotted(cx + 40, cx + 290, y + 11)

T(X, 643, "History", 25, weight="bold")
run(X, 688, [("1.", dict(size=22, color=MUTED)),
             ("Peter asks Quinty:", dict(size=22)),
             ("Electron (elementary particles)?", dict(size=22, style="italic")),
             ("No", dict(size=22, color=YELLOW, weight="bold"))])
run(X, 732, [("2.", dict(size=22, color=MUTED)),
             ("Quinty asks Peter:", dict(size=22)),
             ("Newton (physicists)?", dict(size=22, style="italic")),
             ("...", dict(size=22, color=YELLOW, weight="bold"))])

T(60, 877, "Illustration: the 34,032 worlds are laid out row by row, "
           "in the order of a systematic list of deals.", 18, color=MUTED, style="italic")

fig.savefig(OUT / "Figure_1.png", dpi=DPI, facecolor=BG)
print("wrote", OUT / "Figure_1.png")
