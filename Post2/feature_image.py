#!/usr/bin/env python3
"""
feature_image.py - feature image for "Teaching a Computer to Play Blind Kwartet".

One position, three answers: after P1 asks P2 for A1 and hears NO, a search of
depth 1, 2 and 3 chooses three different questions. The root card (the position)
sends one arc to each chosen question.

    python3 feature_image.py                      # writes Feature_image.png
    python3 feature_image.py -o out.png --width 2400 --height 1350
    xvfb-run -a python3 feature_image.py          # if there is no display (servers, CI)

Requires: pyvista  (pip install pyvista)
"""
import argparse
import numpy as np
import pyvista as pv

# ---- palette (matches the notebook GIF: P1 purple, P2 teal, P3 coral) ----
CARD = (0.96, 0.945, 0.90)
CARD_EDGE = (0.80, 0.78, 0.72)
INK = (0.17, 0.17, 0.16)
NO_RED = (0.64, 0.18, 0.18)
PLAYER = {"P1": (0.31, 0.27, 0.72), "P2": (0.05, 0.43, 0.34), "P3": (0.76, 0.28, 0.14)}
ARC = (0.94, 0.62, 0.15)          # the amber of the "worlds still possible" squares
DEPTH_TXT_CARD = (0.30, 0.29, 0.26)

CARD_W, CARD_T, CARD_H = 3.0, 0.07, 4.2


def text_mesh(s, height, depth=0.03):
    """Text3D scaled to a given cap height, centred on x and z=0, lying in the xz-plane
    so that it reads upright from the -y side (the camera side)."""
    t = pv.Text3D(s, depth=depth)
    b = t.bounds
    sc = height / max(b[3] - b[2], 1e-9)          # scale by the y-extent (text height)
    t.points = t.points * sc
    b = t.bounds
    t.points = t.points - np.array([(b[0] + b[1]) / 2, (b[2] + b[3]) / 2, 0.0])
    t.rotate_x(90, point=(0, 0, 0), inplace=True)         # up -> +z, extrusion -> -y
    return t


def make_card(lines, yaw=0.0, pos=(0, 0, 0)):
    """A card standing on the floor. lines: list of (text, rgb, cap_height, z_centre)."""
    parts = []
    body = pv.Box(bounds=(-CARD_W / 2, CARD_W / 2, -CARD_T / 2, CARD_T / 2, 0, CARD_H))
    parts.append((body, CARD))
    rim = pv.Box(bounds=(-CARD_W / 2 - 0.04, CARD_W / 2 + 0.04, -CARD_T / 2 + 0.02,
                         CARD_T / 2 - 0.02, -0.04, CARD_H + 0.04))
    parts.append((rim, CARD_EDGE))
    for s, col, h, zc in lines:
        t = text_mesh(s, h)
        t.translate((0, -CARD_T / 2 - 0.005, zc), inplace=True)
        parts.append((t, col))
    out = []
    for m, c in parts:
        m = m.copy()
        m.rotate_z(yaw, point=(0, 0, 0), inplace=True)
        m.translate(pos, inplace=True)
        out.append((m, c))
    return out


def arc(p0, p1, lift, n=60, radius=0.10):
    """A tube from p0 to p1 bulging upward by `lift`."""
    p0, p1 = np.array(p0, float), np.array(p1, float)
    t = np.linspace(0, 1, n)[:, None]
    pts = p0 + (p1 - p0) * t
    pts[:, 2] += lift * np.sin(np.pi * t[:, 0])
    return pv.Spline(pts, n).tube(radius=radius)


def build(width, height, out):
    pl = pv.Plotter(off_screen=True, window_size=(width, height))
    pl.set_background((0.02, 0.025, 0.04), top=(0.09, 0.11, 0.17))
    try:
        pl.enable_anti_aliasing("ssaa")
    except Exception:
        pl.enable_anti_aliasing()

    # the position: root card at the left
    root = make_card(
        [("A1", INK, 1.1, 2.75), ("NO", NO_RED, 0.62, 1.30), ("position", DEPTH_TXT_CARD, 0.42, 0.52)],
        yaw=-6, pos=(-8.5, 0.6, 0))
    # the three answers, one per search depth
    leaves = [
        ("depth 1", make_card([("A2?", INK, 0.95, 2.75), ("P1", PLAYER["P1"], 0.62, 1.30), ("depth 1", DEPTH_TXT_CARD, 0.42, 0.52)],
                              yaw=4, pos=(-2.2, 0.0, 0)), 2.4),
        ("depth 2", make_card([("B1?", INK, 0.95, 2.75), ("P1", PLAYER["P1"], 0.62, 1.30), ("depth 2", DEPTH_TXT_CARD, 0.42, 0.52)],
                              yaw=-3, pos=(3.4, 1.2, 0)), 3.9),
        ("depth 3", make_card([("A1?", INK, 0.95, 2.75), ("P3", PLAYER["P3"], 0.62, 1.30), ("depth 3", DEPTH_TXT_CARD, 0.42, 0.52)],
                              yaw=5, pos=(9.0, 2.4, 0)), 5.4),
    ]

    scene = list(root)
    for _, card, _ in leaves:
        scene += card
    for label, card, lift in leaves:
        pos = card[0][0].center
        top_root = (-8.5, 0.6, CARD_H + 0.1)
        top_leaf = (pos[0], pos[1], CARD_H + 0.1)
        scene.append((arc(top_root, top_leaf, lift), ARC))

    for m, c in scene:
        pl.add_mesh(m, color=c, smooth_shading=True, specular=0.12, specular_power=10,
                    ambient=0.25, diffuse=0.85)
        # reflection in the floor: a dimmer mirrored copy
        if c != ARC:
            pl.add_mesh(m.reflect((0, 0, 1), point=(0, 0, 0)), color=c, opacity=0.22,
                        smooth_shading=True, ambient=0.3, diffuse=0.6)

    pl.remove_all_lights()
    pl.add_light(pv.Light(position=(-14, -22, 20), focal_point=(0, 0, 2), intensity=0.9))
    pl.add_light(pv.Light(position=(18, -12, 9), focal_point=(0, 0, 2), intensity=0.45,
                          color=(0.75, 0.8, 1.0)))

    pl.camera.position = (1.5, -29.0, 12.0)
    pl.camera.focal_point = (0.3, 0.8, 3.0)
    pl.camera.up = (0, 0, 1)
    pl.camera.view_angle = 30
    pl.show(screenshot=out)
    print("wrote", out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", default="./post2/Feature_image.png")
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    a = ap.parse_args()
    build(a.width, a.height, a.output)
