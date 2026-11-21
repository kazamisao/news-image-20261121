"""Draw the news poster for Saturday 21 November 2026.

Build-time renderer (Pillow, run on this machine only). The graded
program is main.py, which ships the finished PNG untouched.

Layout: newspaper front page. Masthead names the day; the hero is
NATO chief Mark Rutte flying to Warsaw on Saturday 21 November, the
day's one genuinely new event, after Russian missiles fell on Polish
soil on Friday; the right column carries Friday's Wall Street rout
and the Shenzhen summit's thin result; four cards below cover the
Saudi-Houthi exchange, the daraxonrasib cancer-pill trial, COP31 and
the Palisades fire verdict; the footer strip carries four more stories
first reported on 21 November. Everything is drawn in code -- no
photographs. Dates are honest: Friday's events are labelled Friday.

Deterministic: fixed seed, no timestamps, no network.
"""

import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SS = 3                      # supersample factor
W = H = 1024 * SS
OUT = os.path.join(HERE, "news.png")

ANTON = "/home/hatch/workspace/makefun/fonts/Anton-Regular.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (246, 241, 227)
INK = (22, 19, 14)
NAVY = (20, 38, 63)
NAVY2 = (16, 30, 50)
SEA = (28, 52, 84)
LAND_A = (74, 104, 138)
LAND_B = (58, 88, 120)
TEAL = (14, 124, 123)
TEAL_LT = (120, 200, 198)
ORANGE = (232, 89, 12)
GOLD = (201, 162, 39)
RED = (180, 35, 24)
RED_DK = (128, 22, 14)
CREAM = (252, 248, 236)
WHITE = (255, 255, 255)
MUTED = (90, 84, 70)

rng = random.Random(20261121)


def font(path, size):
    return ImageFont.truetype(path, int(size * SS))


def text(draw, xy, s, fnt, fill, anchor="la"):
    draw.text((xy[0] * SS, xy[1] * SS), s, font=fnt, fill=fill, anchor=anchor)


