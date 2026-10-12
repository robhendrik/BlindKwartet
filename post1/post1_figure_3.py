"""Figure 3 -- every name still has somewhere to go, but together they do not fit.

Run from the repo root:   python post2_figure_3.py
Writes:                   post2/Figure_3.png
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

OUT = Path("post1")
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- style
BG, DARK, YELLOW = "#080a10", "#1e2433", "#ffd56b"
TEXT, MUTED = "#e8e9ee", "#8b92a8"
GREY_EDGE, ROBIN_FILL, RED = "#565d78", "#25221a", "#ff7a70"
W, H, DPI = 1700, 780, 100
SERIF = "DejaVu Serif"


def pt(px):
    return px * 72 / DPI


fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.set_aspect("equal")
ax.axis("off")


def T(x, y, s, size, color=TEXT, weight="normal", style="normal", ha="left"):
    return ax.text(x, y, s, fontsize=pt(size), color=color, fontweight=weight,
                   fontstyle=style, fontfamily=SERIF, ha=ha, va="center")


def box(x, y, w, h, fc, ec, lw=2.4):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=8",
                                fc=fc, ec=ec, lw=lw, zorder=3))


T(60, 61, "Every name fits somewhere, but not all together", 34, weight="bold")
T(60, 100, "names we have invented, and the places the table leaves for them", 22,
  color=MUTED, style="italic")

# ------------------------------------------------------------- right side
BX, BW, BH = 951, 308, 66
places = {
    "Peter": (127, False),
    "Quinty": (247, False),
    "Robin, place 1": (367, True),
    "Robin, place 2": (487, True),
}
for label, (y, open_) in places.items():
    if open_:
        box(BX, y, BW, BH, ROBIN_FILL, YELLOW)
        T(BX + 20, y + BH / 2 + 1, label, 24, weight="bold")
    else:
        box(BX, y, BW, BH, DARK, GREY_EDGE)
        T(BX + 20, y + BH / 2 + 1, label, 24, weight="bold")
        T(BX + 159, y + BH / 2 + 1, "not possible", 18, color=MUTED, style="italic")
        cx, cy, d = 924, y + BH / 2, 12
        ax.plot([cx - d, cx + d], [cy - d, cy + d], color=RED, lw=3, solid_capstyle="round")
        ax.plot([cx - d, cx + d], [cy + d, cy - d], color=RED, lw=3, solid_capstyle="round")

# bracket + count
ax.plot([1280, 1280], [367, 553], color=YELLOW, lw=2.6, solid_capstyle="butt")
T(1300, 390, "3 names,", 26, color=YELLOW, weight="bold")
T(1300, 424, "2 places", 26, color=YELLOW, weight="bold")

# ------------------------------------------------------------- left side
names = [("Electron", "A1", 210), ("Muon", "A2", 350), ("Photon", "A3", 490)]
targets = [BX - 1, BX - 1]
target_y = [places["Robin, place 1"][0] + BH / 2, places["Robin, place 2"][0] + BH / 2]

for label, code, y in names:
    T(274, y - 1, label, 24, weight="bold", ha="right")
    ax.add_patch(Circle((330, y), 34, color=YELLOW, lw=0, zorder=4))
    T(330, y + 1, code, 21, color="#1b1a14", weight="bold", ha="center").set_zorder(5)
    for ty in target_y:                       # a name may sit in either of Robin's places
        ax.plot([364, BX - 1], [y, ty], color=YELLOW, lw=1.5, zorder=2)

# ------------------------------------------------------------------ notes
T(60, 662, "Each name was asked for by one of Peter and Quinty and refused by the "
           "other, so each can only be Robin's.", 20, color=MUTED, style="italic")
T(60, 696, "Peter and Quinty each asked for a particle, so each holds at least one: "
           "Robin has at most two of the four.", 20, color=MUTED, style="italic")
T(60, 730, "This is the best case; every other table leaves Robin fewer particle places.",
  20, color=MUTED, style="italic")

fig.savefig(OUT / "Figure_3.png", dpi=DPI, facecolor=BG)
print("wrote", OUT / "Figure_3.png")
