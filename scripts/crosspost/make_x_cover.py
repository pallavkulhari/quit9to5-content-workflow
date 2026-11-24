#!/usr/bin/env python3
"""Render the X Article cover for Quit 9to5 post 8 at 5:2 (3000x1200).

On-brand with the blog thumbs: grid background from t4_seven.jpg, dark-grey
house + red speech-bubble, Josefin Sans title, black then red with grey stroke.
Text names what is being quit ("Job").
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

import os
# Ported from the box (crosspost/make_post08_x_cover.py). Copy per post: change the illustration and the two lines.
# Env: BLOG_THUMB_BG (t4_seven.jpg, not in repo), X_COVER_OUT_DIR (default ./), Q9_FONT_JOSEFIN, Q9_FONT_DEJAVU_BOLD.
SRC_BG = Path(os.environ.get("BLOG_THUMB_BG", "t4_seven.jpg"))
OUT_DIR = Path(os.environ.get("X_COVER_OUT_DIR", "."))
FONT = os.environ.get("Q9_FONT_JOSEFIN", "/usr/share/fonts/truetype/sand-box/google/Josefin Sans/JosefinSans-VariableFont_wght.ttf")
LABEL_FONT = os.environ.get("Q9_FONT_DEJAVU_BOLD", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")

# Master canvas: 5:2 at 2x the commonly cited 1500x600 working size.
W, H = 3000, 1200
# Safe zone: 10% sides (also the crop if a 2:1 summary_large_image card
# cover-fits a 5:2 image), 12% top/bottom (Pilcrow habit, not an X spec).
SAFE_X, SAFE_Y = int(W * 0.10), int(H * 0.12)  # 300, 144

DG = (64, 64, 64)
RED = (204, 68, 60)
GR = (188, 188, 188)
WH = (250, 250, 250)
INK = (10, 10, 10)

LINE1 = "Quitting Your Job?"
LINE2 = "How to Tell Your Family"


def load_grid_5x2(w, h):
    """Same left-extend as the blog thumb scripts, then a centre 5:2 crop."""
    a = np.array(Image.open(SRC_BG).convert("RGB"))
    for x in range(1024, -1, -1):
        a[:, x] = a[:, x + 155]
    src = Image.fromarray(a)  # 1200x630
    # Scale by width, then centre-crop to 5:2.
    scaled = src.resize((w, int(round(src.height * w / src.width))), Image.LANCZOS)
    top = (scaled.height - h) // 2
    return scaled.crop((0, top, w, top + h))


def josefin(size):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_name("Regular")
    except Exception as e:
        print("font variation:", e)
    return f


def draw_house(d, left, top, scale):
    """Draw the post-8 house in original 1200-space units, mapped by scale.

    Original logical bbox with cx=290: left=80, top=40, right=515, bottom=472.
    """
    OL, OT = 80, 40
    cx = 290

    def X(x):
        return left + (x - OL) * scale

    def Y(y):
        return top + (y - OT) * scale

    def xy(x, y):
        return (X(x), Y(y))

    def box(x0, y0, x1, y1):
        return [X(x0), Y(y0), X(x1), Y(y1)]

    sw = max(2, round(5 * scale))  # window mullion width

    d.polygon([xy(cx - 170, 250), xy(cx + 170, 250), xy(cx, 120)], fill=DG)
    d.rectangle(box(cx - 140, 250, cx + 140, 460), fill=DG)
    d.rectangle(box(cx + 70, 150, cx + 105, 215), fill=DG)
    for wx in (cx - 110, cx + 45):
        d.rectangle(box(wx, 285, wx + 65, 345), fill=WH)
        d.line([xy(wx + 32, 285), xy(wx + 32, 345)], fill=DG, width=sw)
        d.line([xy(wx, 315), xy(wx + 65, 315)], fill=DG, width=sw)
    d.rounded_rectangle(
        box(cx - 32, 370, cx + 32, 460), radius=max(2, 6 * scale), fill=WH
    )
    d.rectangle(box(cx - 210, 460, cx + 210, 472), fill=DG)
    # Speech bubble
    bx0, by0, bx1, by1 = cx + 95, 40, cx + 225, 120
    d.rounded_rectangle(box(bx0, by0, bx1, by1), radius=max(4, 22 * scale), fill=RED)
    d.polygon(
        [xy(bx0 + 25, by1 - 2), xy(bx0 + 60, by1 - 2), xy(bx0 + 5, by1 + 40)],
        fill=RED,
    )
    for i in range(3):
        x = bx0 + 35 + i * 30
        d.ellipse(box(x - 8, 72, x + 8, 88), fill=WH)

    return (X(515), Y(472))  # right, bottom of original bbox


def render_cover(debug=False):
    img = load_grid_5x2(W, H)
    d = ImageDraw.Draw(img)

    # House: ~560px wide so the long second line still fits in the 10% side margin.
    # Original bbox width 435, height 432.
    house_w = 480
    scale = house_w / 435.0
    house_h = 432 * scale
    house_left = SAFE_X + 40  # 340, a little inset from the 10% line
    house_top = (H - house_h) / 2
    house_right, house_bottom = draw_house(d, house_left, house_top, scale)

    # Type: two lines, vertically centred as a block, starting after the house.
    font_size = 160
    stroke = 10
    font = josefin(font_size)
    gap_after_house = 70
    text_x = int(round(house_right + gap_after_house))
    line_gap = 24

    b1 = d.textbbox((0, 0), LINE1, font=font, stroke_width=stroke)
    b2 = d.textbbox((0, 0), LINE2, font=font, stroke_width=stroke)
    w1, h1 = b1[2] - b1[0], b1[3] - b1[1]
    w2, h2 = b2[2] - b2[0], b2[3] - b2[1]
    block_h = h1 + line_gap + h2
    # textbbox y-origin includes ascent; place so the ink block is centred.
    text_y = int(round((H - block_h) / 2 - b1[1]))
    y2 = text_y + h1 + line_gap

    d.text((text_x, text_y), LINE1, font=font, fill=INK, stroke_width=stroke, stroke_fill=GR)
    d.text((text_x, y2), LINE2, font=font, fill=RED, stroke_width=stroke, stroke_fill=GR)

    # Reported boxes (ink, including stroke)
    box1 = d.textbbox((text_x, text_y), LINE1, font=font, stroke_width=stroke)
    box2 = d.textbbox((text_x, y2), LINE2, font=font, stroke_width=stroke)
    print(f"canvas {W}x{H}")
    print(f"house  L={house_left:.1f} T={house_top:.1f} R={house_right:.1f} B={house_bottom:.1f} scale={scale:.3f}")
    print(f"line1  {box1}  w={box1[2]-box1[0]}  inside_safe={box1[0]>=SAFE_X and box1[2]<=W-SAFE_X and box1[1]>=SAFE_Y and box1[3]<=H-SAFE_Y}")
    print(f"line2  {box2}  w={box2[2]-box2[0]}  inside_safe={box2[0]>=SAFE_X and box2[2]<=W-SAFE_X and box2[1]>=SAFE_Y and box2[3]<=H-SAFE_Y}")
    print(f"safe   x={SAFE_X}..{W-SAFE_X}  y={SAFE_Y}..{H-SAFE_Y}")

    if debug:
        # Safe zone (green) and 2:1 card crop (blue).
        d.rectangle([SAFE_X, SAFE_Y, W - SAFE_X, H - SAFE_Y], outline=(40, 160, 80), width=4)
        crop_x = int((W - H * 2) / 2)  # 2:1 centre crop
        d.rectangle([crop_x, 0, W - crop_x, H - 1], outline=(40, 90, 200), width=4)

    return img


def crop_2x1(im):
    """Centre crop 5:2 -> 2:1 (sides off). 3000x1200 -> 2400x1200."""
    w, h = im.size
    new_w = int(h * 2)
    x0 = (w - new_w) // 2
    return im.crop((x0, 0, x0 + new_w, h))


def make_preview(cover):
    """Contact sheet: full 5:2, possible 2:1 card crop, and a phone-width 5:2."""
    pad = 48
    label_h = 56
    # Phone column is ~390–696px for the article; show 780x312 (2x a 390px phone).
    phone = cover.resize((780, 312), Image.LANCZOS)
    card = crop_2x1(cover).resize((1500, 750), Image.LANCZOS)
    header = cover.resize((1500, 600), Image.LANCZOS)

    width = pad * 2 + 1500
    blocks = [
        ("Article page header — 5:2, as X stores and displays the cover (object-cover, aspect-5/2)", header),
        ("Possible timeline / link card — 2:1 centre crop (twitter:card = summary_large_image)", card),
        ("Mobile article header — 5:2 at ~390px wide, shown at 2x (780x312)", phone),
    ]
    height = pad
    for _, im in blocks:
        height += label_h + im.height + pad

    sheet = Image.new("RGB", (width, height), (245, 245, 245))
    d = ImageDraw.Draw(sheet)
    font = ImageFont.truetype(LABEL_FONT, 28)
    small = ImageFont.truetype(LABEL_FONT, 20)
    y = pad
    title = "Post 8 X Article cover — crop preview"
    d.text((pad, y - 8), title, font=font, fill=(20, 20, 20))
    # actually put title above first label; redo layout with a title row
    # Simpler: the first label is enough. Leave as is if title overlaps — we'll add a title band.
    # Rebuild with title band for clarity.
    return _preview_with_title(cover, phone, card, header, pad, label_h, width)


def _preview_with_title(cover, phone, card, header, pad, label_h, width):
    font = ImageFont.truetype(LABEL_FONT, 32)
    small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    title_h = 100
    blocks = [
        ("1. Article page header (5:2). X stores and displays the cover at aspect-5/2, object-cover.", header),
        ("2. Possible timeline / link card (2:1 centre crop). twitter:card=summary_large_image may trim 10% from each side.", card),
        ("3. Mobile article header (same 5:2, ~390px wide, shown at 2x to judge type size).", phone),
    ]
    height = title_h + pad
    for _, im in blocks:
        height += label_h + im.height + pad
    sheet = Image.new("RGB", (width, height), (245, 245, 245))
    d = ImageDraw.Draw(sheet)
    d.rectangle([0, 0, width, title_h - 16], fill=(30, 30, 30))
    d.text((pad, 28), "Post 8 X Article cover — crop preview", font=font, fill=(255, 255, 255))
    y = title_h
    for label, im in blocks:
        d.text((pad, y), label, font=small, fill=(30, 30, 30))
        y += label_h
        # centre narrower phone image on the 1500-wide column
        x = pad + (1500 - im.width) // 2
        # white frame
        sheet.paste((255, 255, 255), [x - 4, y - 4, x + im.width + 4, y + im.height + 4])
        sheet.paste(im, (x, y))
        y += im.height + pad
    return sheet


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cover = render_cover(debug=False)
    png_path = OUT_DIR / "post08_x_cover.png"
    jpg_path = OUT_DIR / "post08_x_cover.jpg"
    preview_path = OUT_DIR / "post08_x_cover_preview.jpg"
    debug_path = OUT_DIR / "post08_x_cover_safezone.png"

    cover.save(png_path)
    # High-quality JPEG, 4:4:4-ish via quality/subsampling for sharper type.
    cover.save(jpg_path, quality=92, subsampling=0, optimize=True)

    debug = render_cover(debug=True)
    debug.save(debug_path)

    preview = make_preview(cover)
    preview.save(preview_path, quality=90, optimize=True)

    for p in (png_path, jpg_path, preview_path, debug_path):
        print(f"wrote {p}  {p.stat().st_size} bytes  ", end="")
        im = Image.open(p)
        print(f"{im.size[0]}x{im.size[1]} {im.format}")


if __name__ == "__main__":
    main()
