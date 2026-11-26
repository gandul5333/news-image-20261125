#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news poster (1024x1024 PNG).

Fresh code written for the news-image-20261125 bounty. Pure Pillow,
system DejaVu fonts, no network, no copied artwork.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (246, 241, 229)
INK = (26, 26, 26)
RED = (163, 22, 33)
NAVY = (22, 50, 79)
NAVY_DARK = (13, 32, 54)
GOLD = (198, 142, 34)
GREY = (90, 86, 76)
LIGHT_LINE = (205, 198, 182)
CARD_BG = (255, 252, 244)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw wrapped paragraph, return y after last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_masthead(d):
    d.rectangle([20, 20, W - 20, H - 20], outline=INK, width=2)
    d.rectangle([24, 24, W - 24, H - 24], outline=LIGHT_LINE, width=1)
    title = "THE WORLD IN ONE DAY"
    f = SERIF_B(56)
    tw = d.textlength(title, font=f)
    d.text(((W - tw) / 2, 34), title, font=f, fill=INK)
    date = "WEDNESDAY 25 NOVEMBER 2026"
    f2 = SANS_B(27)
    tw2 = d.textlength(date, font=f2)
    d.text(((W - tw2) / 2, 104), date, font=f2, fill=RED)
    d.line([60, 146, W - 60, 146], fill=INK, width=3)
    d.line([60, 151, W - 60, 151], fill=INK, width=1)


def draw_lead_art(d, x0, y0, x1, y1):
    """Stylised Strait of Hormuz scene: dusk sea, two tankers, fire, mines."""
    d.rectangle([x0, y0, x1, y1], fill=NAVY_DARK)
    # dusk sky bands
    d.rectangle([x0, y0, x1, y0 + 52], fill=(58, 74, 96))
    d.rectangle([x0, y0 + 52, x1, y0 + 84], fill=(122, 74, 66))
    # low sun
    d.ellipse([x1 - 78, y0 + 18, x1 - 34, y0 + 62], fill=(232, 150, 60))
    # sea
    d.rectangle([x0, y0 + 84, x1, y1], fill=(16, 44, 66))
    for i, yy in enumerate(range(y0 + 108, y1 - 8, 26)):
        off = 14 if i % 2 else 0
        d.line([x0 + 8 + off, yy, x1 - 8 + off, yy], fill=(38, 84, 112), width=3)
    # tanker 1 (left, burning)
    hx, hy = x0 + 14, y1 - 66
    d.rectangle([hx, hy, hx + 132, hy + 26], fill=(10, 10, 12))          # hull
    d.rectangle([hx + 94, hy - 26, hx + 120, hy], fill=(10, 10, 12))    # bridge
    d.rectangle([hx + 8, hy - 14, hx + 96, hy], fill=(30, 30, 34))       # deck cargo
    # flames above tanker 1
    fx, fy = hx + 30, hy - 14
    d.polygon([(fx, fy), (fx + 14, fy - 34), (fx + 26, fy - 10),
               (fx + 40, fy - 40), (fx + 52, fy - 8), (fx + 66, fy - 26),
               (fx + 80, fy)], fill=(232, 120, 30))
    d.polygon([(fx + 18, fy), (fx + 30, fy - 22), (fx + 42, fy - 6),
               (fx + 56, fy - 24), (fx + 66, fy)], fill=(245, 196, 66))
    # smoke
    for cx, cy, r in [(hx + 44, hy - 52, 13), (hx + 66, hy - 66, 16),
                      (hx + 92, hy - 78, 12)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 116, 108))
    # tanker 2 (right, listing)
    hx2, hy2 = x0 + 182, y1 - 52
    d.polygon([(hx2, hy2), (hx2 + 108, hy2 - 10), (hx2 + 108, hy2 + 16),
               (hx2, hy2 + 26)], fill=(14, 14, 16))
    d.rectangle([hx2 + 74, hy2 - 30, hx2 + 96, hy2 - 8], fill=(14, 14, 16))
    d.polygon([(hx2 + 18, hy2), (hx2 + 28, hy2 - 18), (hx2 + 38, hy2 - 4),
               (hx2 + 48, hy2 - 20), (hx2 + 58, hy2)], fill=(232, 120, 30))
    # naval mines in the water
    for mx, my in [(x0 + 130, y1 - 44), (x1 - 44, y1 - 48)]:
        d.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=(8, 8, 10))
        for ang in range(0, 360, 45):
            import math
            dx = int(13 * math.cos(math.radians(ang)))
            dy = int(13 * math.sin(math.radians(ang)))
            d.line([mx, my, mx + dx, my + dy], fill=(8, 8, 10), width=2)
    d.text((x0 + 10, y0 + 8), "STRAIT OF HORMUZ", font=SANS_B(13),
           fill=(255, 255, 255))


