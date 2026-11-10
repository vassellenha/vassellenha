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
    d.text((w - 245, y + 11), "CCELL / 2026", font=font(20, mono=True), fill=WHITE)


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


def draw_masked_figure(im, center, scale, t):
    """Original fictional phantom-mask silhouette; no real person's likeness."""
    w, h = im.size
    layer = Image.new("RGBA", (700, 710), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # Cropped fan and speed lines behind the body.
    burst(d, 340, 355, 50, 350, 37, .04 + t * .015, (BLACK, RED, WHITE))
    # Coat silhouette, polygonal lapels, arms, scarf.
    poly(d, [(250, 340), (125, 410), (64, 635), (608, 680), (545, 435),
             (438, 348), (405, 284)], BLACK, WHITE, 7)
    poly(d, [(250, 355), (330, 563), (218, 633), (156, 429)], WHITE)
    poly(d, [(434, 351), (358, 582), (510, 607), (536, 420)], WHITE)
    poly(d, [(282, 340), (358, 560), (423, 343)], RED)
    # High-collar black jacket details.
    poly(d, [(168, 465), (272, 423), (326, 602), (206, 548)], BLACK)
    poly(d, [(474, 425), (389, 602), (510, 558), (561, 493)], BLACK)
    d.line((209, 520, 322, 615), fill=RED, width=11)
    d.line((488, 512, 387, 621), fill=RED, width=11)
    # Neck and face.
    poly(d, [(270, 264), (446, 263), (430, 410), (350, 472), (267, 396)], WHITE, BLACK, 7)
    poly(d, [(272, 267), (442, 271), (416, 378), (347, 417), (282, 358)], WHITE)
    # Hair with very graphic jagged tufts.
    poly(d, [(253, 295), (238, 189), (272, 231), (278, 143), (302, 187),
             (346, 123), (358, 171), (417, 143), (408, 199), (472, 185),
             (445, 301), (410, 277), (386, 218), (345, 253), (298, 248)], BLACK, WHITE, 6)
    # Trademark-free angular phantom eye mask.
    poly(d, [(276, 298), (329, 278), (350, 305), (378, 275), (434, 299),
             (420, 353), (367, 344), (342, 349), (283, 344)], BLACK)
    poly(d, [(287, 306), (330, 309), (340, 330), (301, 328)], WHITE)
    poly(d, [(372, 306), (420, 307), (409, 331), (367, 326)], WHITE)
    # Eyes pulse red only on a couple of frames.
    if (int(t * 12) % 29) in (0, 1, 2):
        d.ellipse((314, 313, 329, 324), fill=RED)
        d.ellipse((383, 312, 397, 323), fill=RED)
    d.line((332, 380, 383, 380), fill=BLACK, width=5)
    # Shattered calling card held near collar.
    poly(d, [(467, 352), (590, 320), (618, 421), (492, 447)], WHITE, BLACK, 6)
    d.text((495, 361), "TAKE", fill=BLACK, font=font(24))
    d.text((496, 390), "HEART", fill=RED, font=font(25))
    # Enlarged illustration clipped deliberately at the bottom.
    nw, nh = int(700 * scale), int(710 * scale)
    layer = layer.resize((nw, nh), Image.Resampling.LANCZOS)
    im.paste(layer, (int(center[0] - nw / 2), int(center[1] - nh / 2)), layer)


def draw_hero(t):
    w, h = 1280, 620
    im = gfx_base(w, h, t, "hero")
    d = ImageDraw.Draw(im)
    # Sweeping title billboard with animated stripes.
    poly(d, [(18, 104), (770, 44), (711, 516), (20, 554)], BLACK, WHITE, 8)
    poly(d, [(24, 123), (760, 63), (737, 147), (20, 212)], RED)
    panel(d, 33, 35, 494, 51, WHITE, 9)
    d.text((54, 44), "STEALING BUGS / SHIPPING DREAMS", font=font(24, mono=True), fill=BLACK)
    d.text((86, 123), "THE PHANTOM", font=font(40), fill=WHITE)
    # Multi-plane typographic motion.
    bounce = 3 * math.sin(t * 3.0)
    type_layer(im, "VASSELL", (32 + bounce, 182), 155, WHITE, RED, angle=3,
               stroke=3, stroke_fill=BLACK, skew=-.07)
    type_layer(im, "ENHA", (73 - bounce, 351), 121, WHITE, RED, angle=-3,
               stroke=3, stroke_fill=BLACK, skew=-.07)
    d = ImageDraw.Draw(im)
    panel(d, 61, 518, 684, 56, RED, 20, WHITE, 4)
    d.text((90, 527), "FULL-STACK  /  UI-UX  /  GAME DEV", font=font(26, mono=True), fill=WHITE)
    draw_masked_figure(im, (990, 365 + 3 * math.sin(t * 2.2)), .96, t)
    d = ImageDraw.Draw(im)
    poly(d, [(798, 493), (1260, 440), (1280, 492), (810, 554)], RED)
    type_layer(im, "CCELL.exe", (828, 483), 42, BLACK, WHITE, angle=5)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 596, w, h), fill=WHITE)
    d.text((22, 597), "// WELCOME TO MY PALACE", font=font(18, mono=True), fill=BLACK)
    d.text((830, 597), "SYSTEM 05 / MAXIMUM STYLE", font=font(18, mono=True), fill=BLACK)
    # Analog glitch line flickers, rare frame flashes.
    if int(t * 12) % 37 in (19, 20):
        for yy in [176, 239, 433]:
            d.rectangle((32, yy, 768, yy + 6), fill=RED if yy % 2 else WHITE)
    # Glint restricted to the top edge so it never obscures the main lettering.
    xx = (t / 6) * 1580 - 140
    poly(d, [(xx, 0), (xx + 18, 0), (xx - 7, 98), (xx - 25, 98)], WHITE)
    # Second act: a complete calling-card impact shot, pushed in with a diagonal
    # comic-panel wipe, then withdrawn before the loop restarts.
    if t >= 3.20:
        enter = ease((t - 3.20) / .52)
        leave = ease((5.95 - t) / .58)
        reveal = clamp(min(enter, leave))
        if reveal > .001:
            scene = Image.new("RGB", (w, h), WHITE)
            sd = ImageDraw.Draw(scene)
            burst(sd, 651, 314, 29, 1100, 43, .15 + t * .15,
                  (RED, BLACK, WHITE))
            dot_field(sd, (25, 50, 1270, 585), step=28, radius=3,
                      seed=9, color=BLACK, wobble=t * 2)
            poly(sd, [(32, 76), (1082, 18), (1022, 520), (20, 589)], BLACK, WHITE, 12)
            poly(sd, [(38, 91), (1043, 39), (1022, 175), (31, 233)], RED)
            type_layer(scene, "I DON'T JUST", (52, 92), 78, WHITE, BLACK,
                       angle=2, stroke=2)
            type_layer(scene, "WRITE CODE.", (80, 203), 102, WHITE, RED,
                       angle=-2, stroke=3)
            type_layer(scene, "I STEAL", (122, 355), 89, RED, WHITE,
                       angle=3, stroke=3)
            sd = ImageDraw.Draw(scene)
            panel(sd, 809, 428, 398, 84, WHITE, 20, BLACK, 6)
            sd.text((845, 444), "THE IMPOSSIBLE.", font=font(39), fill=BLACK)
            sd.rectangle((0, 590, w, h), fill=RED)
            sd.text((32, 594), "CCELL / MISSION IN PROGRESS", font=font(22, mono=True), fill=WHITE)
            # Slight shake only during the impact moment.
            if 3.68 < t < 3.88:
                scene = scene.transform((w, h), Image.Transform.AFFINE,
                                        (1, 0, int(4 * math.sin(t * 95)), 0, 1,
                                         int(3 * math.cos(t * 81))),
                                        Image.Resampling.NEAREST)
            mask = Image.new("L", (w, h), 0)
            md = ImageDraw.Draw(mask)
            edge = -240 + reveal * 1800
            poly(md, [(-300, 0), (edge, 0), (edge - 260, h), (-300, h)], 255)
            im.paste(scene, (0, 0), mask)
    return im


