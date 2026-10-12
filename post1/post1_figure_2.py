"""Figure 2 -- the same state, compressed: 87 count tables + a naming matrix.

Run from the repo root:   python post2_figure_2.py
Writes:                   post2/Figure_2.png

The 87 count tables are computed from the 34,032 worlds (a table is the 3x3
matrix of 'how many cards of category A/B/C does each player start with').
A table is lit when at least one surviving world has that table.
"""
from itertools import product
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

OUT = Path("post1")
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- style
BG, DARK, YELLOW = "#080a10", "#1e2433", "#ffd56b"
TEXT, MUTED, RULE = "#e8e9ee", "#8b92a8", "#2a2f40"
CROSS, BOXLINE = "#555c73", "#2d3345"
W, H, DPI = 1960, 760, 100
SERIF = "DejaVu Serif"


def pt(px):
    return px * 72 / DPI


# ------------------------------------------------------------ multiverse
FULL = {tuple(range(4 * c, 4 * c + 4)) for c in range(3)}


def all_worlds():
    for owners in product(range(3), repeat=12):
        if owners.count(0) != 4 or owners.count(1) != 4:
            continue
        hands = tuple(tuple(c for c in range(12) if owners[c] == p) for p in range(3))
        if any(h in FULL for h in hands):
            continue
        yield hands


def consistent(world):
    peter, quinty, robin = world
    if 0 not in robin:                                   # Electron (A1) is Robin's
        return False
    if not any(c in peter for c in (1, 2, 3)):           # Peter holds another A
        return False
    if 4 in quinty:                                      # Quinty does not hold Newton (B1)
        return False
    if not any(c in quinty for c in (5, 6, 7)):          # Quinty holds another B
        return False
    return True


def count_table(world):
    return tuple(tuple(sum(1 for c in hand if c // 4 == k) for k in range(3))
                 for hand in world)


worlds = list(all_worlds())
tables = sorted({count_table(w) for w in worlds})
alive_tables = {count_table(w) for w in worlds if consistent(w)}
n_alive_worlds = sum(consistent(w) for w in worlds)
print(f"tables: {len(tables)}, still possible: {len(alive_tables)}, "
      f"worlds still possible: {n_alive_worlds}")
assert len(tables) == 87

FRAMED = 38                                  # the table shown on the right
framed_table = tables[FRAMED]
assert framed_table in alive_tables
print("framed table:", framed_table)

# ---------------------------------------------------------------- canvas
fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.axis("off")


def T(x, y, s, size, color=TEXT, weight="normal", style="normal", ha="left"):
    return ax.text(x, y, s, fontsize=pt(size), color=color, fontweight=weight,
                   fontstyle=style, fontfamily=SERIF, ha=ha, va="center")


T(60, 60, "The same state, compressed", 34, weight="bold")
T(60, 100, "87 bits for the count tables, plus a small naming matrix", 22,
  color=MUTED, style="italic")

for x in (661, 1261):
    ax.plot([x, x], [128, 690], color=RULE, lw=2.2)

# ------------------------------------------------------ left: count tables
T(60, 143, "Count tables", 24, weight="bold")
X0, Y0, PITCH, CELL = 60, 170, 48, 46
for i, t in enumerate(tables):
    r, c = divmod(i, 10)
    x, y = X0 + c * PITCH, Y0 + r * PITCH
    ax.add_patch(Rectangle((x, y), CELL, CELL, color=YELLOW if t in alive_tables else DARK, lw=0))
    if i == FRAMED:
        ax.add_patch(Rectangle((x, y), CELL, CELL, fill=False, ec="white", lw=2.2))

ax.add_patch(Rectangle((60, 616), 23, 23, color=YELLOW, lw=0))
T(96, 626, f"{len(alive_tables)} tables still possible", 21)
ax.add_patch(Rectangle((60, 656), 23, 23, color=DARK, lw=0))
T(96, 666, f"{len(tables) - len(alive_tables)} ruled out", 21)

# ----------------------------------------------------------- naming matrix
T(700, 143, "Naming matrix", 25, weight="bold")
T(700, 173, "possible initial owners of each named card", 18, color=MUTED, style="italic")

players = ["Peter", "Quinty", "Robin"]
box_x = [896, 1016, 1136]
for name, bx in zip(players, box_x):
    T(bx + 54, 217, name, 21, weight="bold", ha="center")

# who could have held each named card at the start (derived from the history)
named = [
    ("Electron", "A1", [False, False, True]),
    ("Newton", "B1", [True, False, True]),
]
# sanity check against the real worlds: owner sets seen in surviving worlds
owner_sets = {0: set(), 4: set()}
for w in worlds:
    if consistent(w):
        for p, hand in enumerate(w):
            for card in owner_sets:
                if card in hand:
                    owner_sets[card].add(p)
assert owner_sets[0] == {2} and owner_sets[4] == {0, 2}

for row, (label, code, possible) in enumerate(named):
    y_top = 254 + 84 * row
    T(700, y_top + 19, label, 23, style="italic")
    T(700, y_top + 48, code, 18, color=MUTED)
    for ok, bx in zip(possible, box_x):
        ax.add_patch(Rectangle((bx, y_top), 108, 72, fc=BG, ec=BOXLINE, lw=1.8))
        cx, cy = bx + 54, y_top + 36
        if ok:
            ax.add_patch(Circle((cx, cy), 15, color=YELLOW, lw=0))
        else:
            d = 12
            ax.plot([cx - d, cx + d], [cy - d, cy + d], color=CROSS, lw=2.6, solid_capstyle="round")
            ax.plot([cx - d, cx + d], [cy + d, cy - d], color=CROSS, lw=2.6, solid_capstyle="round")

T(700, 457, "Electron: Peter asked for it, and Quinty said no.", 18, color=MUTED, style="italic")
T(700, 489, "Newton: Quinty asked for it, so she does not hold it.", 18, color=MUTED, style="italic")

# --------------------------------------------------- right: surviving table
T(1300, 143, "One of the surviving tables", 25, weight="bold")
T(1300, 173, "the framed square on the left", 18, color=MUTED, style="italic")
col_x = [1455, 1545, 1635]
for letter, cx in zip("ABC", col_x):
    T(cx, 221, letter, 21, color=MUTED, weight="bold", ha="center")
ax.plot([1400, 1681], [253, 253], color="#3a4054", lw=1.4)
for p, name in enumerate(players):
    y = 292 + 70 * p
    T(1300, y, name, 21)
    for k, cx in enumerate(col_x):
        T(cx, y, str(framed_table[p][k]), 32, color=YELLOW, weight="bold", ha="center")

T(1300, 509, "Every row and column sums to four.", 18, color=MUTED, style="italic")
T(1300, 541, "Counts of cards, not which cards.", 18, color=MUTED, style="italic")

T(60, 719, f"Each of the {len(alive_tables)} lit tables still has at least one world. "
           f"Together with the naming matrix they describe the same {n_alive_worlds:,} "
           f"worlds as Figure 1.", 18, color=MUTED, style="italic")

fig.savefig(OUT / "Figure_2.png", dpi=DPI, facecolor=BG)
print("wrote", OUT / "Figure_2.png")
