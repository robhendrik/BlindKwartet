"""
Feature image: "A Card Game With Cards That Don't Exist (Yet)"

Four cards fanned in a hand, on a black background. One card has just been
inked: "Electron". The other three are only dotted outlines with a faint
question mark. Cards are lacquered (PBR with a clear coat), lit by soft studio
light, and mirrored in a glossy black surface.

Run:    python feature_image.py
Needs:  pip install pyvista numpy pillow
Output: feature_image.png (2800 x 1576)

Everything you may want to change is in the SETTINGS block.
"""

import math
from pathlib import Path

import numpy as np
import pyvista as pv
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# --------------------------------------------------------------------------
# SETTINGS
# --------------------------------------------------------------------------
OUT = Path("feature_image.png")
WINDOW = (1400, 788)          # rendered window; the screenshot is scaled by SCALE
SCALE = 2                     # output = WINDOW * SCALE
MAIN_TEXT = "Electron"
SUB_TEXT = "elementary particles"

CARD_W, CARD_H, CARD_T = 2.5, 3.5, 0.035   # poker proportions, units are arbitrary
CORNER_R = 0.17

# Fan, left to right. Positive angle leans the card to the left (counter-clockwise).
GHOST_ANGLES = [46, 27, 8]
NAMED_ANGLE = -19
NAMED_LIFT = (1.0, 0.15, 0.45)    # (dx, dy, dz): the named card is pulled out of the hand
TILT_BACK = -7                      # degrees, leans the cards back a little
Z_STEP = 0.07

BOW_X, BOW_Y = 0.11, 0.04           # how much the cards curve towards the viewer
GRID = 0.03                         # mesh resolution of a card (smaller = smoother, slower)
GLOSS_ROUGHNESS = 0.28
COAT_STRENGTH = 0.8
ENV_LEVEL = 1.0                    # brightness of the soft boxes the cards mirror
REFLECTION_OPACITY = 0.30           # strength of the mirror image in the surface
BACKDROP_GLOW = True                # very faint pool of light behind the hand
FONT_CANDIDATES = [                 # first one found is used for the handwriting
    "DejaVuSerif-Italic.ttf", "Georgia Italic.ttf", "georgiai.ttf",
    "Times New Roman Italic.ttf", "timesi.ttf", "LiberationSerif-Italic.ttf",
    "Palatino.ttc", "DejaVuSerif.ttf",
]

TEX_W, TEX_H = 1000, 1400           # card face texture, same ratio as the card
# Where the faint question mark sits on each ghost card. Cards further back are
# covered more by their neighbours, so their mark sits closer to the visible left edge.
GHOST_QUESTION = [dict(qx=0.19, qy=0.15, qsize=220), dict(qx=0.20, qy=0.16, qsize=290),
                  dict(qx=0.30, qy=0.17, qsize=330)]


# --------------------------------------------------------------------------
# Card face textures (Pillow)
# --------------------------------------------------------------------------
def load_font(size):
    for name in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default(size=size)


def rounded_rect_path(w, h, r, margin, n=60):
    """Dense closed polyline of a rounded rectangle, in pixel coordinates."""
    x0, y0, x1, y1 = margin, margin, w - margin, h - margin
    pts = []
    centres = [(x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0),
               (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)]
    for cx, cy, a0 in centres:
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    pts.append(pts[0])
    return np.array(pts)


def points_along(path, spacing):
    seg = np.linalg.norm(np.diff(path, axis=0), axis=1)
    s = np.r_[0, np.cumsum(seg)]
    targets = np.arange(0, s[-1], spacing)
    xs = np.interp(targets, s, path[:, 0])
    ys = np.interp(targets, s, path[:, 1])
    return np.c_[xs, ys]


def gradient(w, h, top, bottom):
    t = np.linspace(0, 1, h)[:, None, None]
    top, bottom = np.array(top, float), np.array(bottom, float)
    return (top * (1 - t) + bottom * t) * np.ones((h, w, 1))