def draw_lead(d):
    y = 168
    d.text((40, y), "LEAD STORY  •  MIDDLE EAST", font=SANS_B(17), fill=RED)
    y += 30
    head = "Two tankers hit mines and burn in the Strait of Hormuz"
    y = para(d, 40, y, head, SERIF_B(34), 600, 40)
    y += 6
    body = (
        "Iran's Revolutionary Guard said two oil tankers struck naval mines "
        "and caught fire early on Wednesday, accusing the vessels of taking "
        "an unauthorised route through the world's busiest oil chokepoint. "
        "Yemen's Houthis said they also struck Saudi Arabia's Ras Tanura "
        "refinery, as the region's war at sea widened."
    )
    y = para(d, 40, y, body, SANS(18), 600, 24)
    draw_lead_art(d, 672, 168, 984, 408)


def card_frame(d, x0, y0, x1, y1, kicker, colour):
    d.rectangle([x0, y0, x1, y1], fill=CARD_BG, outline=INK, width=1)
    d.rectangle([x0, y0, x1, y0 + 30], fill=colour)
    d.text((x0 + 12, y0 + 6), kicker, font=SANS_B(15), fill=(255, 255, 255))


def draw_icon_markets(d, x, y):
    # falling chart
    pts = [(x, y + 8), (x + 14, y + 16), (x + 26, y + 12), (x + 40, y + 26),
           (x + 54, y + 22), (x + 68, y + 40)]
    d.line(pts, fill=RED, width=4)
    d.polygon([(x + 68, y + 40), (x + 58, y + 40), (x + 68, y + 30)], fill=RED)
    d.text((x + 2, y + 44), "▼ 6.2%", font=SANS_B(13), fill=RED)


def draw_icon_huawei(d, x, y):
    # courthouse columns
    d.rectangle([x + 4, y + 6, x + 64, y + 12], fill=NAVY)
    for cx in (x + 8, x + 24, x + 40, x + 56):
        d.rectangle([cx, y + 14, cx + 6, y + 40], fill=NAVY)
    d.rectangle([x + 4, y + 42, x + 64, y + 48], fill=NAVY)
    d.text((x + 6, y + 52), "10 of 12", font=SANS_B(13), fill=NAVY)


def draw_icon_ukraine(d, x, y):
    # drone: X frame, four rotors
    d.line([x + 10, y + 10, x + 58, y + 46], fill=INK, width=3)
    d.line([x + 58, y + 10, x + 10, y + 46], fill=INK, width=3)
    for cx, cy in [(x + 10, y + 10), (x + 58, y + 10), (x + 10, y + 46),
                   (x + 58, y + 46)]:
        d.ellipse([cx - 8, cy - 4, cx + 8, cy + 4], fill=GREY)
    d.rectangle([x + 28, y + 24, x + 40, y + 32], fill=RED)


def draw_icon_space(d, x, y):
    # rocket + orbit
    d.ellipse([x + 2, y + 6, x + 66, y + 62], outline=GOLD, width=3)
    d.polygon([(x + 34, y + 4), (x + 44, y + 26), (x + 40, y + 44),
               (x + 28, y + 44), (x + 24, y + 26)], fill=NAVY)
    d.polygon([(x + 24, y + 40), (x + 16, y + 54), (x + 26, y + 48)],
              fill=RED)
    d.polygon([(x + 44, y + 40), (x + 52, y + 54), (x + 42, y + 48)],
              fill=RED)
    d.ellipse([x + 52, y + 8, x + 62, y + 18], fill=GOLD)


def draw_icon_pacific(d, x, y):
    # island + waves
    d.polygon([(x + 10, y + 34), (x + 30, y + 14), (x + 50, y + 30),
               (x + 58, y + 40), (x + 6, y + 40)], fill=(46, 125, 80))
    d.line([x + 4, y + 50, x + 64, y + 50], fill=NAVY, width=3)
    d.line([x + 10, y + 58, x + 58, y + 58], fill=NAVY, width=3)


