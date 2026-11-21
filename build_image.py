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
DISPLAY_FONT = Path("/home/ubuntu/.local/share/fonts/NotoSerifJP.ttf")


@cache
def font(size, bold=False):
    weight = "Bold" if bold else "Regular"
    return ImageFont.truetype(str(FONT_DIR / f"LiberationSans-{weight}.ttf"), size)


@cache
def display_font(size):
    face = ImageFont.truetype(str(DISPLAY_FONT), size)
    face.set_variation_by_name("Black")
    return face


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


def block(draw, x, y, text, *, width, face, max_lines, line_step, color=INK):
    lines = wrap(text, face, width)
    if len(lines) > max_lines or any(text_width(line, face) > width for line in lines):
        raise ValueError(f"Text does not fit at {face.size}px: {text}")
    cap_height = -face.getbbox("H", anchor="ls")[1]
    for index, line in enumerate(lines):
        draw.text((x, y + cap_height + index * line_step),
                  line, font=face, fill=color, anchor="ls")


def dot(draw, x, y, radius, fill):
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=fill)


def number_badge(draw, x, y, number, radius=14):
    dot(draw, x, y, radius, RED)
    draw.text((x, y), str(number), font=font(round(radius * 1.55), True),
              fill=(255, 255, 255), anchor="mm")


def kicker(draw, x, y, number, text):
    number_badge(draw, x + 14, y + 14, number)
    draw.text((x + 37, y + 14), text, font=font(19, True), fill=RED, anchor="lm")


def masthead(draw):
    label = "THE WORLD IN ONE DAY"
    face = font(19, True)
    spacing = 4
    advances = [face.getlength(letter) + spacing for letter in label]
    label_width = sum(advances) - spacing
    label_left = (SIZE - label_width) / 2
    draw.line((LEFT, 21, label_left - 18, 21), fill=RULE)
    draw.line((SIZE - label_left + 18, 21, RIGHT, 21), fill=RULE)
    x = label_left
    for letter, advance in zip(label, advances):
        draw.text((x, 28), letter, font=face, fill=INK, anchor="ls")
        x += advance

    date_face = display_font(64)
    weekday, date = "FRIDAY", "20 NOVEMBER 2026"
    gap = 21
    weekday_width = date_face.getlength(weekday)
    date_left = (SIZE - weekday_width - gap - date_face.getlength(date)) / 2
    draw.text((date_left, 89), weekday, font=date_face, fill=RED, anchor="ls")
    draw.text((date_left + weekday_width + gap, 89), date, font=date_face,
              fill=INK, anchor="ls")
    draw.line((LEFT, 103, RIGHT, 103), fill=INK, width=2)


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
    page.paste(tile.resize((116, 116), Image.Resampling.LANCZOS), (x, y))


def star(draw, x, y, radius, color):
    points = []
    for point in range(10):
        angle = point * pi / 5 - pi / 2
        distance = radius if point % 2 == 0 else radius * 0.4
        points.append((round(x + distance * cos(angle)),
                       round(y + distance * sin(angle))))
    draw.polygon(points, fill=color)


