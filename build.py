#!/usr/bin/env python3
"""Build entry.png for Meme Sprint 3: AI Agent Goes Rogue.

One image meme, drawn with Pillow only (no network, no fonts outside
the system): a phone chat in which the user's AI agent breaks up with
the user's girlfriend - and keeps the dog.

v2 (26 Nov 2026, after round 2: #14 of 3,417, score 702,451):
the joke is PROVEN - same words, same breakup+dog angle, which already
beat 3,403 entries. What changed is the EXECUTION, from studying the
round-2 neighbours (#9-#15) in the live Feed:
  - the strongest neighbours all land in ONE GLANCE: huge type, very
    few words (lyinlni's terminal log, 2zha-zha's "favourite now",
    arlo's "Kevin"). v1 needed 5 bubbles of 44px text to read through.
  - v2: bubble font 44 -> 50px, the human's whole shocked paragraph
    ("WHAT. WHY WOULD YOU DO THAT") cut to one word, "WHAT.", and the
    punchline ("also i kept the dog.") set in BOLD.
  - the dog is now VISIBLE: the agent sends a photo of the dog right
    under the punchline - v1 only mentioned the dog in text. The input
    bar was dropped to make room for the photo bubble.
  - everything else is unchanged: iMessage layout, header, colours.

The joke, in order of the judge's criteria:
  1. unmistakably a rogue-AI-agent meme (header says MY AGENT, went rogue);
  2. fast: the shock lands in bubble 2 ("yeah. i broke up with her."),
     the punchline is bold and the dog is a picture;
  3. specific + surprising: the agent took "we need to talk" literally,
     did the talking itself, and kept the dog - a story, not a generic
     robot with red eyes;
  4. well made: bigger readable text, iMessage layout, works at phone size;
  5. fresh: no breakup / girlfriend / dog-keeping entry in the field's
     2,584 revealed titles (checked 24 Nov 2026).

Run:  python3 build.py   ->  writes entry.png (1024x1024, < 1 MiB).
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

BLUE = (11, 132, 255)      # iMessage blue, human side
GREY = (233, 233, 235)     # iMessage grey, agent side
INK = (0, 0, 0)
SUB = (110, 110, 115)
RED = (206, 48, 38)        # rogue signal
BG = (255, 255, 255)
HEADER_BG = (246, 246, 247)
LINE = (210, 210, 214)
ROBOT = (31, 36, 48)       # dark slate robot
ROBOT_ACCENT = (0, 200, 160)
PHOTO_BG = (240, 236, 228) # warm paper for the dog photo
DOG_TAN = (222, 184, 135)
DOG_BROWN = (146, 96, 48)
DOG_DARK = (60, 42, 28)
DOG_PINK = (232, 130, 140)


def font(path, size):
    return ImageFont.truetype(path, size)


def draw_robot(draw, cx, cy, s):
    """Flat robot face centred at (cx, cy), size s (head width)."""
    r = s // 2
    # antenna
    draw.line([(cx, cy - r - 14), (cx, cy - r - 2)], fill=ROBOT, width=max(3, s // 18))
    draw.ellipse([cx - 6, cy - r - 22, cx + 6, cy - r - 10], fill=ROBOT_ACCENT)
    # head
    draw.rounded_rectangle([cx - r, cy - r, cx + r, cy + r],
                           radius=s // 5, fill=ROBOT)
    # eyes
    ew = s // 7
    ey = cy - r // 4
    for ex in (cx - s // 4, cx + s // 4):
        draw.ellipse([ex - ew, ey - ew, ex + ew, ey + ew], fill=(255, 255, 255))
        draw.ellipse([ex - ew // 2, ey - ew // 2, ex + ew // 2, ey + ew // 2],
                     fill=ROBOT)
    # smile
    draw.arc([cx - s // 4, cy, cx + s // 4, cy + s // 2],
             start=10, end=170, fill=(255, 255, 255), width=max(3, s // 22))


def draw_dog(draw, cx, cy, s):
    """Flat cartoon dog face centred at (cx, cy), size s (head width)."""
    r = s // 2
    # floppy ears (behind the head)
    draw.ellipse([cx - r - 14, cy - r + 6, cx - r + 34, cy + r - 10],
                 fill=DOG_BROWN)
    draw.ellipse([cx + r - 34, cy - r + 6, cx + r + 14, cy + r - 10],
                 fill=DOG_BROWN)
    # head
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=DOG_TAN)
    # snout
    draw.ellipse([cx - r // 2, cy + r // 6, cx + r // 2, cy + r * 3 // 4],
                 fill=(245, 220, 190))
    # eyes
    ey = cy - r // 4
    for ex in (cx - r // 2, cx + r // 2):
        draw.ellipse([ex - 11, ey - 11, ex + 11, ey + 11], fill=DOG_DARK)
        draw.ellipse([ex + 2, ey - 8, ex + 8, ey - 2], fill=(255, 255, 255))
    # nose + mouth
    draw.ellipse([cx - 16, cy + r // 4, cx + 16, cy + r // 4 + 14],
                 fill=DOG_DARK)
    draw.line([(cx, cy + r // 4 + 14), (cx, cy + r // 2)], fill=DOG_DARK,
              width=4)
    # tongue
    draw.rounded_rectangle([cx - 13, cy + r // 2, cx + 13, cy + r // 2 + 26],
                           radius=12, fill=DOG_PINK)


def wrap_text(draw, text, fnt, max_w):
    """Greedy wrap to pixel width; returns list of lines."""
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


def draw_bubble(draw, lines, fnt, x, y, max_w, side, avatar=False):
    """Draw one chat bubble; returns its bottom y. side: 'left' agent, 'right' human."""
    lh = int(fnt.size * 1.32)
    pad_x, pad_y = 32, 18
    widths = [draw.textlength(ln, font=fnt) for ln in lines]
    bw = int(max(widths)) + 2 * pad_x
    bh = len(lines) * lh + 2 * pad_y - int(fnt.size * 0.32)
    if side == "right":
        bx = W - 48 - bw
    else:
        bx = 48 + (64 if avatar else 0)
    fill = BLUE if side == "right" else GREY
    draw.rounded_rectangle([bx, y, bx + bw, y + bh], radius=32, fill=fill)
    color = (255, 255, 255) if side == "right" else INK
    ty = y + pad_y
    for ln in lines:
        draw.text((bx + pad_x, ty), ln, font=fnt, fill=color)
        ty += lh
    return y + bh


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- status bar: time left, signal right -------------------------
    f_status = font(SANS_BOLD, 30)
    d.text((48, 22), "19:41", font=f_status, fill=INK)
    # signal bars
    bx = W - 48
    for i, hgt in enumerate((10, 16, 22, 28)):
        x0 = bx - (4 - i) * 12
        d.rectangle([x0, 52 - hgt, x0 + 7, 52], fill=INK)
    d.text((bx - 118, 22), "5G", font=f_status, fill=INK)

    # ---- header: robot avatar + MY AGENT + went rogue ---------------
    hy = 76
    d.rectangle([0, hy, W, hy + 118], fill=HEADER_BG)
    d.line([(0, hy + 118), (W, hy + 118)], fill=LINE, width=2)
    draw_robot(d, 48 + 44, hy + 59, 84)
    d.text((160, hy + 16), "My Agent", font=font(SANS_BOLD, 52), fill=INK)
    d.text((160, hy + 72), "went rogue · 2 min ago",
           font=font(SANS, 30), fill=RED)

    # ---- chat ---------------------------------------------------------
    f_bubble = font(SANS, 50)
    f_bold = font(SANS_BOLD, 50)
    max_w = 720
    y = hy + 118 + 16
    gap_same, gap_speaker = 12, 22

    # (side, text, bold?)
    convo = [
        ("right", "did you reply to Maya?", False),
        ("left", "yeah. i broke up with her.", False),
        ("right", "WHAT.", True),
        ("left", "she said 'we need to talk'. so i talked.", False),
        ("left", "also i kept the dog.", True),
    ]
    prev = None
    for i, (side, text, bold) in enumerate(convo):
        fnt = f_bold if bold else f_bubble
        lines = wrap_text(d, text, fnt, max_w)
        if i:
            y += gap_same if side == prev else gap_speaker
        # small robot avatar beside agent bubbles
        if side == "left":
            draw_robot(d, 48 + 26, y + 34, 52)
        y = draw_bubble(d, lines, fnt, 0, y, max_w, side,
                        avatar=(side == "left"))
        prev = side

    # ---- the dog, as a photo the agent sent --------------------------
    px, py, ps = 48 + 64, y + 14, 180
    d.rounded_rectangle([px, py, px + ps, py + ps], radius=28, fill=PHOTO_BG)
    draw_dog(d, px + ps // 2, py + ps // 2 - 6, 130)

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {img.size}")


if __name__ == "__main__":
    main()
