"""Draw the 20 November 2026 front page beside this script."""

from functools import cache
from math import cos, pi, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SIZE = 1024
LEFT, RIGHT = 28, 996
PAGE_WIDTH = RIGHT - LEFT
PAPER = "#F7F2E7"
INK = "#14213D"
RED = "#C0392B"
GOLD = "#E9C46A"
RULE = "#B6AA96"
ICON_PAPER = "#EFE4CB"
BLUE = "#315A91"

FONT_DIR = Path("/usr/share/fonts/truetype/liberation")


@cache
def font(size, bold=False):
    weight = "Bold" if bold else "Regular"
    return ImageFont.truetype(str(FONT_DIR / f"LiberationSans-{weight}.ttf"), size)


def text_width(text, face):
    left, _, right, _ = face.getbbox(text)
    return max(right, face.getlength(text)) - min(left, 0)


def wrap(text, face, width):
    lines = []
    for paragraph in text.splitlines():
        line = ""
        for word in paragraph.split():
            candidate = f"{line} {word}" if line else word
            if line and text_width(candidate, face) > width:
                lines.append(line)
                line = word
            else:
                line = candidate
        lines.append(line)
    return lines


def block(draw, x, y, text, *, width, size, min_size, max_lines,
          line_step, bold=False, color=INK):
    for point_size in range(size, min_size - 1, -1):
        face = font(point_size, bold)
        lines = wrap(text, face, width)
        if len(lines) <= max_lines and all(text_width(s, face) <= width for s in lines):
            cap_height = -face.getbbox("H", anchor="ls")[1]
            for index, line in enumerate(lines):
                draw.text(
                    (x, y + cap_height + index * line_step),
                    line, font=face, fill=color, anchor="ls",
                )
            return
    raise ValueError(f"Text does not fit at {min_size}px: {text}")


def kicker(draw, x, y, text):
    draw.text((x, y), text, font=font(19, True), fill=RED, anchor="lt")


def masthead(draw):
    label = "THE WORLD IN ONE DAY"
    face = font(19, True)
    spacing = 4
    advances = [face.getlength(letter) + spacing for letter in label]
    label_width = sum(advances) - spacing
    label_left = (SIZE - label_width) / 2
    draw.line((LEFT, 25, label_left - 18, 25), fill=RULE)
    draw.line((SIZE - label_left + 18, 25, RIGHT, 25), fill=RULE)
    x = label_left
    for letter, advance in zip(label, advances):
        draw.text((x, 32), letter, font=face, fill=INK, anchor="ls")
        x += advance

    date_face = font(70, True)
    weekday, date = "FRIDAY", "20 NOVEMBER 2026"
    gap = 21
    weekday_width = date_face.getlength(weekday)
    date_left = (SIZE - weekday_width - gap - date_face.getlength(date)) / 2
    draw.text((date_left, 98), weekday, font=date_face, fill=RED, anchor="ls")
    draw.text((date_left + weekday_width + gap, 98), date, font=date_face,
              fill=INK, anchor="ls")
    draw.line((LEFT, 114, RIGHT, 114), fill=INK, width=2)


def scales(page, x, y):
    tile = Image.new("RGB", (166, 166), GOLD)
    draw = ImageDraw.Draw(tile)
    draw.rectangle((8, 8, 157, 157), outline=INK, width=1)
    draw.ellipse((77, 29, 89, 41), fill=INK)
    draw.line((83, 35, 83, 125), fill=INK, width=6)
    draw.line((35, 53, 131, 53), fill=INK, width=5)
    for pivot in (43, 123):
        draw.ellipse((pivot - 5, 48, pivot + 5, 58), fill=INK)
        draw.line((pivot - 18, 91, pivot, 54, pivot + 18, 91),
                  fill=INK, width=3, joint="curve")
        draw.pieslice((pivot - 22, 76, pivot + 22, 106), 0, 180, fill=INK)
    draw.polygon(((70, 123), (96, 123), (107, 131), (59, 131)), fill=INK)
    draw.rounded_rectangle((53, 130, 113, 136), radius=2, fill=INK)
    page.paste(tile, (x, y))