def wrap(draw, s, fnt, max_w):
    """Greedy word wrap; max_w in final px. Returns list of lines."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w * SS:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, s, fnt, fill, max_w, leading):
    """Draw wrapped paragraph, return y after last line (final px)."""
    for line in wrap(draw, s, fnt, max_w):
        text(draw, (x, y), line, fnt, fill)
        y += leading
    return y


def fit(draw, s, fnt_path, size, max_w, min_size=10):
    """Shrink font until the string fits max_w (final px)."""
    while size > min_size:
        fnt = font(fnt_path, size)
        if draw.textlength(s, font=fnt) <= max_w * SS:
            return fnt
        size -= 1
    return font(fnt_path, min_size)


def dashed_line(draw, p0, p1, fill, width, dash=10, gap=7):
    """Straight dashed line between two points (final px)."""
    import math
    x0, y0 = p0
    x1, y1 = p1
    length = math.hypot(x1 - x0, y1 - y0)
    if length == 0:
        return
    ux, uy = (x1 - x0) / length, (y1 - y0) / length
    d = 0.0
    while d < length:
        e = min(d + dash, length)
        draw.line([(x0 + ux * d) * SS, (y0 + uy * d) * SS,
                   (x0 + ux * e) * SS, (y0 + uy * e) * SS],
                  fill=fill, width=max(1, int(width * SS)))
        d = e + gap


def star(draw, cx, cy, r, fill):
    """Five-point star centred at (cx, cy), final px."""
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append(((cx + rr * math.cos(ang)) * SS,
                    (cy + rr * math.sin(ang)) * SS))
    draw.polygon(pts, fill=fill)


# ---------------------------------------------------------------- icons
def draw_rocket(draw, cx, cy, s, color):
    """Small rocket, nose up, with a flame."""
    w = max(2, int(3 * SS))
    draw.polygon([(cx - 0.16 * s, cy - 0.10 * s),
                  (cx + 0.16 * s, cy - 0.10 * s),
                  (cx, cy - 0.52 * s)], fill=color)
    draw.rounded_rectangle([cx - 0.16 * s, cy - 0.12 * s,
                            cx + 0.16 * s, cy + 0.28 * s],
                           radius=int(0.08 * s), fill=color)
    draw.polygon([(cx - 0.16 * s, cy + 0.10 * s),
                  (cx - 0.34 * s, cy + 0.34 * s),
                  (cx - 0.16 * s, cy + 0.28 * s)], fill=color)
    draw.polygon([(cx + 0.16 * s, cy + 0.10 * s),
                  (cx + 0.34 * s, cy + 0.34 * s),
                  (cx + 0.16 * s, cy + 0.28 * s)], fill=color)
    draw.polygon([(cx - 0.10 * s, cy + 0.28 * s),
                  (cx + 0.10 * s, cy + 0.28 * s),
                  (cx, cy + 0.58 * s)], fill=GOLD)
    draw.ellipse([cx - 0.07 * s, cy - 0.28 * s, cx + 0.07 * s,
                  cy - 0.14 * s], outline=WHITE, width=w)


def draw_pill(draw, cx, cy, s, color):
    """Capsule, tilted, half colour half white.

    cx, cy and s are already in supersampled units (like the other
    icon helpers). Built from ellipses + rectangles, not
    rounded_rectangle: Pillow 10.2's rounded_rectangle fails when the
    radius approaches half the box height (its corner rectangles
    invert), which is exactly a capsule's shape.
    """
    import math
    layer = Image.new("RGBA", (int(1.6 * s), int(1.6 * s)),
                      (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    c = 0.8 * s
    x0, x1 = c - 0.55 * s, c + 0.55 * s
    y0, y1 = c - 0.20 * s, c + 0.20 * s
    w = max(2, int(3 * SS))
    # White capsule body.
    ld.rectangle([x0 + 0.20 * s, y0, x1 - 0.20 * s, y1], fill=WHITE)
    ld.ellipse([x0, y0, x0 + 0.40 * s, y1], fill=WHITE)
    ld.ellipse([x1 - 0.40 * s, y0, x1, y1], fill=WHITE)
    # Teal left half.
    ld.rectangle([x0 + 0.20 * s, y0, c, y1], fill=color)
    ld.ellipse([x0, y0, x0 + 0.40 * s, y1], fill=color)
    ld.rectangle([x0 + 0.20 * s, y0, c, y1], fill=color)
    # Outline: end arcs + top/bottom edges.
    ld.ellipse([x0, y0, x0 + 0.40 * s, y1], outline=color, width=w)
    ld.ellipse([x1 - 0.40 * s, y0, x1, y1], outline=color, width=w)
    ld.line([x0 + 0.20 * s, y0, x1 - 0.20 * s, y0], fill=color, width=w)
    ld.line([x0 + 0.20 * s, y1, x1 - 0.20 * s, y1], fill=color, width=w)
    ld.line([c, y0, c, y1], fill=color, width=max(1, int(2 * SS)))
    layer = layer.rotate(35, resample=Image.BICUBIC, center=(c, c))
    # Paste with the layer itself as mask (base image is RGB).
    draw._image.paste(layer, (int(cx - 0.8 * s), int(cy - 0.8 * s)),
                      layer)


def draw_leaf(draw, cx, cy, s, color):
    """Simple leaf: two arcs meeting at tip and stem."""
    draw.polygon([(cx, cy - 0.55 * s),
                  (cx + 0.42 * s, cy - 0.05 * s),
                  (cx + 0.18 * s, cy + 0.45 * s),
                  (cx - 0.18 * s, cy + 0.45 * s),
                  (cx - 0.42 * s, cy - 0.05 * s)], fill=color)
    draw.line([cx * SS, (cy - 0.45 * s) * SS, cx * SS,
               (cy + 0.52 * s) * SS], fill=WHITE,
              width=max(2, int(3 * SS)))


def draw_flame(draw, cx, cy, s, color):
    """Teardrop flame with an inner tongue."""
    draw.polygon([(cx, cy - 0.55 * s),
                  (cx + 0.38 * s, cy - 0.05 * s),
                  (cx + 0.30 * s, cy + 0.38 * s),
                  (cx - 0.30 * s, cy + 0.38 * s),
                  (cx - 0.38 * s, cy - 0.05 * s)], fill=color)
    draw.polygon([(cx, cy - 0.18 * s),
                  (cx + 0.18 * s, cy + 0.12 * s),
                  (cx + 0.12 * s, cy + 0.34 * s),
                  (cx - 0.12 * s, cy + 0.34 * s),
                  (cx - 0.18 * s, cy + 0.12 * s)], fill=GOLD)


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img, "RGBA")

    # ---- masthead (0-176) -----------------------------------------
    d.rectangle([0, 0, W, 176 * SS], fill=INK)
    text(d, (512, 22), "T H E   W O R L D   I N   O N E   D A Y",
         font(BOLD, 24), GOLD, anchor="ma")
    f_date = fit(d, "SATURDAY  21 NOVEMBER 2026", ANTON, 60, 940)
    text(d, (512, 54), "SATURDAY  21 NOVEMBER 2026", f_date, WHITE,
         anchor="ma")
    d.line([28 * SS, 138 * SS, 996 * SS, 138 * SS], fill=GOLD,
           width=3 * SS)
    text(d, (512, 148), "One day's news, in one picture",
         font(REG, 18), (200, 196, 180), anchor="ma")

    # ---- hero: Rutte to Warsaw (190-548) ---------------------------
    hx, hy, hw, hh = 28, 190, 612, 358
    d.rectangle([hx * SS, hy * SS, (hx + hw) * SS, (hy + hh) * SS],
                fill=NAVY)
    # Map zone (hero-local y 0-190): stylised Poland / Ukraine diagram.
    mx, my = hx, hy
    for _ in range(46):
        x = rng.uniform(mx + 10, mx + hw - 10)
        y = rng.uniform(my + 8, my + 150)
        r = rng.uniform(0.8, 1.8)
        d.ellipse([(x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS],
                  fill=(255, 255, 255, rng.randint(40, 110)))
    poland = [(mx + 118, my + 34), (mx + 232, my + 20),
              (mx + 298, my + 44), (mx + 290, my + 112),
              (mx + 238, my + 152), (mx + 168, my + 144),
              (mx + 116, my + 98)]
    ukraine = [(mx + 298, my + 44), (mx + 428, my + 28),
               (mx + 518, my + 60), (mx + 543, my + 142),
               (mx + 478, my + 184), (mx + 378, my + 170),
               (mx + 290, my + 112)]
    d.polygon([(x * SS, y * SS) for x, y in poland], fill=LAND_A)
    d.polygon([(x * SS, y * SS) for x, y in ukraine], fill=LAND_B)
    d.polygon([((mx + 430) * SS, (my + 170) * SS),
               ((mx + 543) * SS, (my + 142) * SS),
               ((mx + 560) * SS, (my + 196) * SS),
               ((mx + 470) * SS, (my + 196) * SS)], fill=SEA)
    dashed_line(d, (mx + 296, my + 46), (mx + 288, my + 110),
                WHITE, 3)
    text(d, (mx + 150, my + 58), "POLAND", font(BOLD, 17),
         (215, 228, 240))
    text(d, (mx + 400, my + 96), "UKRAINE", font(BOLD, 17),
         (205, 218, 232))
    star(d, (mx + 196) * SS, (my + 96) * SS, 11 * SS, GOLD)
    text(d, (mx + 196, my + 112), "WARSAW", font(BOLD, 16), GOLD,
         anchor="ma")
    for ix, iy in ((mx + 276, my + 70), (mx + 290, my + 106),
                   (mx + 270, my + 138)):
        d.ellipse([(ix - 7) * SS, (iy - 7) * SS, (ix + 7) * SS,
                   (iy + 7) * SS], fill=RED, outline=WHITE,
                  width=max(2, int(3 * SS)))
        d.ellipse([(ix - 13) * SS, (iy - 13) * SS, (ix + 13) * SS,
                   (iy + 13) * SS], outline=(255, 120, 100),
                  width=max(1, int(2 * SS)))
    text(d, (mx + 16, my + 156),
         "3 IMPACT SITES IN SE POLAND — FRIDAY 20 NOV",
         font(BOLD, 15), (255, 150, 135))
    text(d, (mx + 16, my + 8), "NATO'S EASTERN FLANK",
         font(BOLD, 15), TEAL_LT)
    # Hero text block.
    d.rounded_rectangle([(hx + 16) * SS, (hy + 178) * SS,
                         (hx + 216) * SS, (hy + 208) * SS],
                        radius=8 * SS, fill=ORANGE)
    text(d, (hx + 116, hy + 185), "NATO  •  POLAND", font(BOLD, 18),
         WHITE, anchor="ma")
    f_hero = fit(d, "MISSILES ON NATO SOIL", ANTON, 54, 580)
    text(d, (hx + 16, hy + 212), "MISSILES ON NATO SOIL", f_hero,
         WHITE)
    para(d, hx + 16, hy + 272,
         "Rutte flies to Warsaw today; Tusk calls Friday's strikes "
         "a deliberate provocation.",
         font(REG, 20), (220, 228, 238), 580, 26)
    text(d, (hx + 16, hy + 322),
         "8 KILLED IN UKRAINE'S BARRAGE  •  NO ONE HURT IN POLAND",
         font(BOLD, 15), GOLD)

    # ---- right column: Wall Street (190-362) + Shenzhen (376-548) --
    rx, rw = 656, 340
    wy, wh = 190, 172
    d.rectangle([rx * SS, wy * SS, (rx + rw) * SS, (wy + wh) * SS],
                fill=RED)
    text(d, (rx + 14, wy + 10), "MARKETS  •  NEW YORK",
         font(BOLD, 15), (255, 200, 190))
    text(d, (rx + 14, wy + 30), "WALL STREET ROUT", fit(
        d, "WALL STREET ROUT", ANTON, 34, 312), WHITE)
    text(d, (rx + 14, wy + 70),
         "S&P 500 slides into correction",
         font(REG, 16), (255, 220, 210))
    for i, (num, lab) in enumerate((("−3.7%", "S&P 500"),
                                    ("−5.3%", "NASDAQ"),
                                    ("−14%", "NVIDIA"))):
        y = wy + 96 + i * 26
        text(d, (rx + 14, y), num, font(BOLD, 22), WHITE)
        text(d, (rx + 118, y + 4), lab, font(BOLD, 16),
             (255, 200, 190))
    iy, ih = 376, 172
    d.rectangle([rx * SS, iy * SS, (rx + rw) * SS, (iy + ih) * SS],
                fill=CREAM, outline=INK, width=2 * SS)
    text(d, (rx + 14, iy + 10), "CHINA  •  SHENZHEN",
         font(BOLD, 15), TEAL)
    text(d, (rx + 14, iy + 30), "SUMMIT, NO DEAL", fit(
        d, "SUMMIT, NO DEAL", ANTON, 34, 312), NAVY)
    para(d, rx + 14, iy + 74,
         "Trump is home from China after the first Trump–Xi–Putin "
         "summit — 4 points, no ceasefire.",
         font(REG, 17), INK, 312, 22)
    text(d, (rx + 14, iy + 148), "TRUMP: TALKS “STUCK IN THE MUD”",
         font(BOLD, 14), RED)

    # ---- middle row: four cards (564-828) --------------------------
    cards = [
        ("SAUDI  •  HOUTHIS", "Missiles over Riyadh",
         "Coalition intercepts 3 Houthi missiles and strikes "
         "Hodeidah port. Houthis say 41 killed in 24 hours.",
         "rocket", RED),
        ("HEALTH  •  CANCER", "A pill that stops tumours",
         "Daraxonrasib: growth halted in 90% of 61 patients in a "
         "trial shown in Barcelona on Friday.",
         "pill", TEAL),
        ("CLIMATE  •  COP31", "Fossil fuels stay in the draft",
         "COP31 negotiators drop the phase-out call; the final "
         "text may slip past the deadline.",
         "leaf", NAVY),
        ("JUSTICE  •  LOS ANGELES", "Palisades fire: guilty",
         "Jury convicts Rinderknecht, 30, over the blaze that "
         "killed 12 and destroyed 6,800 homes.",
         "flame", ORANGE),
    ]
    cx0, cy0, cw, ch, gap = 28, 564, 224, 264, 16
    for i, (tag, head, body, icon, accent) in enumerate(cards):
        x = cx0 + i * (cw + gap)
        d.rectangle([x * SS, cy0 * SS, (x + cw) * SS, (cy0 + ch) * SS],
                    fill=WHITE, outline=(200, 192, 172), width=2 * SS)
        d.rectangle([x * SS, cy0 * SS, (x + cw) * SS, (cy0 + 64) * SS],
                    fill=accent)
        icx, icy = x + cw // 2, cy0 + 32
        if icon == "rocket":
            draw_rocket(d, icx * SS, icy * SS, 26 * SS, WHITE)
        elif icon == "pill":
            draw_pill(d, icx * SS, icy * SS, 26 * SS, WHITE)
        elif icon == "leaf":
            draw_leaf(d, icx * SS, icy * SS, 26 * SS, WHITE)
        else:
            draw_flame(d, icx * SS, icy * SS, 26 * SS, WHITE)
        text(d, (x + 12, cy0 + 78), tag, font(BOLD, 14), accent)
        y = cy0 + 100
        for line in wrap(d, head, font(BOLD, 22), cw - 24):
            text(d, (x + 12, y), line, font(BOLD, 22), INK)
            y += 28
        para(d, x + 12, y + 8, body, font(REG, 16), (60, 56, 48),
             cw - 24, 21)

    # ---- footer: also today (844-996) ------------------------------
    fy = 844
    d.rectangle([28 * SS, fy * SS, 996 * SS, 996 * SS], fill=INK)
    text(d, (52, fy + 14), "ALSO TODAY", font(BOLD, 21), GOLD)
    d.line([52 * SS, (fy + 46) * SS, 972 * SS, (fy + 46) * SS],
           fill=(90, 84, 70), width=2 * SS)
    also = [
        ("ESTONIA", "Russia border to close from 1 Dec"),
        ("AUSTRIA", "Summons Russian envoy over embassy damage"),
        ("KRYVYI RIH", "2 dead, 42 hurt in overnight strike"),
        ("GOLD & BITCOIN", "Gold −4%; Bitcoin down 24% in a month"),
    ]
    ax = 52
    for tag, item in also:
        text(d, (ax, fy + 58), tag, font(BOLD, 17), GOLD)
        para(d, ax, fy + 82, item, font(REG, 16), WHITE, 205, 20)
        ax += 236
    d.line([52 * SS, (fy + 126) * SS, 972 * SS, (fy + 126) * SS],
           fill=(90, 84, 70), width=1 * SS)
    text(d, (512, fy + 134),
         "Headlines as reported on 21 November 2026  •  Drawn entirely "
         "in code — no photographs",
         font(REG, 14), (170, 164, 148), anchor="ma")

    img = img.resize((1024, 1024), Image.LANCZOS)
    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    build()
