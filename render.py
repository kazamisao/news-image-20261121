"""Rendering module for the one-page broadsheet poster.

Draws a deterministic 1024x1024 newspaper front page with Pillow.
Every coordinate, colour and string is fixed in this file so that
repeated runs produce exactly the same PNG bytes.
"""

from PIL import Image, ImageDraw, ImageFont

# Canvas and palette — square poster, warm paper tone, near-black ink
WIDTH = 1024
HEIGHT = 1024
PAPER = (250, 247, 238)
INK = (18, 18, 18)
MUTED = (70, 70, 70)
RULE = (18, 18, 18)
LIGHT_RULE = (140, 140, 140)

MARGIN = 48
CONTENT_W = WIDTH - 2 * MARGIN


def _font(size, bold=False, serif=True):
    """Return a font, preferring a serif face for the broadsheet look."""
    candidates = []
    if serif:
        if bold:
            candidates = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
            ]
        else:
            candidates = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
            ]
    else:
        if bold:
            candidates = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            ]
        else:
            candidates = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def _wrap(draw, text, font, max_width):
    """Wrap text to a list of lines that fit max_width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        bbox = draw.textbbox((0, 0), trial, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _draw_wrapped(draw, x, y, text, font, max_width, line_gap=4, fill=INK):
    lines = _wrap(draw, text, font, max_width)
    _, top, _, bottom = draw.textbbox((0, 0), "Ag", font=font)
    line_h = (bottom - top) + line_gap
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += line_h
    return y


def _rule(draw, y, weight=3, colour=RULE):
    draw.line([(MARGIN, y), (WIDTH - MARGIN, y)], fill=colour, width=weight)
    return y + weight


def render(path="news.png"):
    img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(img)

    # Outer border
    draw.rectangle([18, 18, WIDTH - 19, HEIGHT - 19], outline=INK, width=2)
    draw.rectangle([24, 24, WIDTH - 25, HEIGHT - 25], outline=INK, width=1)

    y = 40

    # Top line: edition note and price-style tag
    small = _font(13, serif=False)
    draw.text((MARGIN, y), "MORNING EDITION  -  ONE PAGE, THE WHOLE DAY", font=small, fill=MUTED)
    tag = "No. 21-11"
    tb = draw.textbbox((0, 0), tag, font=small)
    draw.text((WIDTH - MARGIN - (tb[2] - tb[0]), y), tag, font=small, fill=MUTED)
    y += 22
    y = _rule(draw, y, weight=1, colour=LIGHT_RULE) + 10

    # Masthead
    masthead_font = _font(54, bold=True, serif=True)
    title = "THE WORLD IN ONE DAY"
    tb = draw.textbbox((0, 0), title, font=masthead_font)
    tw = tb[2] - tb[0]
    draw.text(((WIDTH - tw) // 2, y), title, font=masthead_font, fill=INK)
    y += 68
    y = _rule(draw, y, weight=4) + 4
    y = _rule(draw, y, weight=1) + 10

    # Dateline bar
    dateline_font = _font(17, bold=True, serif=False)
    dateline = "SATURDAY 21 NOVEMBER 2026"
    tb = draw.textbbox((0, 0), dateline, font=dateline_font)
    draw.text(((WIDTH - (tb[2] - tb[0])) // 2, y), dateline, font=dateline_font, fill=INK)
    # Side notes on the same line
    draw.text((MARGIN, y + 1), "Warsaw  -  Washington  -  Shenzhen", font=small, fill=MUTED)
    right_note = "Weather: Fair, 18 C"
    rb = draw.textbbox((0, 0), right_note, font=small)
    draw.text((WIDTH - MARGIN - (rb[2] - rb[0]), y + 1), right_note, font=small, fill=MUTED)
    y += 26
    y = _rule(draw, y, weight=2) + 14

    # Lead story — full width headline, then two columns of body
    kicker_font = _font(14, bold=True, serif=False)
    draw.text((MARGIN, y), "LEAD STORY  -  EUROPE", font=kicker_font, fill=MUTED)
    y += 22
    lead_head_font = _font(36, bold=True, serif=True)
    y = _draw_wrapped(
        draw, MARGIN, y,
        "Russian Missile Strikes Poland; Rutte Heads to Warsaw",
        lead_head_font, CONTENT_W, line_gap=4,
    ) + 6
    lead_sub_font = _font(17, serif=True)
    y = _draw_wrapped(
        draw, MARGIN, y,
        "A Russian missile struck Poland on Friday, shaking the eastern "
        "flank of the alliance. NATO Secretary General Rutte travels to "
        "Warsaw today for urgent talks with Polish leaders.",
        lead_sub_font, CONTENT_W, line_gap=5,
    ) + 6
    y = _rule(draw, y, weight=1, colour=LIGHT_RULE) + 8

    body_font = _font(14, serif=True)
    col_gap = 28
    col_w = (CONTENT_W - col_gap) // 2
    left_x = MARGIN
    right_x = MARGIN + col_w + col_gap
    lead_left = (
        "WARSAW - The strike, which landed on Friday, drew swift "
        "condemnation from capitals across Europe. Officials in Warsaw "
        "said air defences had tracked the missile before impact and "
        "that emergency services were on the scene within minutes. "
        "No government in the region was treating the incident as an "
        "accident of geography; the question in every briefing room "
        "was whether it was a warning or a mistake."
    )
    lead_right = (
        "Rutte's visit, announced overnight, is meant to show unity. "
        "He is expected to meet the Polish president and prime minister, "
        "visit the affected area, and restate the alliance commitment "
        "that an attack on one member is an attack on all. Diplomats "
        "said further air-defence deployments to the east were under "
        "active discussion as leaders gathered statements and facts."
    )
    y_left = _draw_wrapped(draw, left_x, y, lead_left, body_font, col_w, line_gap=4)
    y_right = _draw_wrapped(draw, right_x, y, lead_right, body_font, col_w, line_gap=4)
    # Vertical divider between lead columns
    draw.line([(WIDTH // 2, y), (WIDTH // 2, max(y_left, y_right))], fill=LIGHT_RULE, width=1)
    y = max(y_left, y_right) + 10
    y = _rule(draw, y, weight=3) + 12

    # Markets story — left column wide, with a figures box
    draw.text((MARGIN, y), "MARKETS", font=kicker_font, fill=MUTED)
    y += 22
    market_head_font = _font(28, bold=True, serif=True)
    y = _draw_wrapped(
        draw, MARGIN, y,
        "Wall Street Falls 3,7% as Tech Sell-Off Deepens",
        market_head_font, CONTENT_W, line_gap=4,
    ) + 6
    market_body = (
        "NEW YORK - Stocks slid sharply as investors cut exposure to "
        "technology shares. The Nasdaq fell 5,3% in its worst session "
        "in months, and Nvidia dropped 14%, dragging chipmakers and "
        "the wider market lower. Traders said the move reflected "
        "worries about stretched valuations meeting thinner liquidity, "
        "with selling broadening from megacap names into banks, "
        "industrials and consumer shares before a late, partial stabilisation."
    )
    y = _draw_wrapped(draw, MARGIN, y, market_body, body_font, CONTENT_W, line_gap=4) + 8

    # Figures strip
    box_top = y
    box_h = 52
    draw.rectangle([MARGIN, box_top, WIDTH - MARGIN, box_top + box_h], outline=INK, width=1)
    fig_font = _font(15, bold=True, serif=False)
    fig_small = _font(12, serif=False)
    figures = [
        ("WALL ST", "-3,7%"),
        ("NASDAQ", "-5,3%"),
        ("NVIDIA", "-14%"),
        ("MOOD", "RISK OFF"),
    ]
    cell_w = CONTENT_W // len(figures)
    for i, (label, value) in enumerate(figures):
        cx = MARGIN + i * cell_w + 14
        draw.text((cx, box_top + 7), label, font=fig_small, fill=MUTED)
        draw.text((cx, box_top + 24), value, font=fig_font, fill=INK)
        if i > 0:
            draw.line([(MARGIN + i * cell_w, box_top), (MARGIN + i * cell_w, box_top + box_h)],
                      fill=LIGHT_RULE, width=1)
    y = box_top + box_h + 12
    y = _rule(draw, y, weight=1, colour=LIGHT_RULE) + 10

    # Shorter items — two columns, three on the left, two on the right plus a note
    head_font = _font(17, bold=True, serif=True)
    short_body = _font(13, serif=True)

    left_items = [
        ("Shenzhen Bets Big on Technology",
         "SHENZHEN - Factories and labs in Shenzhen showed a new "
         "generation of robots, chips and consumer devices, underlining "
         "the city's push to lead the next wave of technology."),
        ("Saudi-Houthi Tensions Rise Again",
         "RIYADH - Tensions between Saudi Arabia and Houthi forces "
         "flared again, raising fears for shipping and energy routes "
         "as mediators urged both sides to step back."),
        ("New Hope in Daraxonrasib Cancer Drug",
         "LONDON - Researchers reported encouraging news for "
         "daraxonrasib, a cancer-drug candidate aimed at hard-to-treat "
         "tumours, while cautioning that larger trials still lie ahead."),
    ]
    right_items = [
        ("COP31 Climate Summit Seeks a Deal",
         "Delegates at the COP31 climate summit worked through the "
         "night on finance and emissions language, with poorer nations "
         "pressing richer ones for firmer pledges and clearer timelines."),
        ("Palisades Fire Recovery Moves Forward",
         "LOS ANGELES - Recovery after the Palisades fire entered a "
         "new phase as crews cleared lots, utilities returned street "
         "by street, and residents began planning how to rebuild."),
    ]

    def draw_items(x, items, start_y):
        cy = start_y
        for idx, (headline, text) in enumerate(items):
            cy = _draw_wrapped(draw, x, cy, headline, head_font, col_w, line_gap=3) + 2
            cy = _draw_wrapped(draw, x, cy, text, short_body, col_w, line_gap=3) + 6
            if idx < len(items) - 1:
                draw.line([(x, cy), (x + col_w, cy)], fill=LIGHT_RULE, width=1)
                cy += 8
        return cy

    y_left_end = draw_items(left_x, left_items, y)
    y_right_end = draw_items(right_x, right_items, y)
    draw.line([(WIDTH // 2, y), (WIDTH // 2, max(y_left_end, y_right_end))],
              fill=LIGHT_RULE, width=1)
    y = max(y_left_end, y_right_end) + 8

    # Footer
    if y < HEIGHT - 70:
        y = HEIGHT - 70
    y = _rule(draw, y, weight=2) + 8
    footer_font = _font(12, serif=False)
    footer = "THE WORLD IN ONE DAY  -  All stories summarised for a single page  -  Printed deterministically, no randomness"
    fb = draw.textbbox((0, 0), footer, font=footer_font)
    draw.text(((WIDTH - (fb[2] - fb[0])) // 2, y), footer, font=footer_font, fill=MUTED)

    img.save(path, format="PNG")
    return path