def finish(arr, noise=2.5, seed=1):
    rng = np.random.default_rng(seed)
    grain = rng.normal(0, noise, arr.shape[:2])[:, :, None]
    grain = np.asarray(Image.fromarray(np.clip(grain * 8 + 128, 0, 255).astype(np.uint8)
                                       .squeeze()).filter(ImageFilter.GaussianBlur(0.8)),
                       float)[:, :, None]
    return Image.fromarray(np.clip(arr + (grain - 128) / 8, 0, 255).astype(np.uint8))


def named_card_face():
    base = finish(gradient(TEX_W, TEX_H, (250, 246, 236), (232, 226, 210)), seed=2)
    draw = ImageDraw.Draw(base)
    # thin printed border
    draw.rounded_rectangle((55, 55, TEX_W - 55, TEX_H - 55), radius=60,
                           outline=(205, 198, 180), width=4)
    # ink: draw on a mask, blur a touch so it bleeds into the paper
    ink = Image.new("L", (TEX_W, TEX_H), 0)
    d = ImageDraw.Draw(ink)
    d.text((TEX_W / 2, TEX_H * 0.46), MAIN_TEXT, font=load_font(190),
           fill=255, anchor="mm")
    d.line((TEX_W * 0.22, TEX_H * 0.575, TEX_W * 0.78, TEX_H * 0.575), fill=150, width=4)
    ink = ink.filter(ImageFilter.GaussianBlur(1.6))
    base.paste(Image.new("RGB", base.size, (22, 24, 48)), mask=ink)
    sub = Image.new("L", (TEX_W, TEX_H), 0)
    ImageDraw.Draw(sub).text((TEX_W / 2, TEX_H * 0.63), SUB_TEXT.upper(),
                             font=load_font(52), fill=170, anchor="mm")
    base.paste(Image.new("RGB", base.size, (60, 62, 84)),
               mask=sub.filter(ImageFilter.GaussianBlur(1.0)))
    return base


def ghost_card_face(seed, qx=0.30, qy=0.17, qsize=330):
    base = finish(gradient(TEX_W, TEX_H, (40, 47, 66), (16, 19, 29)), noise=1.5, seed=seed)
    glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    path = rounded_rect_path(TEX_W, TEX_H, 90, 85)
    for x, y in points_along(path, 38):
        gd.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(175, 198, 235, 235))
    # question mark sits in the part of the card that stays visible in the fan
    gd.text((TEX_W * qx, TEX_H * qy), "?", font=load_font(qsize),
            fill=(175, 198, 235, 150), anchor="mm")
    soft = glow.filter(ImageFilter.GaussianBlur(5))
    out = base.convert("RGBA")
    out.alpha_composite(soft)
    out.alpha_composite(glow)
    return out.convert("RGB")


# --------------------------------------------------------------------------
# Card geometry
# --------------------------------------------------------------------------
def rounded_rect_outline(w, h, r, n=22):
    pts = []
    centres = [(w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90),
               (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)]
    for cx, cy, a0 in centres:
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return np.array(pts)


def bow(x, y):
    """Real cards are never flat: a slight bow makes the reflection sweep across."""
    return (BOW_X * (1 - (2 * x / CARD_W) ** 2)
            + BOW_Y * (1 - (2 * y / CARD_H) ** 2))


