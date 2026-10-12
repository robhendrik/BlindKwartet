"""Feature image -- a fan of four cards, one of which has just received its name.

Run from the repo root:   python post2_feature_image.py
                          (headless box: xvfb-run -a python post2_feature_image.py)
Writes:                   post2/Feature_image.png   (2576 x 1450)

PyVista renders the cards (textured rounded rectangles) with a transparent
background; the dark vignette and the reflection on the table are composed
around that render with numpy / Pillow.
"""
from pathlib import Path

import numpy as np
import pyvista as pv
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path("post1")
OUT.mkdir(parents=True, exist_ok=True)

W, H = 2576, 1450
CARD_W, CARD_H = 1.0, 1.4            # world units
TEX_W, TEX_H = 720, 1008             # texture pixels (same aspect)
RADIUS = 46                          # corner radius in texture pixels

import matplotlib
import os

# ------------------------------------------------------------------ fonts
def font(size, italic=False, bold=False):
    names = ["DejaVuSerif"]
    suffix = {(False, False): "", (True, False): "-Italic",
              (False, True): "-Bold", (True, True): "-BoldItalic"}[(italic, bold)]
    for base in (f"/usr/share/fonts/truetype/dejavu/{names[0]}.ttf", 
                 f"/usr/share/fonts/dejavu/{names[0]}.ttf", 
                 os.path.join(matplotlib.get_data_path(), "fonts", "ttf",f"{names[0]}.ttf")):
        try:
            return ImageFont.truetype(base, size)
        except OSError:
            continue
    print("Failed to load any of the specified fonts.")
    return ImageFont.load_default()


def rounded_mask(size, radius, inset=0):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle(
        (inset, inset, size[0] - 1 - inset, size[1] - 1 - inset), radius - inset, fill=255)
    return m


def vertical_gradient(size, top, bottom):
    t = np.linspace(0, 1, size[1])[:, None, None]
    arr = np.array(top)[None, None, :] * (1 - t) + np.array(bottom)[None, None, :] * t
    arr = np.repeat(arr, size[0], axis=1)
    return Image.fromarray(arr.astype(np.uint8), "RGB")


# --------------------------------------------------------------- textures
def face_down_texture():
    """Dark card back: dotted rounded border and a question mark."""
    size = (TEX_W, TEX_H)
    img = vertical_gradient(size, (27, 31, 46), (18, 21, 33)).convert("RGBA")
    d = ImageDraw.Draw(img)
    # dotted border
    inset = 52
    path = Image.new("L", size, 0)
    ImageDraw.Draw(path).rounded_rectangle(
        (inset, inset, TEX_W - 1 - inset, TEX_H - 1 - inset), 52, outline=255, width=1)
    pts = np.argwhere(np.array(path) > 0)
    # walk the outline roughly in order: sort by angle around the centre
    cx, cy = TEX_W / 2, TEX_H / 2
    ang = np.arctan2(pts[:, 0] - cy, pts[:, 1] - cx)
    pts = pts[np.argsort(ang)]
    step, acc, last = 17, 0.0, None
    for (y, x) in pts:
        if last is None or np.hypot(x - last[0], y - last[1]) >= step:
            d.ellipse((x - 3.2, y - 3.2, x + 3.2, y + 3.2), fill=(138, 154, 186, 255))
            last = (x, y)
    # question mark, upper left like a hand of cards seen from the side
    f = font(230, bold=True)
    d.text((TEX_W * 0.27, TEX_H * 0.17), "?", font=f, fill=(154, 163, 181, 255), anchor="mm")
    img.putalpha(rounded_mask(size, RADIUS))
    return img


def face_up_texture():
    """Cream card with the invented name."""
    size = (TEX_W, TEX_H)
    img = vertical_gradient(size, (176, 172, 156), (154, 148, 132)).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((38, 38, TEX_W - 39, TEX_H - 39), 34, outline=(139, 135, 120, 255), width=2)
    d.text((TEX_W / 2, TEX_H * 0.50), "Electron", font=font(134, italic=True),
           fill=(22, 26, 48, 255), anchor="mm")
    d.line((TEX_W * 0.17, TEX_H * 0.585, TEX_W * 0.83, TEX_H * 0.585), fill=(110, 108, 108, 255), width=3)
    d.text((TEX_W / 2, TEX_H * 0.635), "ELEMENTARY PARTICLES", font=font(37),
           fill=(100, 98, 100, 255), anchor="mm")
    img.putalpha(rounded_mask(size, RADIUS))
    return img