def draw_dossier(t):
    w, h = 1200, 480
    im = gfx_base(w, h, t, "dossier")
    d = ImageDraw.Draw(im)
    labels(d, w, "PERSONNEL DOSSIER", 1)
    poly(d, [(17, 92), (844, 72), (795, 421), (33, 455)], BLACK, WHITE, 7)
    panel(d, 62, 97, 650, 59, RED, 19)
    d.text((82, 104), "V A S S E L L    E N H A    A T T H A Y Y A", font=font(27), fill=WHITE)
    type_layer(im, "LEVEL UP", (66, 150), 104, WHITE, RED, angle=3, stroke=3)
    d = ImageDraw.Draw(im)
    d.text((79, 310), "INFORMATION SYSTEMS  /  TELKOM UNIVERSITY", font=font(25, mono=True), fill=WHITE)
    panel(d, 78, 354, 623, 59, WHITE, 17)
    d.text((108, 367), "DESIGN  >  BUILD  >  TEST  >  SHIP", font=font(25, mono=True), fill=BLACK)
    # Original RPG-like paper-cut ID silhouette.
    d.ellipse((891, 102, 1189, 400), fill=BLACK, outline=WHITE, width=8)
    burst(d, 1042, 250, 53, 200, 24, t * .06, (RED, BLACK, WHITE))
    poly(d, [(961, 361), (994, 274), (1089, 274), (1121, 368)], BLACK, WHITE, 5)
    d.ellipse((1000, 174, 1083, 286), fill=WHITE, outline=BLACK, width=6)
    poly(d, [(989, 209), (1007, 162), (1050, 143), (1086, 185), (1093, 220),
             (1055, 198), (1029, 225)], BLACK)
    poly(d, [(1008, 238), (1037, 227), (1063, 237), (1075, 249), (1040, 260)], RED)
    d.text((896, 412), "IDENTITY: CCELL / ACTIVE", font=font(18, mono=True), fill=WHITE)
    # Red flashing 'classified' angled stamp.
    if math.sin(t * 3.5) > -.4:
        type_layer(im, "CONFIDENTIAL", (850, 62), 29, RED, BLACK, angle=-13, stroke=2)
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
    labels(d, w, "PHANTOM ARSENAL", 2)
    poly(d, [(45, 110), (797, 68), (725, 470), (60, 505)], BLACK, WHITE, 7)
    type_layer(im, "SKILL", (61, 108), 113, WHITE, RED, angle=2)
    type_layer(im, "CARDS", (89, 244), 105, RED, WHITE, angle=-3, stroke=3)
    d = ImageDraw.Draw(im)
    d.text((121, 392), "CHOOSE YOUR LOADOUT  //  NO AUTO-EQUIP", font=font(24, mono=True), fill=WHITE)
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
    d.text((51, 25), "// 03  THE MISSION BOARD", font=font(23, mono=True), fill=BLACK)
    poly(d, [(23, 75), (784, 37), (759, 243), (24, 266)], BLACK, WHITE, 6)
    type_layer(im, "SELECT", (52, 97), 106, WHITE, RED, angle=2, stroke=2)
    d = ImageDraw.Draw(im)
    panel(d, 868, 114, 270, 84, WHITE, 19, BLACK, 4)
    d.text((892, 129), "06  MISSIONS", font=font(27), fill=BLACK)
    d.text((892, 160), "OPEN FILES  >", font=font(21, mono=True), fill=RED)
    for i in range(5):
        x = 800 + i * 72
        y = 225 + math.sin(t * 4 + i) * 5
        poly(d, [(x, y), (x + 20, y - 10), (x + 41, y), (x + 20, y + 15)], BLACK, WHITE, 2)
    return im