def make_card():
    """Return (face, body). Face is the textured front, body the slab behind it."""
    grid = pv.Plane(center=(0, 0, 0), direction=(0, 0, 1),
                    i_size=CARD_W + 0.2, j_size=CARD_H + 0.2,
                    i_resolution=int((CARD_W + 0.2) / GRID), j_resolution=int((CARD_H + 0.2) / GRID))
    x, y = grid.points[:, 0], grid.points[:, 1]
    qx = np.abs(x) - (CARD_W / 2 - CORNER_R)          # signed distance to the rounded rectangle
    qy = np.abs(y) - (CARD_H / 2 - CORNER_R)
    grid["sdf"] = (np.hypot(np.maximum(qx, 0), np.maximum(qy, 0))
                   + np.minimum(np.maximum(qx, qy), 0) - CORNER_R)
    clipped = grid.clip_scalar(scalars="sdf", value=0.0, invert=True)
    try:                                    # newer PyVista wants the algorithm spelled out
        surf = clipped.extract_surface(algorithm="dataset_surface")
    except TypeError:
        surf = clipped.extract_surface()
    surf = surf.triangulate().clean()
    surf.clear_data()

    body = surf.extrude((0, 0, -CARD_T), capping=True)
    face = surf.copy()
    for mesh, dz in ((body, 0.0), (face, 0.0015)):
        p = mesh.points
        p[:, 2] += bow(p[:, 0], p[:, 1]) + dz
        mesh.points = p
    p = surf.points
    face.active_texture_coordinates = np.c_[p[:, 0] / CARD_W + 0.5, p[:, 1] / CARD_H + 0.5]
    return face, body


def place(mesh, angle_deg, z, extra=(0, 0, 0)):
    """Rotate a card about the bottom pivot of the hand and stack it."""
    a, t = math.radians(angle_deg), math.radians(TILT_BACK)
    rz = np.array([[math.cos(a), -math.sin(a), 0, 0], [math.sin(a), math.cos(a), 0, 0],
                   [0, 0, 1, 0], [0, 0, 0, 1]])
    rx = np.array([[1, 0, 0, 0], [0, math.cos(t), -math.sin(t), 0],
                   [0, math.sin(t), math.cos(t), 0], [0, 0, 0, 1]])
    up = np.eye(4)
    up[1, 3] = CARD_H / 2 - 0.35
    mv = np.eye(4)
    mv[:3, 3] = (extra[0], extra[1], z + extra[2])
    return mesh.transform(mv @ rz @ rx @ up, inplace=False)


# --------------------------------------------------------------------------
# Scene helpers
# --------------------------------------------------------------------------
def studio_environment():
    """Equirectangular 'studio': black, with a few soft boxes the cards can mirror."""
    w, h = 2048, 1024
    img = np.zeros((h, w, 3), float)

    def box(u0, u1, v0, v1, level, tint=(1, 1, 1)):
        x0, x1, y0, y1 = int(u0 * w), int(u1 * w), int(v0 * h), int(v1 * h)
        img[y0:y1, x0:x1] = np.array(tint) * level

    box(0.30, 0.70, 0.04, 0.22, 1.0 * ENV_LEVEL)                 # big overhead soft box
    box(0.08, 0.14, 0.25, 0.60, 0.8 * ENV_LEVEL, (0.8, 0.9, 1))  # cool strip on the left
    box(0.86, 0.92, 0.25, 0.60, 0.7 * ENV_LEVEL, (1, 0.9, 0.8))  # warm strip on the right
    blur = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(28))
    tex = pv.Texture(np.asarray(blur))
    tex.mipmap = True
    tex.interpolate = True
    return tex


def fade_plane_texture(h=512):
    """Black, transparent at the top, opaque below: fades the mirror image out."""
    a = (np.linspace(0, 1, h) ** 0.7) * 255
    img = np.zeros((h, 4, 4), np.uint8)
    img[..., 3] = a.astype(np.uint8)[:, None]
    return pv.Texture(img)


def glow_texture(size=512):
    y, x = np.mgrid[-1:1:size * 1j, -1:1:size * 1j]
    r = np.clip(1 - np.sqrt(x ** 2 + (y * 1.6) ** 2), 0, 1) ** 2.2
    base = np.array([34, 40, 56])[None, None, :] * r[:, :, None]
    return pv.Texture(base.astype(np.uint8))


