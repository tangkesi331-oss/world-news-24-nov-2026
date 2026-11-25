#!/usr/bin/env python3
"""Render the one-image news summary for Tuesday 24 November 2026.

Draws a 1024x1024 PNG poster: off-white background, black type, one red
accent, a big headline and a 2x3 grid of story panels. Build-time tool
only (uses Pillow); the contest entrypoint main.py just copies the
resulting assets/entry.png.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = REPO_ROOT / "assets" / "entry.png"

W = H = 1024
BG = (247, 244, 236)        # #F7F4EC
INK = (17, 17, 17)          # near-black
RED = (200, 16, 46)         # #C8102E
HAIR = (216, 210, 196)      # light warm grey for panel rules

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
BOLD = FONT_DIR / "DejaVuSans-Bold.ttf"
REG = FONT_DIR / "DejaVuSans.ttf"

MARGIN = 64
CONTENT_W = W - 2 * MARGIN


def font(path, size):
    return ImageFont.truetype(str(path), size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in s.split():
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def balanced_wrap(draw, s, f, max_w):
    """Wrap a headline into at most 2 lines, split so the lines are as
    equal in width as possible (no orphan word dangling on line 2)."""
    if text_w(draw, s, f) <= max_w:
        return [s]
    words = s.split()
    best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        wa, wb = text_w(draw, a, f), text_w(draw, b, f)
        if wa <= max_w and wb <= max_w:
            score = max(wa, wb)
            if best is None or score < best[0]:
                best = (score, [a, b])
    if best:
        return best[1]
    return wrap(draw, s, f, max_w)


def draw_spaced(draw, xy, s, f, fill, tracking):
    """Draw text with extra letter tracking, return total width drawn."""
    x, y = xy
    for ch in s:
        draw.text((x, y), ch, font=f, fill=fill)
        x += text_w(draw, ch, f) + tracking
    return x - tracking - xy[0]


def spaced_w(draw, s, f, tracking):
    return sum(text_w(draw, ch, f) for ch in s) + tracking * (len(s) - 1)


STORIES = [
    ("Tanker hits a mine in Hormuz",
     "Oil on edge as the strait stays tense"),
    ("Airstrike hits Zaporizhzhia",
     "Ukraine's nuclear city under fire again"),
    ("Hamas security chief killed",
     "Strike in Gaza raises the stakes"),
    ("COP31 talks collapse",
     "No deal as climate summit ends in deadlock"),
    ("Ukraine sinks Russian warship",
     "Struck off the Libyan coast"),
    ("NATO answers nuclear-satellite reports",
     "Alliance responds to Moscow's space claims"),
]

BRIEFS = [
    "UAE bus crash kills 13",
    "Germany first to receive Ukraine's Delta system",
    "King tides threaten US Thanksgiving travel",
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- header ------------------------------------------------------
    y = 50
    f_head = font(BOLD, 29)
    draw_spaced(d, (MARGIN, y), "THE WORLD IN A DAY", f_head, INK, 6)
    f_date = font(REG, 25)
    date = "Tuesday, 24 November 2026"
    d.text((W - MARGIN - text_w(d, date, f_date), y + 3), date, font=f_date, fill=INK)
    y += 58
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=3)

    # ---- headline ----------------------------------------------------
    y += 30
    d.rectangle([MARGIN, y, MARGIN + 132, y + 13], fill=RED)
    y += 34
    headline = ["JENSEN HUANG BACK", "AS NVIDIA CEO"]
    size = 100
    while size > 40:
        f_h = font(BOLD, size)
        if max(text_w(d, line, f_h) for line in headline) <= CONTENT_W:
            break
        size -= 4
    lh = int(size * 1.06)
    for line in headline:
        d.text((MARGIN, y), line, font=f_h, fill=INK)
        y += lh
    y += 10
    f_sub = font(REG, 35)
    d.text((MARGIN, y), "Shares jump about 30% in a day", font=f_sub, fill=INK)
    y += 62
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=3)

    # ---- story grid --------------------------------------------------
    y += 34
    gap_x = 44
    col_w = (CONTENT_W - gap_x) // 2
    f_title = font(BOLD, 30)
    f_body = font(REG, 24)
    title_lh, body_lh = 37, 30

    rows = [STORIES[i:i + 2] for i in range(0, 6, 2)]
    for r, row in enumerate(rows):
        panels = []
        row_h = 0
        for title, body in row:
            t_lines = balanced_wrap(d, title, f_title, col_w)
            b_lines = balanced_wrap(d, body, f_body, col_w)
            h = len(t_lines) * title_lh + 6 + len(b_lines) * body_lh
            panels.append((t_lines, b_lines))
            row_h = max(row_h, h)
        for c, (t_lines, b_lines) in enumerate(panels):
            x = MARGIN + c * (col_w + gap_x)
            py = y
            d.line([(x, py - 14), (x + col_w, py - 14)], fill=HAIR, width=2)
            for line in t_lines:
                d.text((x, py), line, font=f_title, fill=INK)
                py += title_lh
            py += 6
            for line in b_lines:
                d.text((x, py), line, font=f_body, fill=INK)
                py += body_lh
        y += row_h + 28
        print(f"row {r}: height used, next y = {y}")

    # ---- footer ------------------------------------------------------
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=3)
    y += 24
    f_foot = font(REG, 24)
    # Two fixed lines so a separator dot never dangles at a line end:
    # line 1 carries briefs 1-2, line 2 carries brief 3.
    foot_lines = [BRIEFS[:2], BRIEFS[2:]]
    for parts in foot_lines:
        seg_w = [text_w(d, p, f_foot) for p in parts]
        dot_w = text_w(d, "·", f_foot)
        total = sum(seg_w) + (dot_w + 28) * (len(parts) - 1)
        x = (W - total) / 2
        for i, part in enumerate(parts):
            if i:
                d.text((x + 14, y - 5), "·", font=f_foot, fill=RED)
                x += dot_w + 28
            d.text((x, y), part, font=f_foot, fill=INK)
            x += seg_w[i]
        y += 32
    print(f"final y = {y} (canvas {H})")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT_PATH, format="PNG", optimize=True)
    print(f"wrote {OUT_PATH} ({OUT_PATH.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