def draw_pulse(t):
    w, h = 1200, 400
    im = gfx_base(w, h, t, "pulse")
    d = ImageDraw.Draw(im)
    labels(d, w, "OPERATION: CONTINUOUS BUILD", 4)
    poly(d, [(42, 97), (576, 87), (530, 373), (51, 388)], BLACK, WHITE, 7)
    type_layer(im, "NEVER", (68, 119), 101, WHITE, RED, angle=2)
    type_layer(im, "STOP.", (80, 233), 93, RED, WHITE, angle=-3, stroke=3)
    d = ImageDraw.Draw(im)
    # Decorative activity cells deliberately do not claim real GitHub data.
    for i in range(17):
        for j in range(8):
            x, y = 640 + i * 31, 91 + j * 34
            n = (i * 7 + j * 13) % 11
            wave = math.sin(t * 2.1 - i * .27 - j * .44)
            fill = WHITE if (n + wave * 4) > 6 else BLACK if n < 2 else RED
            poly(d, [(x, y), (x + 26, y - 4), (x + 24, y + 20), (x, y + 25)], fill, BLACK, 2)
    d.text((693, 366), "DECORATIVE GRID / SEE LIVE DATA BELOW", font=font(17, mono=True), fill=WHITE)
    return im


def draw_contact(t):
    w, h = 1200, 360
    im = gfx_base(w, h, t, "dossier")
    d = ImageDraw.Draw(im)
    labels(d, w, "SOCIAL LINK UNLOCKED", 5)
    poly(d, [(39, 109), (863, 76), (814, 337), (61, 348)], BLACK, WHITE, 7)
    type_layer(im, "LET'S", (62, 111), 94, WHITE, RED, angle=2)
    type_layer(im, "CONNECT!", (146, 202), 93, RED, WHITE, angle=-2, stroke=3)
    d = ImageDraw.Draw(im)
    # Envelopes that orbit a graphic dialogue bubble.
    cx, cy = 1032, 205
    d.ellipse((912, 93, 1149, 330), fill=WHITE, outline=BLACK, width=7)
    d.rectangle((961, 160, 1100, 240), fill=RED, outline=BLACK, width=7)
    d.line((968, 165, 1029, 211, 1098, 165), fill=BLACK, width=7)
    d.text((985, 248), "PING ME", font=font(18, mono=True), fill=BLACK)
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
    type_layer(im, "STEAL THE", (66, 62), 107, WHITE, RED, angle=2)
    type_layer(im, "SHOW.", (156, 188), 106, RED, WHITE, angle=-3, stroke=3)
    d = ImageDraw.Draw(im)
    for i in range(6):
        y = 24 + i * 62 + 5 * math.sin(t * 3 + i)
        poly(d, [(1013, y), (1146, y - 27), (1195, y + 13), (1061, y + 42)], BLACK if i%2 else WHITE)
    panel(d, 881, 286, 280, 48, WHITE, 10, BLACK, 3)
    d.text((912, 295), "TO BE CONTINUED...", font=font(20, mono=True), fill=BLACK)
    return im


