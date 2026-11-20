#!/usr/bin/env python3
"""Draw the World News image for Friday 20 November 2026.

A flat, newspaper-style infographic, 1024x1024, drawn entirely with Pillow
primitives and DejaVu fonts. Six verified stories from 20 November 2026
plus a footer ticker. Run: python3 tools/draw.py  (writes entry.png).
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PAPER = (246, 241, 231)
INK = (27, 27, 27)
MUTED = (96, 96, 96)
NAVY = (18, 40, 75)
RED = (179, 39, 30)
WHITE = (255, 255, 255)
BORDER = (214, 208, 194)
GREEN = (14, 107, 74)
TEAL = (15, 106, 120)
GOLD = (150, 108, 8)
SKY = (216, 231, 242)
RIVER = (127, 168, 201)
SUN = (232, 178, 62)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_BOLD = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill, leading):
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def tag_chip(d, x, y, label, color):
    fnt = SANS_BOLD(15)
    tw = fnt.getlength(label)
    pad_x, h = 10, 24
    d.rounded_rectangle([x, y, x + tw + pad_x * 2, y + h], radius=4, fill=color)
    d.text((x + pad_x, y + 4), label, font=fnt, fill=WHITE)
    return tw + pad_x * 2


# ---------------------------------------------------------------- icons
def icon_bridge(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    d.ellipse([x1 - 52, y0 + 14, x1 - 16, y0 + 50], fill=SUN)
    # river
    d.rectangle([x0, y1 - 34, x1, y1], fill=RIVER)
    d.line([(x0, y1 - 34), (x1, y1 - 34)], fill=(255, 255, 255), width=2)
    # towers
    deck_y = y1 - 52
    for tx in (x0 + 52, x1 - 66):
        d.rectangle([tx, y0 + 58, tx + 14, deck_y], fill=NAVY)
    # deck
    d.rectangle([x0 + 8, deck_y, x1 - 8, deck_y + 8], fill=INK)
    # cables
    for tx in (x0 + 59, x1 - 59):
        d.line([(tx, y0 + 58), (x0 + 30, deck_y)], fill=NAVY, width=2)
        d.line([(tx, y0 + 58), (x1 - 30, deck_y)], fill=NAVY, width=2)
    # smoke puffs
    for cx, cy, r in ((x0 + 120, y0 + 78, 12), (x0 + 142, y0 + 66, 15),
                      (x0 + 162, y0 + 82, 10)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 120))
    # small red flash on the deck
    d.polygon([(x0 + 210, deck_y - 16), (x0 + 218, deck_y - 2),
               (x0 + 226, deck_y - 16), (x0 + 222, deck_y - 2),
               (x0 + 232, deck_y - 6), (x0 + 220, deck_y + 2),
               (x0 + 224, deck_y + 12), (x0 + 214, deck_y + 2),
               (x0 + 204, deck_y + 8), (x0 + 212, deck_y - 2)],
              fill=(232, 120, 30))


def icon_tower(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    tx = x0 + (x1 - x0) // 2 - 14
    d.rectangle([tx, y0 + 26, tx + 28, y1 - 6], fill=NAVY)
    for wy in (y0 + 36, y0 + 52, y0 + 68):
        d.rectangle([tx + 5, wy, tx + 11, wy + 8], fill=(255, 214, 90))
        d.rectangle([tx + 17, wy, tx + 23, wy + 8], fill=(255, 214, 90))
    d.polygon([(tx + 14, y0 + 6), (tx + 20, y0 + 18), (tx + 30, y0 + 14),
               (tx + 22, y0 + 24), (tx + 26, y0 + 34), (tx + 14, y0 + 28),
               (tx + 2, y0 + 34), (tx + 6, y0 + 24), (tx - 2, y0 + 14),
               (tx + 8, y0 + 18)], fill=(232, 120, 30))


def icon_crowd(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(233, 228, 216))
    heads = [(x0 + 18, y0 + 58), (x0 + 42, y0 + 48), (x0 + 66, y0 + 58),
             (x0 + 30, y0 + 76), (x0 + 54, y0 + 76)]
    cols = [NAVY, RED, TEAL, GREEN, NAVY]
    for (cx, cy), c in zip(heads, cols):
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=c)
        d.rectangle([cx - 11, cy + 9, cx + 11, y1 - 6], fill=c)
    d.rectangle([x0 + 8, y0 + 12, x0 + 46, y0 + 30], fill=RED)
    d.line([(x0 + 26, y0 + 30), (x0 + 26, y0 + 44)], fill=INK, width=3)
    d.rectangle([x0 + 58, y0 + 16, x0 + 92, y0 + 32], fill=NAVY)
    d.line([(x0 + 74, y0 + 32), (x0 + 74, y0 + 46)], fill=INK, width=3)


def icon_chart(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(233, 228, 216))
    bars = [(x0 + 12, 34), (x0 + 34, 52), (x0 + 56, 74)]
    for bx, bh in bars:
        d.rectangle([bx, y1 - 14 - bh, bx + 16, y1 - 14], fill=GREEN)
    d.line([(x0 + 8, y1 - 14), (x1 - 6, y1 - 14)], fill=INK, width=2)
    d.line([(x0 + 8, y1 - 14), (x0 + 8, y0 + 10)], fill=INK, width=2)
    d.line([(x0 + 16, y1 - 46), (x0 + 40, y1 - 62), (x0 + 64, y1 - 84)],
           fill=RED, width=3)
    d.polygon([(x0 + 64, y1 - 84), (x0 + 56, y1 - 80), (x0 + 62, y1 - 72)],
              fill=RED)


def icon_ball(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(233, 228, 216))
    cx, cy, r = (x0 + x1) // 2, (y0 + y1) // 2, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE,
              outline=INK, width=2)
    d.arc([cx - r + 8, cy - r + 2, cx + 4, cy + r - 2], 300, 60, fill=RED,
          width=3)
    d.arc([cx - 4, cy - r + 2, cx + r - 8, cy + r - 2], 120, 240, fill=RED,
          width=3)
    for t in range(5):
        a = 300 + t * 12
        d.line([(cx - r + 22, cy - r + 14 + t * 12),
                (cx - r + 30, cy - r + 14 + t * 12)], fill=RED, width=2)
        d.line([(cx + r - 30, cy - r + 16 + t * 12),
                (cx + r - 22, cy - r + 16 + t * 12)], fill=RED, width=2)


def icon_cross(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(233, 228, 216))
    cx, cy, r = (x0 + x1) // 2, (y0 + y1) // 2, 32
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TEAL)
    d.rectangle([cx - 8, cy - 20, cx + 8, cy + 20], fill=WHITE)
    d.rectangle([cx - 20, cy - 8, cx + 20, cy + 8], fill=WHITE)


# ---------------------------------------------------------------- layout
def story_panel(d, x0, y0, x1, y1, accent, tag, headline, body, icon,
                head_size, body_size, max_head_lines, max_body_lines):
    d.rectangle([x0, y0, x1, y1], fill=WHITE, outline=BORDER, width=1)
    d.rectangle([x0, y0, x1, y0 + 5], fill=accent)
    ix0, iy0, ix1, iy1 = icon
    pad = 24
    text_w = ix0 - x0 - pad - 16 if icon else x1 - x0 - pad * 2
    y = y0 + 16
    tag_chip(d, x0 + pad, y, tag, accent)
    y += 34
    head_lines = wrap(headline, SANS_BOLD(head_size), text_w)[:max_head_lines]
    y = text_block(d, x0 + pad, y, head_lines, SANS_BOLD(head_size), INK,
                   int(head_size * 1.16))
    y += 6
    body_lines = wrap(body, SANS(body_size), text_w)[:max_body_lines]
    text_block(d, x0 + pad, y, body_lines, SANS(body_size), (64, 64, 64),
               int(body_size * 1.38))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.text((30, 24), "WORLD NEWS", font=SERIF_BOLD(48), fill=WHITE)
    d.text((30, 76), "THE DAY IN ONE IMAGE", font=SANS_BOLD(15),
           fill=(170, 190, 220))
    date_fnt = SANS_BOLD(30)
    d.text((994 - date_fnt.getlength("20 NOVEMBER 2026"), 22),
           "20 NOVEMBER 2026", font=date_fnt, fill=WHITE)
    d.text((994 - SANS_BOLD(16).getlength("FRIDAY"), 58), "FRIDAY",
           font=SANS_BOLD(16), fill=(232, 178, 62))
    d.rectangle([0, 104, W, 110], fill=RED)

    # ---- lead story: Kyiv bridges
    lx0, ly0, lx1, ly1 = 24, 122, 1000, 350
    d.rectangle([lx0, ly0, lx1, ly1], fill=WHITE, outline=BORDER, width=1)
    d.rectangle([lx0, ly0, lx0 + 6, ly1], fill=RED)
    tag_chip(d, lx0 + 28, ly0 + 16, "UKRAINE · CONFLICT", RED)
    head = wrap("Russia hits Kyiv's bridges in overnight raids",
                SANS_BOLD(33), 580)
    y = text_block(d, lx0 + 28, ly0 + 52, head, SANS_BOLD(33), INK, 38)
    body = wrap("Cruise and ballistic missiles struck the Northern, "
                "Podilsky, Southern and Paton bridges over the Dnipro; "
                "traffic was blocked on the two main crossings.",
                SANS(19), 580)
    text_block(d, lx0 + 28, y + 8, body, SANS(19), (64, 64, 64), 26)
    icon_bridge(d, 664, 138, 976, 334)

    # ---- middle row
    story_panel(d, 24, 362, 506, 580, RED, "MIDDLE EAST · CONFLICT",
                "Houthis claim four new strikes on Saudi targets",
                "The Yemeni group said it hit four Saudi targets and "
                "warned foreign investors to leave the kingdom.",
                (392, 378, 490, 476), 24, 17, 3, 3)
    icon_tower(d, 392, 378, 490, 476)
    story_panel(d, 518, 362, 1000, 580, NAVY, "JAPAN · POLITICS",
                "13,000 march in Tokyo against Takaichi",
                "Thousands protested in the Japanese capital against "
                "the policies of Prime Minister Sanae Takaichi.",
                (886, 378, 984, 476), 24, 17, 3, 3)
    icon_crowd(d, 886, 378, 984, 476)

    # ---- bottom row
    story_panel(d, 24, 592, 348, 830, GREEN, "JAPAN · ECONOMY",
                "Japan core inflation hits 2026 high",
                "October core prices rose 2.2%, pressing the Bank of "
                "Japan toward a December hike.",
                (248, 608, 332, 692), 21, 15, 4, 4)
    icon_chart(d, 248, 608, 332, 692)
    story_panel(d, 356, 592, 680, 830, NAVY, "UNITED STATES",
                "Trump pardons Pete Rose, posthumously",
                "The president pardoned the late baseball star, apart "
                "from any Hall of Fame call.",
                (580, 608, 664, 692), 21, 15, 4, 4)
    icon_ball(d, 580, 608, 664, 692)
    story_panel(d, 688, 592, 1000, 830, TEAL, "AFRICA · HEALTH",
                "WHO: DR Congo Ebola still an emergency",
                "Tedros said 400–500 new cases are reported each week "
                "as the outbreak spreads.",
                (900, 608, 984, 692), 21, 15, 4, 4)
    icon_cross(d, 900, 608, 984, 692)

    # ---- ticker
    d.rectangle([0, 842, W, 906], fill=NAVY)
    tick = ("ALSO TODAY  •  California probes Nvidia over China chip risks  "
            "•  ECB warns AI valuations are vulnerable  •  South Korea and "
            "China agree to ease cultural-content barriers")
    tick_lines = wrap(tick, SANS_BOLD(17), 960)
    ty = 842 + (64 - len(tick_lines) * 22) // 2
    for line in tick_lines:
        d.text(((W - SANS_BOLD(17).getlength(line)) // 2, ty), line,
               font=SANS_BOLD(17), fill=WHITE)
        ty += 22

    # ---- footer
    d.text((24, 924), "World News — Friday 20 November 2026 · All six "
           "stories were reported on 20 November 2026.",
           font=SANS(16), fill=INK)
    d.text((24, 950), "Compiled from wire reports and newsrooms. "
           "Drawn by code; no photographs.",
           font=SANS(14), fill=MUTED)

    out = os.path.join(ROOT, "entry.png")
    img.save(out, "PNG")
    print(f"wrote {out} {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