def to_texture(img):
    return pv.Texture(np.array(img))           # RGBA array


# ------------------------------------------------------------------ cards
def card_mesh(angle_deg, pivot_xy, z, centre_offset=(0.0, 0.55)):
    """A card rotated by `angle_deg` (counter-clockwise) about the fan pivot."""
    mesh = pv.Plane(center=(0, 0, 0), direction=(0, 0, 1),
                    i_size=CARD_W, j_size=CARD_H, i_resolution=1, j_resolution=1)
    mesh.texture_map_to_plane(origin=(-CARD_W / 2, -CARD_H / 2, 0),
                              point_u=(CARD_W / 2, -CARD_H / 2, 0),
                              point_v=(-CARD_W / 2, CARD_H / 2, 0), inplace=True)
    mesh.translate((centre_offset[0], centre_offset[1], 0), inplace=True)   # card centre vs pivot
    mesh.rotate_z(angle_deg, point=(0, 0, 0), inplace=True)
    mesh.translate((pivot_xy[0], pivot_xy[1], z), inplace=True)
    return mesh


back_tex, front_tex = to_texture(face_down_texture()), to_texture(face_up_texture())

cards = [   # (angle, pivot, z, texture)  back cards first, the named card on top
    (+44, (0.12, -0.17), 0.00, back_tex),
    (+28, (0.22, -0.13), 0.01, back_tex),
    (+12, (0.32, -0.10), 0.02, back_tex),
    (-18, (0.62, -0.10), 0.03, front_tex),
]

pl = pv.Plotter(off_screen=True, window_size=(W, H), lighting="none")
pl.set_background("white")
meshes = []
for angle, pivot, z, tex in cards:
    m = card_mesh(angle, pivot, z)
    meshes.append(m)
    pl.add_mesh(m, texture=tex, lighting=False, show_edges=False)
pl.enable_depth_peeling(12)

# anchor the camera on the named card: its centre sits right of and above the frame centre
fb = meshes[-1].bounds
cx = (fb[0] + fb[1]) / 2 - 0.437
cy = (fb[2] + fb[3]) / 2 - 0.185
pl.camera.parallel_projection = True
pl.camera.position = (cx, cy, 10)
pl.camera.focal_point = (cx, cy, 0)
pl.camera.up = (0, 1, 0)
pl.camera.parallel_scale = 1.30                      # half the visible height in world units

layer = pl.screenshot(transparent_background=True, return_img=True)
pl.close()
layer = np.asarray(Image.fromarray(layer).convert("RGBA").resize((W, H)), dtype=np.float32) / 255.0

# ------------------------------------------------------------- background
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
r = np.hypot((xx - W * 0.50) / (W * 0.62), (yy - H * 0.40) / (H * 0.70))
glow = np.clip(1 - r, 0, 1) ** 1.6
bg = np.zeros((H, W, 3), np.float32)
bg += np.array([3, 4, 8], np.float32)[None, None, :] / 255.0
bg += glow[..., None] * np.array([15, 19, 33], np.float32)[None, None, :] / 255.0

# --------------------------------------------------------------- compose
alpha = layer[..., 3:4]
bottom_row = int(np.max(np.nonzero(alpha[..., 0].max(axis=1) > 0.05)[0]))
mirror_y = bottom_row + 14                          # the table surface

# reflection: mirror the card layer about the table line, fade with distance
rows = np.arange(H)
src = np.clip(2 * mirror_y - rows, 0, H - 1)
refl = layer[src]
dist = np.clip(rows - mirror_y, 0, None).astype(np.float32)
fade = np.where(rows > mirror_y, 0.34 * np.exp(-dist / 150.0), 0.0)[:, None, None]
refl_alpha = refl[..., 3:4] * fade
refl_img = Image.fromarray((np.concatenate([refl[..., :3], refl_alpha], axis=2) * 255).astype(np.uint8), "RGBA")
refl_img = refl_img.filter(ImageFilter.GaussianBlur(2.2))
refl = np.asarray(refl_img, dtype=np.float32) / 255.0

out = bg * (1 - refl[..., 3:4]) + refl[..., :3] * refl[..., 3:4]
out = out * (1 - alpha) + layer[..., :3] * alpha
Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), "RGB").save(OUT / "Feature_image.png")
print("wrote", OUT / "Feature_image.png")