PROJECTS = [
    ("01", "BRREAD!", "BUSINESS WEB APPLICATION", ["LARAVEL", "PHP", "MYSQL"], "A digital storefront and inventory workflow", "KWU-BRREAD"),
    ("02", "CATCH & CLASH", "ROBLOX GAME DEVELOPMENT", ["ROBLOX", "LUA", "GAME DEV"], "Gameplay systems and interactive experiences", "CatchAndClash_Roblox_Project"),
    ("03", "AMANIN", "AI ANTI-SCAM CONCEPT", ["AI", "PRODUCT", "SAFETY"], "AI-assisted anti-scam decision support", "AMANIN-Project"),
    ("04", "PHARVIA", "PHARMA TRACEABILITY", ["HEALTH", "PRODUCT", "TRACE"], "Pharmaceutical return and traceability", "PHARVIA-Project"),
    ("05", "VUE UI LAB", "INTERFACE EXPERIMENTS", ["VUE.JS", "ROUTING", "REST API"], "Components, state, routing and API integration", "PRAKTIKUM_UI-LANJUT_VASSELL-ENHA-ATTHAYYA_102042300140"),
    ("06", "MORE MISSIONS", "THE FULL ARCHIVE", ["LARAVEL", "VUE", "LUA"], "Explore every other repository and experiment", "?tab=repositories"),
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
    d.text((35, 24), f"MISSION // {number}", font=font(22, mono=True), fill=BLACK)
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
    d.text((43, 289), "OPEN DOSSIER  >", font=font(19, mono=True), fill=WHITE if idx%2==0 else BLACK)
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


ANIMATIONS = [
    ("01-phantom-hero", draw_hero, 6.0),
    ("02-personnel-dossier", draw_dossier, 6.0),
    ("03-phantom-arsenal", draw_arsenal, 6.0),
    ("04-mission-select", draw_missions, 5.0),
    ("05-operation-pulse", draw_pulse, 6.0),
    ("06-social-link", draw_contact, 5.0),
    ("07-steal-the-show", draw_outro, 6.0),
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
    p.add_argument("--cards", action="store_true", help="render 6 animated mission dossiers")
    args = p.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "motion").mkdir(exist_ok=True)
    (OUT / "posters").mkdir(exist_ok=True)
    (OUT / "navigation").mkdir(exist_ok=True)

    if args.only is None or args.only == "static":
        for i in range(6):
            project_card(i).save(OUT / "posters" / f"mission-{i+1:02d}.png", optimize=True)
        for i, name in enumerate(("ABOUT", "ARSENAL", "MISSIONS", "STATUS", "CONTACT"), 1):
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
