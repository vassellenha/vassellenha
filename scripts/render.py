#!/usr/bin/env python3
"""Original Persona-inspired comic motion graphics for GitHub-compatible GIFs.

All animation is pre-rendered: README.md itself requires no scripts or CSS.
Run `python3 scripts/render.py` from the project root to regenerate assets.
"""

from __future__ import annotations

import argparse
import math
import random
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
RED = (222, 16, 36)
BRIGHT = (250, 34, 47)
BLACK = (10, 9, 12)
INK = (22, 18, 22)
WHITE = (250, 247, 236)
YELLOW = (255, 221, 77)
GRAY = (164, 163, 166)
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(size, mono=False, regular=False):
    return ImageFont.truetype(FONT_MONO if mono else FONT_REG if regular else FONT_BOLD, size)


def clamp(x, low=0, high=1):
    return max(low, min(high, x))


def ease(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def poly(d, points, fill, outline=None, width=1):
    d.polygon([(int(x), int(y)) for x, y in points], fill=fill)
    if outline:
        d.line(points + [points[0]], fill=outline, width=width, joint="curve")


def panel(d, x, y, w, h, color, cut=24, border=None, borderwidth=5):
    p = [(x + cut, y), (x + w, y), (x + w - cut, y + h),
         (x, y + h), (x + cut // 2, y + h // 2)]
    poly(d, p, color, border, borderwidth)


def dot_field(d, rect, step=21, radius=3, seed=1, color=BLACK, wobble=0):
    x0, y0, x1, y1 = rect
    rnd = random.Random(seed)
    for x in range(int(x0), int(x1), step):
        for y in range(int(y0), int(y1), step):
            wave = .5 + .5 * math.sin((x + y) / 70 + wobble)
            r = max(1, radius * (.5 + wave) * (.7 + rnd.random() * .4))
            d.ellipse((x - r, y - r, x + r, y + r), fill=color)


def burst(d, cx, cy, r0, r1, n, phase, colors=(RED, BLACK)):
    for i in range(n):
        a = 2 * math.pi * i / n + phase
        a2 = a + .025 + .012 * math.sin(i * 1.3)
        r = r1 * (.85 + .23 * math.sin(i * 3.7 + phase))
        poly(d, [(cx + r0 * math.cos(a), cy + r0 * math.sin(a)),
                 (cx + r * math.cos(a2), cy + r * math.sin(a2)),
                 (cx + r0 * math.cos(a + .065), cy + r0 * math.sin(a + .065))],
             colors[i % len(colors)])


def scratch(d, w, h, t, seed=4, count=44, color=WHITE):
    rnd = random.Random(seed)
    for i in range(count):
        x = rnd.randint(-100, w + 150) + 60 * math.sin(t * 2 + i)
        y = rnd.randint(-100, h + 100)
        ln = rnd.randint(12, 130)
        d.line((x, y, x + ln, y - ln * .34), fill=color, width=rnd.choice([1, 2, 3]))


def labels(d, w, title, index, y=22):
    panel(d, 18, y, min(w - 36, 580), 46, WHITE, 11)
    d.text((42, y + 7), f"// {index:02d}  {title}", font=font(25, mono=True), fill=BLACK)
    d.text((w - 255, y + 11), "VASSELL / 2026", font=font(20, mono=True), fill=WHITE)


def type_layer(im, text, pos, size, fg=WHITE, shadow=BLACK, angle=0,
               stroke=0, stroke_fill=BLACK, skew=0, mono=False):
    f = font(size, mono)
    bb = f.getbbox(text, stroke_width=stroke)
    lw = bb[2] - bb[0] + 70
    lh = bb[3] - bb[1] + 60
    lay = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    at = (32 - bb[0], 28 - bb[1])
    if shadow:
        ld.text((at[0] + 8, at[1] + 8), text, font=f, fill=shadow,
                stroke_width=stroke + 2 if stroke else 0, stroke_fill=shadow)
    ld.text(at, text, font=f, fill=fg, stroke_width=stroke, stroke_fill=stroke_fill)
    if skew:
        ext = abs(skew) * lh
        lay = lay.transform((int(lw + ext), lh), Image.Transform.AFFINE,
                            (1, skew, -min(0, skew * lh), 0, 1, 0),
                            Image.Resampling.BICUBIC)
    if angle:
        lay = lay.rotate(angle, Image.Resampling.BICUBIC, expand=True)
    im.paste(lay, (int(pos[0]), int(pos[1])), lay)


def gfx_base(w, h, t, variant):
    im = Image.new("RGB", (w, h), RED)
    d = ImageDraw.Draw(im)
    if variant in ("hero", "missions", "outro"):
        d.rectangle((0, 0, w, h), fill=RED)
        poly(d, [(0, 0), (w * .48, 0), (w * .24, h), (0, h)], BLACK)
        poly(d, [(w * .9, 0), (w, 0), (w, h), (w * .64, h)], BLACK)
        burst(d, w * .77, h * .52, 90, max(w, h), 32,
              t * .035, (WHITE, RED, BLACK))
        poly(d, [(0, h * .84), (w, h * .63), (w, h), (0, h)], BLACK)
        dot_field(d, (w * .63, 0, w, h * .73), step=22, radius=2.8,
                  color=BLACK, wobble=t)
    else:
        d.rectangle((0, 0, w, h), fill=BLACK)
        poly(d, [(w * .38, 0), (w, 0), (w, h * .21), (w * .21, h)], RED)
        poly(d, [(0, h * .77), (w * .58, h * .30), (w * .43, h), (0, h)], WHITE)
        dot_field(d, (w * .5, 20, w, h), step=20, radius=2.4, color=BLACK, wobble=t)
    scratch(d, w, h, t, seed=54, count=25)
    # Printed-paper imperfections on the edges.
    for i in range(12):
        xx = (i * 231 + 51) % w
        yy = (i * 79 + 11) % h
        d.line((xx, yy, xx + 33, yy - 9), fill=BLACK if i % 2 else WHITE, width=2)
    return im


_OC_CACHE = {}


def oc_frame(width, height, mode="wide"):
    """Preserve the supplied original character art and facial details."""
    key = (width, height, mode)
    if key in _OC_CACHE:
        return _OC_CACHE[key].copy()
    source = Image.open(OUT / "source" / "vassell-oc.png").convert("RGB")
    if mode == "portrait":
        source = source.crop((515, 25, 1435, 940))
    elif mode == "close":
        source = source.crop((225, 0, 1510, 830))
    sw, sh = source.size
    scale = max(width / sw, height / sh)
    sized = source.resize((math.ceil(sw * scale), math.ceil(sh * scale)),
                          Image.Resampling.LANCZOS)
    left = (sized.width - width) // 2
    top = (sized.height - height) // 2
    result = sized.crop((left, top, left + width, top + height))
    _OC_CACHE[key] = result
    return result.copy()


def oc_panel(im, box, mode="portrait"):
    x, y, w, h = box
    fragment = oc_frame(w, h, mode)
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    poly(md, [(25, 0), (w, 0), (w - 27, h), (0, h), (0, 45)], 255)
    im.paste(fragment, (x, y), mask)
    d = ImageDraw.Draw(im)
    d.line([(x + 25, y), (x + w, y), (x + w - 27, y + h),
            (x, y + h), (x, y + 45), (x + 25, y)], fill=WHITE, width=8)


def draw_hero_oc(t):
    """Two-act main banner with the user's actual OC rather than a placeholder."""
    w, h = 1280, 620
    im = oc_frame(w, h, "wide")
    d = ImageDraw.Draw(im)
    poly(d, [(23, 107), (658, 47), (638, 515), (15, 566)], BLACK, WHITE, 10)
    poly(d, [(25, 121), (645, 65), (633, 176), (21, 235)], RED)
    panel(d, 40, 22, 533, 58, WHITE, 12, BLACK, 4)
    d.text((62, 37), "VASSELL // FULL-STACK DEVELOPER", font=font(22, mono=True), fill=BLACK)
    d.text((72, 132), "DEVELOPER PROFILE", font=font(34), fill=WHITE)
    shift = 5 * math.sin(t * 2.4)
    type_layer(im, "VASSELL", (46 + shift, 219), 131, WHITE, RED,
               angle=3, stroke=3, stroke_fill=BLACK, skew=-.05)
    d = ImageDraw.Draw(im)
    panel(d, 65, 413, 535, 76, RED, 18, WHITE, 5)
    d.text((94, 429), "FULL-STACK / UI-UX", font=font(31, mono=True), fill=WHITE)
    x = 37 + 5 * math.sin(t * 1.9)
    panel(d, x, 500, 550, 52, WHITE, 14, BLACK, 3)
    d.text((x + 25, 510), "DESIGN. DEVELOP. DEPLOY.", font=font(26, mono=True), fill=BLACK)
    for j in range(7):
        px = 11 + j * 73 + 10 * math.sin(t * 4 + j)
        d.line((px, 583, px + 66, 569), fill=BLACK if j % 2 else WHITE, width=3)
    if int(t * 20) % 41 in (10, 11):
        d.rectangle((28, 305, 627, 313), fill=RED)
        d.rectangle((35, 325, 521, 327), fill=WHITE)
    d.rectangle((0, 591, w, h), fill=BLACK)
    d.text((26, 595), "VASSELL ENHA ATTHAYYA", font=font(21, mono=True), fill=WHITE)
    d.text((821, 595), "ADAPT // IMPROVE // OVERCOME", font=font(20, mono=True), fill=WHITE)
    if t >= 3.05:
        reveal = min(ease((t - 3.05) / .58), ease((5.95 - t) / .52))
        if reveal > .001:
            scene = oc_frame(w, h, "close")
            sd = ImageDraw.Draw(scene)
            poly(sd, [(10, 16), (630, 0), (563, 615), (0, 620)], BLACK, WHITE, 8)
            poly(sd, [(14, 35), (638, 0), (600, 122), (9, 171)], RED)
            type_layer(scene, "ADAPT", (56, 51), 113, WHITE, BLACK, angle=3, stroke=2)
            type_layer(scene, "IMPROVE", (32, 203), 91, RED, WHITE, angle=-3, stroke=3)
            type_layer(scene, "OVERCOME", (44, 342), 84, WHITE, RED, angle=3, stroke=2)
            sd = ImageDraw.Draw(scene)
            panel(sd, 48, 504, 515, 65, WHITE, 14, BLACK, 4)
            sd.text((77, 519), "VASSELL / PORTFOLIO", font=font(27, mono=True), fill=BLACK)
            if 3.6 < t < 3.78:
                scene = scene.transform((w, h), Image.Transform.AFFINE,
                                        (1, 0, round(3 * math.sin(t * 96)), 0, 1, 0),
                                        Image.Resampling.NEAREST)
            mask = Image.new("L", (w, h), 0)
            md = ImageDraw.Draw(mask)
            edge = -400 + 1830 * clamp(reveal)
            poly(md, [(-400, 0), (edge, 0), (edge - 270, h), (-400, h)], 255)
            im.paste(scene, (0, 0), mask)
    return im


def draw_dossier_oc(t):
    w, h = 1200, 480
    im = gfx_base(w, h, t, "dossier")
    d = ImageDraw.Draw(im)
    labels(d, w, "PROFESSIONAL PROFILE", 1)
    poly(d, [(24, 96), (790, 73), (748, 424), (32, 455)], BLACK, WHITE, 7)
    panel(d, 56, 105, 650, 61, RED, 17)
    d.text((76, 120), "VASSELL ENHA ATTHAYYA", font=font(33), fill=WHITE)
    type_layer(im, "ABOUT ME", (63, 171), 100, WHITE, RED, angle=3, stroke=3)
    d = ImageDraw.Draw(im)
    d.text((83, 314), "INFORMATION SYSTEMS", font=font(27, mono=True), fill=WHITE)
    d.text((83, 350), "TELKOM UNIVERSITY", font=font(27, mono=True), fill=WHITE)
    panel(d, 82, 401, 594, 43, WHITE, 12)
    d.text((104, 406), "DESIGN > DEVELOP > TEST > DEPLOY", font=font(22, mono=True), fill=BLACK)
    oc_panel(im, (793, 80, 390, 359), "portrait")
    d = ImageDraw.Draw(im)
    panel(d, 811, 402, 326, 47, RED, 11, WHITE, 3)
    d.text((840, 411), "IDENTITY / VASSELL", font=font(21, mono=True), fill=WHITE)
    return im


STACKS = [
    ("FRONTEND", "HTML  CSS  JAVASCRIPT  TYPESCRIPT  REACT  VUE  TAILWIND  FIGMA"),
    ("BACKEND", "PHP  LARAVEL  NODE.JS  MYSQL  PYTHON  REST API  RBAC"),
    ("TOOLS", "GIT  GITHUB  POSTMAN  VS CODE  DOCKER  CLOUD  LUA  ROBLOX"),
]


def draw_arsenal(t):
    w, h = 1200, 520
    im = gfx_base(w, h, t, "arsenal")
    d = ImageDraw.Draw(im)
    labels(d, w, "TECHNICAL SKILLS", 2)
    poly(d, [(45, 110), (797, 68), (725, 470), (60, 505)], BLACK, WHITE, 7)
    type_layer(im, "TECH", (61, 108), 113, WHITE, RED, angle=2)
    type_layer(im, "STACK", (89, 244), 105, RED, WHITE, angle=-3, stroke=3)
    d = ImageDraw.Draw(im)
    d.text((121, 392), "TOOLS / FRAMEWORKS / WORKFLOWS", font=font(24, mono=True), fill=WHITE)
    # Rotating glyph, orbit and moving target lines.
    cx, cy = 979, 286
    for j in range(4):
        r = 55 + j * 33
        d.arc((cx-r, cy-r, cx+r, cy+r),
              start=int(t * 20 + j * 35), end=int(t * 20 + j * 35 + 240),
              fill=WHITE if j % 2 else BLACK, width=5)
    for j in range(12):
        a = 2 * math.pi * j / 12 + t * .7
        x, y = cx + 142 * math.cos(a), cy + 142 * math.sin(a)
        d.rectangle((x-5, y-5, x+5, y+5), fill=BLACK)
    poly(d, [(947, 243), (1015, 243), (1033, 282), (981, 335), (931, 284)], BLACK, WHITE, 5)
    d.text((956, 265), "VX", font=font(33, mono=True), fill=WHITE)
    # Rapidly switch among actual stack categories.
    idx = int(t * .5) % len(STACKS)
    title, body = STACKS[idx]
    panel(d, 787, 426, 400, 51, WHITE, 10)
    d.text((812, 437), f"{title} // {idx+1:02d}/03", font=font(24, mono=True), fill=BLACK)
    # Small legible marquee lists below large title area.
    text = body
    d.text((812, 485), text[:55], font=font(14, mono=True), fill=WHITE)
    return im


def draw_missions(t):
    w, h = 1200, 284
    im = gfx_base(w, h, t, "missions")
    d = ImageDraw.Draw(im)
    panel(d, 22, 19, 518, 42, WHITE, 13)
    d.text((51, 25), "// 03  SELECTED PROJECTS", font=font(23, mono=True), fill=BLACK)
    poly(d, [(23, 75), (784, 37), (759, 243), (24, 266)], BLACK, WHITE, 6)
    type_layer(im, "PROJECTS", (52, 97), 106, WHITE, RED, angle=2, stroke=2)
    d = ImageDraw.Draw(im)
    panel(d, 868, 114, 270, 84, WHITE, 19, BLACK, 4)
    d.text((892, 129), "06  PROJECTS", font=font(27), fill=BLACK)
    d.text((892, 160), "VIEW DETAILS  >", font=font(21, mono=True), fill=RED)
    for i in range(5):
        x = 800 + i * 72
        y = 225 + math.sin(t * 4 + i) * 5
        poly(d, [(x, y), (x + 20, y - 10), (x + 41, y), (x + 20, y + 15)], BLACK, WHITE, 2)
    return im


def draw_pulse(t):
    w, h = 1200, 400
    im = gfx_base(w, h, t, "pulse")
    d = ImageDraw.Draw(im)
    labels(d, w, "DEVELOPMENT ACTIVITY", 4)
    poly(d, [(42, 97), (576, 87), (530, 373), (51, 388)], BLACK, WHITE, 7)
    type_layer(im, "ONGOING", (58, 119), 80, WHITE, RED, angle=2)
    type_layer(im, "PROGRESS", (72, 233), 72, RED, WHITE, angle=-3, stroke=3)
    d = ImageDraw.Draw(im)
    # Decorative activity cells deliberately do not claim real GitHub data.
    for i in range(17):
        for j in range(8):
            x, y = 640 + i * 31, 91 + j * 34
            n = (i * 7 + j * 13) % 11
            wave = math.sin(t * 2.1 - i * .27 - j * .44)
            fill = WHITE if (n + wave * 4) > 6 else BLACK if n < 2 else RED
            poly(d, [(x, y), (x + 26, y - 4), (x + 24, y + 20), (x, y + 25)], fill, BLACK, 2)
    d.text((693, 366), "ACTIVITY ILLUSTRATION / VIEW ACTUAL DATA", font=font(16, mono=True), fill=WHITE)
    return im


def draw_contact(t):
    w, h = 1200, 360
    im = gfx_base(w, h, t, "dossier")
    d = ImageDraw.Draw(im)
    labels(d, w, "CONTACT & COLLABORATION", 5)
    poly(d, [(39, 109), (863, 76), (814, 337), (61, 348)], BLACK, WHITE, 7)
    type_layer(im, "GET IN", (62, 111), 94, WHITE, RED, angle=2)
    type_layer(im, "TOUCH", (146, 202), 93, RED, WHITE, angle=-2, stroke=3)
    d = ImageDraw.Draw(im)
    # Envelopes that orbit a graphic dialogue bubble.
    cx, cy = 1032, 205
    d.ellipse((912, 93, 1149, 330), fill=WHITE, outline=BLACK, width=7)
    d.rectangle((961, 160, 1100, 240), fill=RED, outline=BLACK, width=7)
    d.line((968, 165, 1029, 211, 1098, 165), fill=BLACK, width=7)
    d.text((985, 248), "CONTACT", font=font(18, mono=True), fill=BLACK)
    for j in range(8):
        a = t * .6 + j * math.pi / 4
        x, y = cx + 115 * math.cos(a), cy + 115 * math.sin(a)
        d.ellipse((x-5, y-5, x+5, y+5), fill=RED, outline=BLACK, width=2)
    return im


def draw_outro(t):
    w, h = 1200, 378
    im = gfx_base(w, h, t, "outro")
    d = ImageDraw.Draw(im)
    poly(d, [(35, 34), (966, 22), (916, 337), (28, 350)], BLACK, WHITE, 7)
    type_layer(im, "BUILD WITH", (66, 62), 99, WHITE, RED, angle=2)
    type_layer(im, "PURPOSE.", (156, 188), 106, RED, WHITE, angle=-3, stroke=3)
    d = ImageDraw.Draw(im)
    for i in range(6):
        y = 24 + i * 62 + 5 * math.sin(t * 3 + i)
        poly(d, [(1013, y), (1146, y - 27), (1195, y + 13), (1061, y + 42)], BLACK if i%2 else WHITE)
    panel(d, 881, 286, 280, 48, WHITE, 10, BLACK, 3)
    d.text((912, 295), "THANK YOU FOR VISITING", font=font(17, mono=True), fill=BLACK)
    return im


PROJECTS = [
    ("01", "BRREAD!", "BUSINESS WEB APPLICATION", ["LARAVEL", "PHP", "MYSQL"], "A digital storefront and inventory workflow", "KWU-BRREAD"),
    ("02", "CATCH & CLASH", "ROBLOX GAME DEVELOPMENT", ["ROBLOX", "LUA", "GAME DEV"], "Gameplay systems and interactive experiences", "CatchAndClash_Roblox_Project"),
    ("03", "AMANIN", "AI ANTI-SCAM CONCEPT", ["AI", "PRODUCT", "SAFETY"], "AI-assisted anti-scam decision support", "AMANIN-Project"),
    ("04", "PHARVIA", "PHARMA TRACEABILITY", ["HEALTH", "PRODUCT", "TRACE"], "Pharmaceutical return and traceability", "PHARVIA-Project"),
    ("05", "VUE UI LAB", "INTERFACE EXPERIMENTS", ["VUE.JS", "ROUTING", "REST API"], "Components, state, routing and API integration", "PRAKTIKUM_UI-LANJUT_VASSELL-ENHA-ATTHAYYA_102042300140"),
    ("06", "MORE PROJECTS", "ALL REPOSITORIES", ["LARAVEL", "VUE", "LUA"], "Explore every other repository and experiment", "?tab=repositories"),
]


def project_card(idx, t=None):
    number, name, subtitle, tags, desc, repo = PROJECTS[idx]
    w, h = 640, 327
    im = Image.new("RGB", (w, h), WHITE if idx % 2 else RED)
    d = ImageDraw.Draw(im)
    darker = RED if idx % 2 else BLACK
    poly(d, [(0, 0), (640, 0), (610, 305), (0, 327)], darker)
    poly(d, [(405, 0), (640, 0), (640, 290), (474, 260)], WHITE if idx % 2 == 0 else BLACK)
    burst(d, 535, 132, 33, 204, 18, idx * .2, (RED, BLACK, WHITE))
    dot_field(d, (457, 37, 626, 254), 14, 2, idx, BLACK)
    panel(d, 18, 17, 290, 45, WHITE, 10)
    d.text((35, 24), f"PROJECT // {number}", font=font(22, mono=True), fill=BLACK)
    if len(name) > 12:
        sz = 51
    elif len(name) > 9:
        sz = 58
    else:
        sz = 72
    # Headline two-line room reserved for oversized game typography.
    type_layer(im, name, (11, 84), sz, WHITE if idx % 2 == 0 else BLACK,
               BLACK if idx % 2 == 0 else RED, angle=2, stroke=1)
    d = ImageDraw.Draw(im)
    d.text((43, 192), subtitle, font=font(22, mono=True), fill=WHITE if idx % 2 == 0 else BLACK)
    panel(d, 32, 232, 545, 46, BLACK if idx % 2 == 0 else RED, 11, WHITE, 3)
    d.text((49, 242), "  /  ".join(tags), font=font(18, mono=True), fill=WHITE)
    d.text((43, 289), "VIEW REPOSITORY  >", font=font(19, mono=True), fill=WHITE if idx%2==0 else BLACK)
    if t is not None:
        # A different moving scanner and graphic heartbeat in every dossier.
        sweep_x = 560 - (t / 3.5) * 590
        poly(d, [(sweep_x, 72), (sweep_x + 10, 73),
                 (sweep_x - 50, 224), (sweep_x - 60, 224)],
             RED if idx % 2 else WHITE)
        for k in range(3):
            yy = 277 + 4 * k + int(math.sin(t * 7 + k + idx) * 2)
            d.line((402, yy, 590, yy - 14), fill=WHITE if idx%2==0 else RED, width=2)
        if int(t * 12) % 23 in (4, 5):
            d.rectangle((38, 191, 395, 195), fill=BLACK if idx % 2 == 0 else RED)
    return im


def nav_card(index, label):
    im = Image.new("RGB", (230, 76), BLACK)
    d = ImageDraw.Draw(im)
    poly(d, [(3, 7), (220, 0), (207, 70), (0, 75)], RED if index % 2 else WHITE)
    poly(d, [(11, 16), (210, 9), (200, 62), (10, 67)], BLACK)
    d.text((25, 22), f"{index:02d} // {label}", font=font(20, mono=True), fill=WHITE)
    d.line((31, 58, 171, 55), fill=RED, width=3)
    return im


def draw_identity_board(t):
    """Three custom game-status cards replace the previous Markdown table."""
    w, h = 1200, 345
    im = Image.new("RGB", (w, h), BLACK)
    d = ImageDraw.Draw(im)
    dot_field(d, (0, 0, w, h), 24, 2.5, color=RED, wobble=t)
    items = [
        ("01 / PROFILE", ["VASSELL", "ENHA ATTHAYYA", "FULL-STACK DEVELOPER"], WHITE, BLACK),
        ("02 / EDUCATION", ["TELKOM", "INFORMATION SYSTEMS", "UI/UX + PRODUCT"], RED, WHITE),
        ("03 / INTERESTS", ["ROBLOX / LUA", "DOCKER + CLOUD", "CONTINUOUS LEARNING"], WHITE, BLACK),
    ]
    for i, (label, lines, bg, fg) in enumerate(items):
        x = 17 + i * 398
        top = 26 + 6 * math.sin(t * 2 + i)
        poly(d, [(x + 22, top), (x + 390, top - 9), (x + 364, top + 292),
                 (x, top + 315)], bg, BLACK if i != 1 else WHITE, 5)
        panel(d, x + 24, top + 26, 330, 47, BLACK, 9)
        d.text((x + 42, top + 35), label, font=font(20, mono=True), fill=WHITE)
        d.text((x + 30, top + 110), lines[0], font=font(47 if len(lines[0]) < 10 else 32), fill=fg)
        d.line((x + 29, top + 178, x + 328, top + 163), fill=fg, width=6)
        d.text((x + 30, top + 200), lines[1], font=font(22, mono=True), fill=fg)
        d.text((x + 30, top + 243), lines[2], font=font(20, mono=True), fill=fg)
    return im


def draw_skill_board(t):
    """A dense, carefully readable arsenal interface without HTML tables."""
    w, h = 1200, 440
    im = Image.new("RGB", (w, h), BLACK)
    d = ImageDraw.Draw(im)
    burst(d, 593, 224, 70, 720, 28, t * .017, (RED, BLACK, WHITE))
    cards = [
        ("FRONTEND", ["HTML / CSS", "JAVASCRIPT / TYPESCRIPT", "REACT / VUE", "TAILWIND CSS / FIGMA"], WHITE, BLACK),
        ("BACKEND", ["PHP / LARAVEL", "NODE.JS / MYSQL", "PYTHON / REST API", "ROLE-BASED ACCESS"], RED, WHITE),
        ("WORKBENCH", ["GIT / GITHUB", "POSTMAN / VS CODE", "DOCKER / CLOUD", "LUA / ROBLOX STUDIO"], BLACK, WHITE),
    ]
    for i, (title, rows, bg, fg) in enumerate(cards):
        x = 10 + i * 396
        y = 12 + round(4 * math.sin(t * 3 + i))
        poly(d, [(x + 24, y), (x + 385, y + 4), (x + 359, y + 408),
                 (x, y + 430)], bg, WHITE if bg == BLACK else BLACK, 5)
        panel(d, x + 24, y + 19, 338, 66, RED if bg != RED else BLACK, 11)
        d.text((x + 44, y + 33), f"0{i+1}  {title}", font=font(30), fill=WHITE)
        for j, row in enumerate(rows):
            yy = y + 124 + j * 65
            d.text((x + 38, yy), row, font=font(22 if len(row) < 20 else 20, mono=True), fill=fg)
            d.line((x + 36, yy + 38, x + 316, yy + 27), fill=fg, width=2)
        marker = x + 42 + 240 * ((t * .37 + i * .17) % 1)
        d.ellipse((marker - 8, y + 393, marker + 8, y + 409), fill=RED if bg != RED else WHITE)
    return im


def draw_bio_manifesto(t):
    w, h = 1200, 275
    im = gfx_base(w, h, t, "dossier")
    d = ImageDraw.Draw(im)
    poly(d, [(28, 16), (842, 4), (795, 253), (20, 268)], BLACK, WHITE, 7)
    panel(d, 50, 29, 624, 45, RED, 10)
    d.text((68, 39), "//  VASSELL / PROFESSIONAL OVERVIEW", font=font(22, mono=True), fill=WHITE)
    d.text((67, 101), "FROM CONCEPT", font=font(62), fill=WHITE)
    d.text((68, 170), "TO IMPLEMENTATION.", font=font(45), fill=RED)
    d.text((74, 231), "DESIGN  >  DEVELOPMENT  >  DEPLOYMENT", font=font(19, mono=True), fill=WHITE)
    oc_panel(im, (839, 18, 350, 250), "portrait")
    return im


def draw_status_link(t):
    w, h = 1200, 176
    im = Image.new("RGB", (w, h), RED)
    d = ImageDraw.Draw(im)
    burst(d, 1040, 90, 30, 410, 21, t * .05, (BLACK, RED, WHITE))
    poly(d, [(16, 24), (1112, 0), (1071, 153), (10, 171)], BLACK, WHITE, 7)
    type_layer(im, "GITHUB DEVELOPMENT ACTIVITY", (38, 36), 52, WHITE, RED, angle=1)
    d = ImageDraw.Draw(im)
    d.text((72, 125), "VIEW CONTRIBUTIONS AND REPOSITORIES >", font=font(22, mono=True), fill=WHITE)
    return im


LINKS = [
    ("01", "GITHUB", "@vassellenha"),
    ("02", "LINKEDIN", "VASSELL ENHA ATTHAYYA"),
    ("03", "INSTAGRAM", "@vassellenha"),
    ("04", "PORTFOLIO", "EXPLORE THE WORK"),
]


def draw_link_card(i, t):
    n, label, secondary = LINKS[i]
    w, h = 560, 154
    im = Image.new("RGB", (w, h), WHITE if i % 2 else RED)
    d = ImageDraw.Draw(im)
    poly(d, [(0, 5), (552, 0), (536, 148), (6, 153)], BLACK, WHITE, 5)
    panel(d, 23, 17, 98, 42, WHITE, 8)
    d.text((40, 26), f"//{n}", font=font(20, mono=True), fill=BLACK)
    d.text((142, 13), label, font=font(51 if len(label) < 9 else 44), fill=WHITE)
    d.text((39, 103), secondary, font=font(19, mono=True), fill=WHITE)
    x = 510 - 20 * ((t * 2) % 1)
    poly(d, [(x - 36, 101), (x + 4, 101), (x + 16, 114),
             (x + 4, 128), (x - 36, 128)], RED, WHITE, 3)
    return im


ANIMATIONS = [
    ("01-phantom-hero", draw_hero_oc, 6.0),
    ("02-personnel-dossier", draw_dossier_oc, 6.0),
    ("02b-identity-board", draw_identity_board, 5.0),
    ("02c-bio-manifesto", draw_bio_manifesto, 5.0),
    ("03-phantom-arsenal", draw_arsenal, 6.0),
    ("03b-skill-board", draw_skill_board, 5.0),
    ("04-mission-select", draw_missions, 5.0),
    ("05-operation-pulse", draw_pulse, 6.0),
    ("05b-status-link", draw_status_link, 5.0),
    ("06-social-link", draw_contact, 5.0),
    ("07-professional-finale", draw_outro, 6.0),
]


def encode_gif(folder, destination, fps):
    # Palette-aware GIFs: render each full-color master frame before quantization.
    palette = folder / "palette.png"
    input_pattern = str(folder / "%04d.png")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-framerate", str(fps), "-i", input_pattern,
                    "-vf", "palettegen=stats_mode=diff", str(palette)], check=True)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-framerate", str(fps), "-i", input_pattern,
                    "-i", str(palette), "-filter_complex",
                    "[0:v][1:v]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle",
                    "-loop", "0", str(destination)], check=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--fps", type=int, default=20)
    p.add_argument("--only", help="partial animation name or 'static'")
    p.add_argument("--preview-only", action="store_true", help="save first frames, skip GIF")
    p.add_argument("--cards", action="store_true", help="render 6 animated project cards")
    args = p.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "motion").mkdir(exist_ok=True)
    (OUT / "posters").mkdir(exist_ok=True)
    (OUT / "navigation").mkdir(exist_ok=True)
    (OUT / "links").mkdir(exist_ok=True)

    if args.only is None or args.only == "static":
        for i in range(6):
            project_card(i).save(OUT / "posters" / f"mission-{i+1:02d}.png", optimize=True)
        for i, name in enumerate(("ABOUT", "SKILLS", "PROJECTS", "ACTIVITY", "CONTACT"), 1):
            nav_card(i, name).save(OUT / "navigation" / f"nav-{i:02d}.png", optimize=True)
        print("Rendered 6 mission cards and 5 navigation cards", flush=True)
        if args.only == "static":
            return

    if args.cards:
        for i in range(6):
            dest = OUT / "posters" / f"mission-{i+1:02d}.gif"
            with tempfile.TemporaryDirectory(prefix="phantom-card-") as td:
                frames = Path(td)
                for k in range(int(3.5 * args.fps)):
                    project_card(i, k / args.fps).save(frames / f"{k:04d}.png")
                encode_gif(frames, dest, args.fps)
            print(f"Animated {dest.relative_to(ROOT)} ({dest.stat().st_size/1048576:.1f} MiB)", flush=True)
        for i in range(4):
            dest = OUT / "links" / f"contact-{i+1:02d}.gif"
            with tempfile.TemporaryDirectory(prefix="phantom-link-") as td:
                frames = Path(td)
                for k in range(int(3 * args.fps)):
                    draw_link_card(i, k / args.fps).save(frames / f"{k:04d}.png")
                encode_gif(frames, dest, args.fps)
            print(f"Animated {dest.relative_to(ROOT)} ({dest.stat().st_size/1048576:.1f} MiB)", flush=True)
    for name, renderer, seconds in ANIMATIONS:
        if args.only and args.only not in name:
            continue
        dest = OUT / "motion" / (name + ".gif")
        sample = renderer(seconds * .37)
        sample.save(OUT / "motion" / (name + "-preview.png"), optimize=True)
        if args.preview_only:
            print(f"Previewed {name}", flush=True)
            continue
        with tempfile.TemporaryDirectory(prefix="phantom-frames-") as td:
            frames = Path(td)
            for k in range(int(seconds * args.fps)):
                t = seconds * k / (seconds * args.fps)
                frame = renderer(t)
                frame.save(frames / f"{k:04d}.png")
            encode_gif(frames, dest, args.fps)
        print(f"Rendered {dest.relative_to(ROOT)} ({dest.stat().st_size/1048576:.1f} MiB)", flush=True)


if __name__ == "__main__":
    main()