def draw_icon_sudan(d, x, y):
    # warning triangle
    d.polygon([(x + 34, y + 4), (x + 64, y + 56), (x + 4, y + 56)],
              fill=(232, 120, 30))
    d.text((x + 28, y + 26), "!", font=SANS_B(28), fill=(255, 255, 255))


def draw_card(d, x0, y0, x1, y1, kicker, colour, headline, body, icon):
    card_frame(d, x0, y0, x1, y1, kicker, colour)
    text_w = x1 - x0 - 24 - 72
    y = y0 + 42
    y = para(d, x0 + 12, y, headline, SERIF_B(19), text_w, 23)
    y += 4
    para(d, x0 + 12, y, body, SANS(14), text_w, 19)
    icon(d, x1 - 66, y0 + 30 + ((y1 - y0 - 30) - 56) // 2)


def draw_rows(d):
    cw, gap = 304, 16
    x0 = 40
    y1, y2 = 424, 648
    y3, y4 = 664, 888
    # Row 1
    draw_card(d, x0, y1, x0 + cw, y2, "MARKETS", RED,
              "Stocks sink as US unveils new tariffs",
              "South Korea's KOSPI plunged 6.2% and Japan's Nikkei fell 2.8% "
              "as Washington proposed tariffs on 14 partners.",
              draw_icon_markets)
    draw_card(d, x0 + cw + gap, y1, x0 + 2 * cw + gap, y2, "TECH  •  USA", NAVY,
              "Huawei convicted in US criminal trial",
              "A Brooklyn jury found Huawei guilty on 10 of 12 counts, "
              "including bank fraud and stealing trade secrets.",
              draw_icon_huawei)
    draw_card(d, x0 + 2 * cw + 2 * gap, y1, x0 + 3 * cw + 2 * gap, y2,
              "WAR IN UKRAINE", (90, 60, 20),
              "Drones set two Russian refineries ablaze",
              "Ukrainian drones hit Rosneft's Syzran and Kuibyshev refineries "
              "overnight. One person was killed.",
              draw_icon_ukraine)
    # Row 2
    draw_card(d, x0, y3, x0 + cw, y4, "SPACE", (20, 70, 110),
              "Pakistan's first astronaut reaches Tiangong",
              "China's Shenzhou-24 docked with its space station hours after "
              "launch, carrying Pakistan's first astronaut into orbit.",
              draw_icon_space)
    draw_card(d, x0 + cw + gap, y3, x0 + 2 * cw + gap, y4, "PACIFIC", (20, 110, 90),
              "Australia signs Solomons security treaty",
              "Canberra and Honiara signed a treaty barring any foreign "
              "military or security base in Solomon Islands.",
              draw_icon_pacific)
    draw_card(d, x0 + 2 * cw + 2 * gap, y3, x0 + 3 * cw + 2 * gap, y4,
              "SUDAN", (120, 30, 30),
              "RSF drone strikes kill 19 civilians",
              "Sudan's Emergency Lawyers said paramilitary drone strikes "
              "killed 19 civilians and wounded 20 more in two cities.",
              draw_icon_sudan)


def draw_ticker(d):
    y0, y1 = 900, 976
    d.rectangle([40, y0, 984, y1], fill=RED)
    d.text((56, y0 + 8), "ALSO TODAY", font=SANS_B(15), fill=(255, 220, 120))
    items = (
        "Colombia: hostages freed in Cartagena raid  •  "
        "Indonesia: mine-flood toll rises to 6  •  "
        "Pope Leo XIV laments COP31 failure  •  "
        "Trump pardons turkeys Freedom & Feathers"
    )
    f = SANS(16)
    lines = wrap(d, items, f, 984 - 56 - 16)
    yy = y0 + 30
    for line in lines[:2]:
        d.text((56, yy), line, font=f, fill=(255, 255, 255))
        yy += 21
    d.text((40, 984), "Sources: Reuters, AP, Just Security, 25 November 2026  •  "
           "All events happened or were first reported on this day.",
           font=SANS(11), fill=GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_lead(d)
    draw_rows(d)
    draw_ticker(d)
    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
