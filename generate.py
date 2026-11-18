#!/usr/bin/env python3
"""Render entry.png for make.fun news-image-20261118.

A clean, typographic infographic summing up the world news of
Wednesday 18 November 2026. Six stories, two columns x three rows,
rendered with PIL only. No AI image generation: every glyph is
crisp vector type.

Run: python3 generate.py   (writes entry.png next to this file)
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1024, 1024

# --- palette -------------------------------------------------------------
NAVY = (15, 36, 64)          # header band, headlines
NAVY_LIGHT = (31, 78, 121)
GOLD = (232, 184, 75)        # header accent
PAPER = (244, 241, 234)      # page background
CARD = (255, 255, 255)       # story card background
CARD_BORDER = (216, 210, 195)
INK = (51, 51, 51)           # body text
MUTED = (110, 110, 105)      # footer text
WHITE = (255, 255, 255)

# --- fonts ---------------------------------------------------------------
FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, max_width):
    """Wrap text to lines that each fit max_width pixels."""
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, max_width, max_lines):
    """Wrap text; if it needs more than max_lines, shrink the font."""
    size = fnt.size
    while size > 14:
        f = font(fnt.path, size) if hasattr(fnt, "path") else fnt
        # truetype fonts keep their path on .path in Pillow
        try:
            f = ImageFont.truetype(fnt.path, size)
        except Exception:
            f = fnt
        lines = wrap_text(draw, text, f, max_width)
        if len(lines) <= max_lines:
            return f, lines
        size -= 1
    lines = wrap_text(draw, text, f, max_width)
    return f, lines[:max_lines]


# --- stories -------------------------------------------------------------
# Every story was verified against reporting dated 18 November 2026
# (Reuters, AP, AFP, The Japan Times, NDTV, Times Now).
STORIES = [
    {
        "tag": "MIDDLE EAST",
        "color": (169, 50, 38),
        "headline": "U.S. sinks five Iranian tankers",
        "body": "U.S. forces sank five Iranian oil tankers in the Gulf of "
                "Oman overnight; Iran says it struck ships near Hormuz and "
                "fired missiles at a U.S. base in Jordan.",
    },
    {
        "tag": "DIPLOMACY",
        "color": (31, 78, 121),
        "headline": "Trump, Xi and Putin to meet in Shenzhen",
        "body": "Putin landed in Shenzhen today and meets Xi now; Trump "
                "flies in for a three-way summit tomorrow \u2014 their first.",
    },
    {
        "tag": "HEALTH",
        "color": (14, 124, 123),
        "headline": "U.S. loses measles-free status",
        "body": "Health officials confirm more than 5,400 measles cases "
                "this year \u2014 the worst U.S. outbreak in over three decades.",
    },
    {
        "tag": "EUROPE",
        "color": (108, 52, 131),
        "headline": "Ukraine hits Crimea bridge again",
        "body": "Kyiv says a strike partly destroyed the bridge to Crimea "
                "for a second night running; Russia hit Ukrainian bridges "
                "in reply.",
    },
    {
        "tag": "CLIMATE",
        "color": (30, 132, 73),
        "headline": "COP31 talks enter final days",
        "body": "Negotiators in Antalya are stuck on 144 disputed items as "
                "the climate summit nears its Friday deadline.",
    },
    {
        "tag": "ASIA-PACIFIC",
        "color": (154, 125, 10),
        "headline": "Two earthquakes strike in one day",
        "body": "A magnitude 6.0 quake hit Papua New Guinea and a 5.9 quake "
                "hit Indonesia\u2019s Flores island, seismologists say.",
    },
]


def draw_header(draw):
    draw.rectangle([0, 0, W, 160], fill=NAVY)
    # thin gold rule at the bottom of the header
    draw.rectangle([0, 160, W, 164], fill=GOLD)

    # kicker
    kicker = font(FONT_BOLD, 26)
    draw.text((W // 2, 26), "THE WORLD TODAY", font=kicker,
              fill=GOLD, anchor="ma")

    # date: the single most important line, auto-fit to the width
    date_text = "WEDNESDAY 18 NOVEMBER 2026"
    size = 58
    while size > 30:
        f = font(FONT_BOLD, size)
        if draw.textlength(date_text, font=f) <= W - 64:
            break
        size -= 2
    draw.text((W // 2, 56), date_text, font=f, fill=WHITE, anchor="ma")

    # subline
    sub = font(FONT_REG, 26)
    draw.text((W // 2, 122), "Six stories from around the globe",
              font=sub, fill=(200, 210, 222), anchor="ma")


def draw_card(draw, x, y, w, h, story):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=CARD_BORDER,
                   width=2)
    # coloured top bar
    draw.rectangle([x + 2, y + 2, x + w - 2, y + 10], fill=story["color"])

    pad = 20
    cx = x + pad
    cw = w - 2 * pad
    cy = y + 24

    # tag chip
    tag_font = font(FONT_BOLD, 21)
    tag_text = story["tag"]
    tw = draw.textlength(tag_text, font=tag_font)
    chip_w = int(tw) + 24
    chip_h = 32
    draw.rounded_rectangle([cx, cy, cx + chip_w, cy + chip_h],
                           radius=6, fill=story["color"])
    draw.text((cx + 12, cy + 5), tag_text, font=tag_font, fill=WHITE)
    cy += chip_h + 12

    # headline, at most 2 lines
    head_font, head_lines = fit_lines(
        draw, story["headline"], font(FONT_BOLD, 31), cw, 2)
    for line in head_lines:
        draw.text((cx, cy), line, font=head_font, fill=NAVY)
        cy += head_font.size + 6
    cy += 4

    # body, at most 3 lines
    body_font, body_lines = fit_lines(
        draw, story["body"], font(FONT_REG, 25), cw, 3)
    for line in body_lines:
        draw.text((cx, cy), line, font=body_font, fill=INK)
        cy += body_font.size + 6


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    draw_header(draw)

    # grid: 2 columns x 3 rows
    margin = 32
    gutter_x = 20
    gutter_y = 18
    grid_top = 184
    grid_bottom = 984
    card_w = (W - 2 * margin - gutter_x) // 2
    card_h = (grid_bottom - grid_top - 2 * gutter_y) // 3

    for i, story in enumerate(STORIES):
        row, col = divmod(i, 2)
        x = margin + col * (card_w + gutter_x)
        y = grid_top + row * (card_h + gutter_y)
        draw_card(draw, x, y, card_w, card_h, story)

    # footer
    foot = font(FONT_REG, 20)
    draw.text((W // 2, 1000),
              "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 The Japan Times "
              "\u00b7 NDTV \u00b7 18 November 2026",
              font=foot, fill=MUTED, anchor="ma")

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