def summit_flags(draw, right, y):
    width, height, gap = 78, 32, 4
    x = right - width + 1

    for stripe in range(7):
        top = y + stripe * height // 7
        bottom = y + (stripe + 1) * height // 7 - 1
        draw.rectangle((x, top, right, bottom), fill=(RED, PAPER)[stripe % 2])
    draw.rectangle((x, y, x + 34, y + 4 * height // 7 - 1), fill=INK)
    for row in range(3):
        for column in range(4):
            dot_x = x + 5 + column * 8
            dot_y = y + 3 + row * 5
            draw.ellipse((dot_x, dot_y, dot_x + 2, dot_y + 2), fill=PAPER)
    draw.rectangle((x, y, right, y + height - 1), outline=INK)

    y += height + gap
    draw.rectangle((x, y, right, y + height - 1), fill=RED, outline=INK)
    for dx, dy, radius in ((12, 11, 7), (24, 5, 3), (30, 9, 3),
                           (30, 16, 3), (24, 21, 3)):
        points = []
        for point in range(10):
            angle = point * pi / 5 - pi / 2
            distance = radius if point % 2 == 0 else radius * 0.4
            points.append((round(x + dx + distance * cos(angle)),
                           round(y + dy + distance * sin(angle))))
        draw.polygon(points, fill=GOLD)

    y += height + gap
    for stripe, color in enumerate((PAPER, BLUE, RED)):
        top = y + stripe * height // 3
        bottom = y + (stripe + 1) * height // 3 - 1
        draw.rectangle((x, top, right, bottom), fill=color)
    draw.rectangle((x, y, right, y + height - 1), outline=INK)


def rocket(draw):
    draw.polygon(((28, 62), (64, 25), (77, 21), (75, 35), (39, 73)), fill=INK)
    draw.polygon(((46, 44), (31, 43), (22, 55), (35, 57)), fill=INK)
    draw.polygon(((52, 62), (52, 75), (39, 82), (41, 69)), fill=INK)
    draw.ellipse((55, 36, 64, 45), fill=ICON_PAPER)
    draw.line((30, 67, 19, 78), fill=RED, width=5)
    draw.line((35, 74, 28, 81), fill=RED, width=4)


def falling_chart(draw):
    draw.line((20, 20, 20, 75, 77, 75), fill=INK, width=5)
    draw.line((29, 30, 43, 44, 54, 39, 74, 60), fill=RED, width=6, joint="curve")
    draw.polygon(((78, 64), (76, 49), (63, 62)), fill=RED)


def tower(draw):
    draw.polygon(((34, 74), (34, 27), (45, 19), (63, 26), (63, 74)), fill=INK)
    draw.line((45, 26, 45, 70), fill=GOLD, width=3)
    for y in (33, 43, 53, 63):
        draw.line((51, y, 57, y), fill=ICON_PAPER, width=3)
    draw.line((20, 76, 77, 76), fill=INK, width=4)
    draw.line((63, 44, 74, 39), fill=RED, width=4)
    draw.line((66, 49, 78, 51), fill=RED, width=4)


def thermometer(draw):
    draw.ellipse((16, 20, 43, 47), fill=GOLD, outline=INK, width=3)
    for ray in ((29, 12, 29, 16), (29, 51, 29, 56), (8, 33, 13, 33),
                (47, 33, 52, 33), (14, 18, 18, 22), (40, 45, 44, 49),
                (14, 49, 18, 45), (40, 22, 44, 18)):
        draw.line(ray, fill=INK, width=3)
    draw.rounded_rectangle((55, 20, 70, 68), radius=7, fill=INK)
    draw.ellipse((49, 54, 76, 81), fill=INK)
    draw.rounded_rectangle((59, 24, 66, 66), radius=3, fill=ICON_PAPER)
    draw.ellipse((54, 59, 71, 76), fill=RED)
    draw.line((62, 45, 62, 67), fill=RED, width=5)


def medical_cross(draw):
    draw.ellipse((16, 16, 80, 80), outline=INK, width=3)
    draw.polygon(
        ((40, 28), (56, 28), (56, 40), (68, 40), (68, 56), (56, 56),
         (56, 68), (40, 68), (40, 56), (28, 56), (28, 40), (40, 40)),
        fill=RED,
    )


def satellite_dish(draw):
    draw.line((43, 56, 43, 76), fill=INK, width=6)
    draw.line((30, 77, 58, 77), fill=INK, width=5)
    draw.polygon(((22, 30), (59, 63), (50, 69), (38, 68), (27, 62),
                  (20, 51), (19, 40)), fill=INK)
    draw.line((39, 46, 58, 26), fill=INK, width=4)
    draw.ellipse((54, 22, 62, 30), fill=RED)
    draw.arc((45, 16, 70, 41), 268, 354, fill=RED, width=3)
    draw.arc((36, 9, 79, 52), 273, 350, fill=RED, width=3)


STORIES = (
    (
        "UKRAINE", "RUSSIAN BARRAGE\nHITS KYIV",
        "Missiles and drones strike Kyiv and nine regions;\n"
        "at least 8 killed; missiles stray into Poland",
        rocket,
    ),
    (
        "MARKETS", "AI SELL-OFF SHAKES\nWORLD STOCKS",
        "S&P 500 falls about 2% for a fifth straight day;\n"
        "Japan's Nikkei plunges 4.8%",
        falling_chart,
    ),
    (
        "RIYADH", "HOUTHI MISSILE\nDAMAGES SKYSCRAPER",
        "PIF tower hit in the financial district; Saudi-led\n"
        "coalition strikes Yemen's Hodeidah port",
        tower,
    ),
    (
        "ANTALYA · COP31", "CLIMATE TALKS GO\nINTO OVERTIME",
        "Draft deal drops the call to phase out\n"
        "fossil fuels as nations quarrel",
        thermometer,
    ),
    (
        "KENYA · HEALTH", "LAST EBOLA PATIENT\nGOES HOME",
        "Kenya discharges its final patient\n"
        "37 days after the first case",
        medical_cross,
    ),
    (
        "SPACE", "VOYAGER 1, ONE\nLIGHT-DAY FROM HOME",
        "NASA's farthest probe phones home\n"
        "from about 26 billion km away",
        satellite_dish,
    ),
)


def story_grid(page, draw):
    top, row_height, gutter = 450, 156, 14
    center = SIZE // 2
    column_width = (PAGE_WIDTH - gutter) // 2
    bottom = top + 3 * row_height
    draw.line((LEFT, top, RIGHT, top), fill=INK, width=2)
    draw.line((center, top, center, bottom), fill=RULE)
    for row in range(1, 4):
        y = top + row * row_height
        draw.line((LEFT, y, RIGHT, y), fill=RULE)

    for index, (location, headline, summary, paint_icon) in enumerate(STORIES):
        row, column = divmod(index, 2)
        x = LEFT + column * (column_width + gutter)
        y = top + row * row_height
        kicker(draw, x, y + 12, location)
        block(draw, x, y + 35, headline, width=column_width, size=37,
              min_size=37, max_lines=2, line_step=35, bold=True)
        block(draw, x, y + 105, summary, width=column_width, size=23,
              min_size=22, max_lines=2, line_step=25)

        icon = Image.new("RGB", (96, 96), ICON_PAPER)
        paint_icon(ImageDraw.Draw(icon))
        page.paste(icon.resize((48, 48), Image.Resampling.LANCZOS),
                   (x + column_width - 48, y + 11))


def front_page():
    page = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(page)
    masthead(draw)

    kicker(draw, LEFT, 132, "THE HAGUE · INTERNATIONAL JUSTICE")
    block(draw, LEFT, 157, "WORLD COURT: MYANMAR\nCOMMITTED GENOCIDE",
          width=778, size=58, min_size=56, max_lines=2, line_step=53, bold=True)
    block(draw, LEFT, 265,
          "The ICJ finds Myanmar's campaign against the Rohingya\n"
          "was genocide — the first such ruling against a state",
          width=778, size=27, min_size=26, max_lines=2, line_step=30)
    scales(page, RIGHT - 166, 139)

    draw.line((LEFT, 331, RIGHT, 331), fill=INK, width=2)
    kicker(draw, LEFT, 349, "SHENZHEN · APEC SUMMIT")
    block(draw, LEFT, 376, "TRUMP, XI & PUTIN HOLD FIRST THREE-WAY SUMMIT",
          width=860, size=33, min_size=32, max_lines=1, line_step=33, bold=True)
    block(draw, LEFT, 414,
          "Joint peace declaration: a nuclear war cannot be won and must never be fought",
          width=860, size=24, min_size=23, max_lines=1, line_step=25)
    summit_flags(draw, RIGHT, 339)

    story_grid(page, draw)

    draw.rectangle((LEFT, 934, RIGHT, 989), fill=INK)
    draw.text((LEFT + 16, 961), "ALSO TODAY:", font=font(20, True), fill=GOLD, anchor="lm")
    draw.line((LEFT + 159, 943, LEFT + 159, 980), fill=GOLD)
    block(draw, LEFT + 171, 942,
          "UK & EU seal food and youth deals in Brussels • EU sends €7.9 billion to Ukraine\n"
          "• White House fires cyber chief after outage chaos",
          width=PAGE_WIDTH - 184, size=21, min_size=21, max_lines=2, line_step=23, color=PAPER)
    draw.text((SIZE // 2, 1000), "Compiled from news reports of 20 November 2026",
              font=font(16), fill=INK, anchor="mt")
    return page


if __name__ == "__main__":
    output = Path(__file__).resolve().with_name("entry.png")
    front_page().save(output, format="PNG", optimize=True)