# --------------------------------------------------------------------------
# Build the scene
# --------------------------------------------------------------------------
def main():
    pv.global_theme.background = "black"
    pl = pv.Plotter(off_screen=True, window_size=WINDOW, lighting="none")
    pl.set_background("black")

    try:
        pl.set_environment_texture(studio_environment(), is_srgb=True)
    except Exception as exc:                     # older PyVista: still lit by the lights below
        print("Environment lighting skipped:", exc)

    # Cards: three ghosts, then the named one on top.
    specs = [("ghost", ang, i) for i, ang in enumerate(GHOST_ANGLES)]
    specs.append(("named", NAMED_ANGLE, len(GHOST_ANGLES)))

    placed = []
    for kind, angle, i in specs:
        face, body = make_card()
        extra = NAMED_LIFT if kind == "named" else (0, 0, 0)
        face = place(face, angle, i * Z_STEP, extra)
        body = place(body, angle, i * Z_STEP, extra)
        img = named_card_face() if kind == "named" else ghost_card_face(seed=10 + i, **GHOST_QUESTION[i])
        tex = pv.Texture(np.asarray(img))
        try:
            tex.SetUseSRGBColorSpace(True)
        except Exception:
            pass
        body_color = (0.93, 0.90, 0.82) if kind == "named" else (0.11, 0.13, 0.19)
        placed.append((face, body, tex, body_color, kind))

    floor_y = min(m.bounds[2] for f, b, *_ in placed for m in (f, b)) - 0.04

    for face, body, tex, body_color, kind in placed:
        for mesh, colour in ((body, body_color), (face, "white")):
            actor = pl.add_mesh(mesh, color=colour, pbr=True,
                                metallic=0.05 if kind == "ghost" else 0.0,
                                roughness=GLOSS_ROUGHNESS, smooth_shading=True,
                                split_sharp_edges=True)
            if mesh is face:
                # PyVista does not hand textures to the PBR shader; VTK wants it as base colour.
                actor.prop.SetBaseColorTexture(tex)
            try:
                actor.prop.SetCoatStrength(COAT_STRENGTH)
                actor.prop.SetCoatRoughness(0.12)
            except Exception:
                pass

        # mirror image in the glossy surface below the hand
        for mesh, kw in ((body, dict(color=body_color)), (face, dict(texture=tex))):
            mirrored = mesh.reflect((0, 1, 0), point=(0, floor_y, 0), inplace=False)
            pl.add_mesh(mirrored, opacity=REFLECTION_OPACITY, lighting=False, **kw)

    # fade the mirror image out with distance from the cards
    drop = 4.5
    fade = pv.Plane(center=(0.3, floor_y - drop / 2 + 0.6, 2.2), direction=(0, 0, 1),
                    i_size=24, j_size=drop + 1.2, i_resolution=1, j_resolution=1)
    pl.add_mesh(fade, texture=fade_plane_texture(), lighting=False)

    if BACKDROP_GLOW:
        glow = pv.Plane(center=(0.3, 1.6, -7), direction=(0, 0, 1), i_size=34, j_size=19)
        pl.add_mesh(glow, texture=glow_texture(), lighting=False)

    # lights: soft key above-left, cool rim from behind-right, faint fill
    pl.add_light(pv.Light(position=(-5, 9, 9), focal_point=(0, 1.5, 0), color="white",
                          intensity=1.35, light_type="scene light"))
    pl.add_light(pv.Light(position=(8, 5, -5), focal_point=(0, 1.5, 0), color="#9cc4ff",
                          intensity=0.6, light_type="scene light"))
    pl.add_light(pv.Light(position=(7, 10, 8), focal_point=(0, 1.5, 0), color="#ffe2c0",
                          intensity=0.45, light_type="scene light"))

    pl.camera.position = (0.0, 2.8, 12.6)
    pl.camera.focal_point = (0.35, 0.95, 0.0)
    pl.camera.up = (0, 1, 0)
    pl.camera.view_angle = 30

    pl.enable_depth_peeling(number_of_peels=8)
    try:
        pl.enable_anti_aliasing("ssaa")
    except Exception:
        pl.enable_anti_aliasing()

    pl.screenshot(str(OUT), scale=SCALE)
    print("Wrote", OUT.resolve())


if __name__ == "__main__":
    main()