def summit_flags(page, right, top_y):
    tile = Image.new("RGB", (78, 104), PAPER)
    draw = ImageDraw.Draw(tile)
    x, y, right_edge = 0, 0, 77
    height, gap = 32, 4

    for stripe in range(7):
        top = y + stripe * height // 7
        bottom = y + (stripe + 1) * height // 7 - 1
        draw.rectangle((x, top, right_edge, bottom), fill=(RED, PAPER)[stripe % 2])
    draw.rectangle((x, y, x + 34, y + 4 * height // 7 - 1), fill=INK)
    for row in range(3):
        for column in range(4):
            dot_x = x + 5 + column * 8
            dot_y = y + 3 + row * 5
            draw.ellipse((dot_x, dot_y, dot_x + 2, dot_y + 2), fill=PAPER)
    draw.rectangle((x, y, right_edge, y + height - 1), outline=INK)

    y += height + gap
    draw.rectangle((x, y, right_edge, y + height - 1), fill=RED, outline=INK)
    for dx, dy, radius in ((12, 11, 7), (24, 5, 3), (30, 9, 3),
                           (30, 16, 3), (24, 21, 3)):
        star(draw, x + dx, y + dy, radius, GOLD)

    y += height + gap
    for stripe, color in enumerate((PAPER, BLUE, RED)):
        top = y + stripe * height // 3
        bottom = y + (stripe + 1) * height // 3 - 1
        draw.rectangle((x, top, right_edge, bottom), fill=color)
    draw.rectangle((x, y, right_edge, y + height - 1), outline=INK)
    page.paste(tile.resize((54, 72), Image.Resampling.LANCZOS), (right - 53, top_y))


# Hand-drawn coastal outlines in (longitude, latitude) for the coarse dot mask.
LAND_OUTLINES = (
    # North America
    ((-168, 65), (-162, 70), (-143, 71), (-133, 69), (-128, 72), (-111, 70),
     (-103, 74), (-88, 71), (-80, 74), (-69, 71), (-72, 65), (-87, 57),
     (-91, 61), (-97, 65), (-96, 54), (-85, 52), (-78, 57), (-77, 62),
     (-63, 58), (-60, 50), (-53, 49), (-66, 45), (-72, 41), (-77, 35),
     (-81, 30), (-80, 25), (-84, 28), (-88, 30), (-96, 28), (-98, 22),
     (-92, 19), (-87, 21), (-86, 15), (-83, 9), (-78, 8), (-81, 8),
     (-88, 14), (-96, 16), (-104, 20), (-111, 28), (-115, 32), (-114, 26),
     (-121, 34), (-125, 42), (-125, 51), (-132, 55), (-140, 60), (-152, 58),
     (-164, 54), (-159, 60), (-166, 62)),
    ((-122, 75), (-107, 80), (-93, 79), (-81, 84), (-64, 81), (-75, 76),
     (-85, 73), (-100, 75)),
    # Greenland
    ((-72, 77), (-57, 82), (-35, 83), (-18, 81), (-21, 73), (-32, 68),
     (-42, 60), (-51, 64), (-53, 70), (-62, 75)),
    # South America
    ((-81, 9), (-74, 12), (-65, 10), (-61, 9), (-52, 5), (-48, 0),
     (-41, -2), (-35, -6), (-38, -13), (-44, -23), (-50, -27), (-54, -34),
     (-59, -38), (-64, -47), (-68, -54), (-74, -50), (-74, -42),
     (-72, -32), (-71, -20), (-77, -12), (-81, -5)),
    # Europe and Asia
    ((-10, 36), (-9, 43), (-2, 44), (-5, 48), (4, 52), (9, 54),
     (13, 55), (7, 58), (6, 63), (15, 69), (29, 72), (31, 66), (44, 67),
     (45, 70), (58, 68), (68, 72), (79, 71), (89, 76), (105, 77),
     (118, 73), (139, 73), (154, 71), (166, 69), (179, 67), (179, 63),
     (166, 62), (162, 57), (158, 51), (154, 52), (156, 59), (148, 60),
     (142, 55), (137, 53), (142, 47), (133, 43), (129, 35), (126, 35),
     (125, 40), (121, 37), (122, 31), (119, 25), (114, 22), (108, 21),
     (109, 14), (104, 9), (103, 2), (100, 6), (98, 15), (94, 17),
     (91, 22), (87, 21), (81, 14), (77, 8), (72, 18), (68, 23), (60, 25),
     (56, 27), (51, 30), (56, 25), (58, 21), (50, 16), (44, 13),
     (42, 17), (36, 28), (32, 31), (36, 36), (28, 36), (26, 40),
     (22, 39), (19, 43), (13, 45), (17, 40), (15, 38), (10, 44), (6, 43),
     (1, 41), (-1, 37)),
    # Africa
    ((-17, 21), (-12, 29), (-6, 35), (3, 37), (11, 37), (11, 33),
     (20, 32), (26, 31), (34, 31), (36, 23), (43, 12), (51, 11),
     (48, 3), (42, -3), (40, -12), (35, -19), (33, -27), (27, -34),
     (18, -35), (14, -25), (12, -18), (13, -8), (9, 0), (10, 5),
     (3, 6), (-3, 5), (-8, 5), (-15, 11), (-17, 15)),
    # Australia
    ((112, -22), (115, -19), (122, -16), (128, -14), (132, -12), (137, -12),
     (137, -16), (142, -17), (143, -11), (148, -19), (153, -25),
     (151, -33), (146, -39), (140, -38), (135, -34), (130, -32),
     (122, -34), (115, -35)),
    # Islands and archipelagos
    ((-24, 65), (-15, 67), (-13, 64), (-23, 63)),
    ((-8, 58), (-3, 59), (2, 52), (-5, 50), (-10, 52)),
    ((-85, 23), (-78, 23), (-73, 20), (-82, 20)),
    ((130, 32), (136, 35), (142, 44), (146, 44), (141, 37), (135, 33)),
    ((95, 5), (105, -4), (114, -7), (119, -9), (105, -8), (99, -2)),
    ((109, 0), (113, 6), (120, 6), (118, -4), (112, -4)),
    ((130, -2), (142, -3), (152, -6), (150, -10), (138, -7)),
    ((49, -12), (50, -17), (47, -24), (43, -25), (44, -18)),
    ((166, -47), (167, -43), (174, -38), (178, -36), (176, -42), (170, -46)),
)

MAP_PINS = (
    # Number, longitude, latitude, badge offset x/y, radius.
    (1, 4.3, 52.1, -21, -12, 15),
    (2, 114.1, 22.5, 0, 0, 15),
    (3, 30.5, 50.4, 21, -12, 15),
    (4, -74.0, 40.7, 0, 0, 15),
    (4, 139.7, 35.7, 0, 0, 12),
    (5, 46.7, 24.6, 25, 13, 15),
    (6, 30.7, 36.9, -26, 15, 15),
    (7, 36.8, -1.3, 1, 26, 15),
)


def project(lon, lat):
    # End at 56°S so the main landmasses fill the shallow map band.
    return (lon + 180) / 360, (90 - lat) / 146


def world_map(page, draw):
    top, bottom = 374, 526
    draw.line((LEFT, top, RIGHT, top), fill=INK, width=2)

    map_x, map_y, map_width, map_height = 154, 378, 752, 120
    columns, rows = 164, 29
    mask = Image.new("1", (columns, rows))
    mask_draw = ImageDraw.Draw(mask)
    for outline in LAND_OUTLINES:
        cells = [
            (round(u * (columns - 1)), round(v * (rows - 1)))
            for u, v in (project(lon, lat) for lon, lat in outline)
        ]
        mask_draw.polygon(cells, fill=1)

    # Render at 3x to keep the ink dots round and distinct along the coast.
    sample = 3
    map_dots = Image.new("RGB", ((map_width + 4) * sample, (map_height + 4) * sample), PAPER)
    dot_draw = ImageDraw.Draw(map_dots)
    for row in range(rows):
        y = round(sample * (2 + row * map_height / (rows - 1)))
        for column in range(columns):
            if mask.getpixel((column, row)):
                x = round(sample * (2 + column * map_width / (columns - 1)))
                dot(dot_draw, x, y, 5, INK)
    page.paste(map_dots.resize((map_width + 4, map_height + 4), Image.Resampling.LANCZOS),
               (map_x - 2, map_y - 2))
    block(draw, LEFT, top + 42, "WHERE IT\nHAPPENED", width=182,
          face=font(26, True), max_lines=2, line_step=26)

    pins = []
    for number, lon, lat, dx, dy, radius in MAP_PINS:
        u, v = project(lon, lat)
        x, y = round(map_x + u * map_width), round(map_y + v * map_height)
        if dx or dy:
            draw.line((x, y, x + dx, y + dy), fill=RED, width=2)
            dot(draw, x, y, 3, RED)
        pins.append((x + dx, y + dy, number, radius))
    for x, y, number, radius in pins:
        dot(draw, x, y, radius + 2, PAPER)
        number_badge(draw, x, y, number, radius)

    for step in range(13):
        t = step / 12
        dot(draw, 867 + 78 * t, 433 - 43 * (2 * t - t * t), 1.6, INK)
    star(draw, 956, 390, 9, RED)
    draw.text((914, 438), "8 · DEEP SPACE", font=font(19, True), fill=RED, anchor="mt")

    draw.line((LEFT, bottom - 25, RIGHT, bottom - 25), fill=RULE)
    draw.text(
        (SIZE // 2, bottom - 19),
        "1 The Hague · 2 Shenzhen · 3 Kyiv · 4 New York & Tokyo · 5 Riyadh · 6 Antalya · 7 Kenya · 8 Deep space",
        font=font(18, True), fill=INK, anchor="mt",
    )


def rocket(draw):
    draw.polygon(((28, 62), (64, 25), (77, 21), (75, 35), (39, 73)), fill=INK)
    draw.polygon(((46, 44), (31, 43), (22, 55), (35, 57)), fill=INK)
    draw.polygon(((52, 62), (52, 75), (39, 82), (41, 69)), fill=INK)
    draw.ellipse((55, 36, 64, 45), fill=ICON_PAPER)
    draw.line((30, 67, 19, 78), fill=RED, width=5)
    draw.line((35, 74, 28, 81), fill=RED, width=4)


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


def market_bars(draw, right, top):
    left, bar_left = right - 175, right - 75
    for label, decline in (("S&P 500 −2%", 2), ("NIKKEI −4.8%", 4.8)):
        draw.text((left, top), label, font=font(14, True), fill=INK, anchor="lm")
        length = round(76 * decline / 4.8)
        draw.rectangle((bar_left, top - 5, bar_left + length - 1, top + 5), fill=RED)
        top += 16


def voyager_scale(draw, right, top):
    left = right - 140
    dot(draw, left, top, 3, INK)
    for x in range(left + 12, right - 6, 8):
        dot(draw, x, top, 1, INK)
    dot(draw, right, top, 3, RED)
    draw.text((right, top + 7), "one light-day ≈ 26 billion km",
              font=font(11, True), fill=INK, anchor="rt")


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
        None,
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
        None,
    ),
)


def story_grid(page, draw):
    top, row_height, gutter = 526, 138, 20
    center = SIZE // 2
    column_width = (PAGE_WIDTH - gutter) // 2
    bottom = top + 3 * row_height
    draw.line((LEFT, top, RIGHT, top), fill=INK, width=2)
    draw.line((center, top, center, bottom), fill=RULE)
    for row in range(1, 4):
        y = top + row * row_height
        draw.line((LEFT, y, RIGHT, y), fill=RULE)

    for index, (location, headline, summary, paint_icon) in enumerate(STORIES):
        number = index + 3
        row, column = divmod(index, 2)
        x = LEFT + column * (column_width + gutter)
        y = top + row * row_height
        right = x + column_width
        kicker(draw, x, y + 6, number, location)
        headline_size, headline_width = 36, column_width
        if number == 4:
            headline_size, headline_width = 31, column_width - 125
            market_bars(draw, right - 12, y + 69)
        elif number == 8:
            voyager_scale(draw, right - 8, y + 41)

        block(draw, x, y + 35, headline, width=headline_width,
              face=display_font(headline_size), max_lines=2, line_step=31)
        block(draw, x, y + 97, summary, width=column_width,
              face=font(21 if number == 3 else 22), max_lines=2, line_step=21)

        if paint_icon:
            icon = Image.new("RGB", (96, 96), ICON_PAPER)
            paint_icon(ImageDraw.Draw(icon))
            page.paste(icon.resize((44, 44), Image.Resampling.LANCZOS),
                       (right - 44, y + 9))


def front_page():
    page = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(page)
    masthead(draw)

    kicker(draw, LEFT, 110, 1, "THE HAGUE · INTERNATIONAL JUSTICE")
    block(draw, LEFT, 142, "WORLD COURT: MYANMAR\nCOMMITTED GENOCIDE",
          width=842, face=display_font(58), max_lines=2, line_step=48)
    block(draw, LEFT, 239,
          "The ICJ finds Myanmar's campaign against the Rohingya\n"
          "was genocide — the first such ruling against a state",
          width=842, face=font(24), max_lines=2, line_step=23)
    scales(page, RIGHT - 115, 145)

    draw.line((LEFT, 284, RIGHT, 284), fill=INK, width=2)
    kicker(draw, LEFT, 288, 2, "SHENZHEN · APEC SUMMIT")
    block(draw, LEFT, 319, "TRUMP, XI & PUTIN HOLD FIRST THREE-WAY SUMMIT",
          width=904, face=display_font(31), max_lines=1, line_step=31)
    block(draw, LEFT, 352,
          "Joint peace declaration: a nuclear war cannot be won and must never be fought",
          width=904, face=font(23), max_lines=1, line_step=23)
    summit_flags(page, RIGHT, 294)

    world_map(page, draw)
    story_grid(page, draw)

    draw.rectangle((LEFT, 947, RIGHT, 995), fill=INK)
    draw.text((LEFT + 15, 971), "ALSO TODAY:", font=font(20, True), fill=GOLD, anchor="lm")
    draw.line((LEFT + 156, 955, LEFT + 156, 987), fill=GOLD)
    block(draw, LEFT + 170, 953,
          "UK & EU seal food and youth deals in Brussels • EU sends €7.9 billion to Ukraine\n"
          "• White House fires cyber chief after outage chaos",
          width=PAGE_WIDTH - 182, face=font(21), max_lines=2, line_step=20, color=PAPER)
    draw.text((SIZE // 2, 1002), "Compiled from news reports of 20 November 2026",
              font=font(17), fill=INK, anchor="mt")
    return page


if __name__ == "__main__":
    output = Path(__file__).resolve().with_name("entry.png")
    front_page().save(output, format="PNG", optimize=True)
