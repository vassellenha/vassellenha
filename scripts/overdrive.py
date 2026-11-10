#!/usr/bin/env python3
"""Vassell / Absolute Overdrive V5: original GitHub-ready motion artwork.

The user's original character is composited ONLY in the hero sequence.
Every other graphic uses original procedural typography, geometry and symbols.
GIF rendering is intentionally deterministic; browser scripts are not required.
"""

from __future__ import annotations

import argparse
import math
import random
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from graphics_core import BLACK, BRIGHT, GRAY, INK, RED, WHITE, YELLOW
from graphics_core import burst, clamp, dot_field, ease, font, oc_frame, panel, poly, scratch, type_layer

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'overdrive5'
R = RED
K = BLACK
W = WHITE
P = (235, 228, 211)
S = (145, 148, 165)
GOLD = (253, 195, 49)
BLUE = (65, 154, 186)
SPEED = 2 * math.pi


def clock(t, duration=4.0):
    return (t / duration) % 1.0


def pulse(t, freq=1, phase=0):
    return .5 + .5 * math.sin(SPEED * (freq * t + phase))


def polygon(d, points, fill, stroke=None, width=4):
    poly(d, points, fill, stroke, width)


def text(d, value, xy, size, color=W, maxwidth=None, mono=False, anchor=None):
    f = font(size, mono=mono)
    if maxwidth:
        while d.textbbox((0, 0), value, font=f)[2] > maxwidth and size > 13:
            size -= 1
            f = font(size, mono=mono)
    d.text(xy, value, font=f, fill=color, anchor=anchor)


def line(d, coords, fill=W, width=4):
    d.line(coords, fill=fill, width=width, joint='curve')


def box(d, rect, fill, outline=None, thick=3):
    d.rectangle(rect, fill=fill, outline=outline, width=thick)


def ring(d, cx, cy, radius, t, n=7, fg=W, thickness=5, spin=1):
    for j in range(n):
        a = t * spin * 45 + j * (360 / n)
        d.arc((cx-radius,cy-radius,cx+radius,cy+radius), a, a+18+5*(j%3), fill=fg, width=thickness)


def rays(d, cx, cy, t, count=18, inner=35, outer=350, color=W):
    for i in range(count):
        a = (i / count) * SPEED + .02 * t
        x1, y1 = cx + inner*math.cos(a), cy + inner*math.sin(a)
        x2, y2 = cx + outer*math.cos(a+.01), cy + outer*math.sin(a+.01)
        line(d, (x1,y1,x2,y2), color, 3 if i%4 else 6)


def slashes(d, w, h, t, count=22, color=R):
    rnd = random.Random(132)
    for i in range(count):
        x = rnd.randint(-200,w+200)+30*math.sin(t*2.5+i*.3)
        y = rnd.randint(-100,h+90)
        size = rnd.randint(12,95)
        line(d,(x,y,x+size,y-size*.34),color,1+(i%3))


def grid(d, x0, y0, cols, rows, cell, t, accent=R):
    for i in range(cols):
        for j in range(rows):
            x, y = x0+i*cell, y0+j*cell
            k = (.5+.5*math.sin(t*2+i*.3-j*.6))
            sz = 2+4*k
            d.ellipse((x-sz,y-sz,x+sz,y+sz),fill=accent if (i+j)%3 else W)


def print_texture(im, t, variant=0):
    d = ImageDraw.Draw(im)
    w,h=im.size
    rnd = random.Random(70+variant)
    for j in range(58):
        x=rnd.randrange(0,w); y=rnd.randrange(0,h)
        n=(j%4)+1
        line(d,(x,y,x+5+n*2,y-2),W if j%3 else R,1)
    for j in range(13):
        x=round(w*(j/13))
        line(d,(x,h-4,x+43+10*math.sin(t+j),h-9),W if j%2 else K,1)


def base(w,h,t,variant=0):
    im=Image.new('RGB',(w,h),K if variant%3!=1 else W)
    d=ImageDraw.Draw(im)
    if variant%3==0:
        polygon(d,[(0,0),(w*.58,0),(w*.34,h),(0,h)],R)
        polygon(d,[(w*.7,0),(w,0),(w,h),(w*.91,h*.77)],W)
        polygon(d,[(0,h*.79),(w*.5,h*.6),(w*.33,h),(0,h)],K)
    elif variant%3==1:
        polygon(d,[(0,0),(w*.77,0),(w*.65,h),(0,h)],W)
        polygon(d,[(w*.52,0),(w,0),(w,h),(w*.67,h)],R)
        polygon(d,[(w*.1,h*.7),(w*.46,h*.52),(w*.8,h)],K)
    else:
        polygon(d,[(0,0),(w*.44,0),(w*.18,h),(0,h)],R)
        polygon(d,[(w*.53,h*.07),(w,h*.0),(w,h),(w*.64,h)],R)
        polygon(d,[(w*.15,h),(w*.53,h*.4),(w*.92,h)],W)
    slashes(d,w,h,t,count=32,color=K if variant==1 else W)
    print_texture(im,t,variant)
    return im


def label(d, number, title, w, dark=True):
    primary=K if dark else W
    paper=W if dark else K
    polygon(d,[(20,15),(min(700,w-27),8),(min(677,w-50),61),(14,68)],paper,R,4)
    text(d,f'// {number:02d}  {title}',(42,22),26,primary,mono=True,maxwidth=w-110)


def signature(d,w,h,t):
    polygon(d,[(0,h-34),(w,h-43),(w,h),(0,h)],K)
    text(d,'VASSELL ENHA ATTHAYYA',(23,h-30),16,W,mono=True)
    txt='DESIGN  /  DEVELOPMENT  /  IMPLEMENTATION'
    text(d,txt,(w-620,h-30),16,W,mono=True,maxwidth=603)
    for j in range(6):
        x=w-55-j*20
        d.rectangle((x,h-8,x+9,h-3),fill=R if j==(int(t*4)%6) else W)


def anim_title(im,title,xy,size,t,phase=0,white=W,shadow=R,angle=2):
    dx = 7*math.sin(t*2.2+phase)
    type_layer(im,title,(xy[0]+dx,xy[1]),size,white,shadow,angle=angle,stroke=2,stroke_fill=K)


def origami(d,cx,cy,s,t,fg=W,edge=K):
    wob=math.sin(t*2.7)*s*.025
    polygon(d,[(cx,cy-s*.7),(cx+s*.61,cy-s*.11+wob),(cx+s*.22,cy+s*.73),
               (cx-s*.65,cy+s*.16+wob)],fg,edge,6)
    line(d,(cx,cy-s*.7,cx+s*.04,cy+s*.28,cx+s*.22,cy+s*.73),edge,4)
    line(d,(cx-s*.65,cy+s*.16,cx+s*.04,cy+s*.28,cx+s*.61,cy-s*.11),edge,4)


def circuit(d,x,y,w,h,t):
    rnd=random.Random(91)
    for j in range(11):
        yy=y+23+j*(h-46)/10
        k=rnd.randint(40,int(w*.5))
        line(d,(x,yy,x+k,yy,x+k+17,yy+12,x+w,yy+12),R if j%3==0 else W,2)
        xx=x+(t*41+j*49)%w
        d.ellipse((xx-4,yy-4,xx+4,yy+4),fill=GOLD)


def draw_hero(t):
    """ONLY image renderer in this entire script that reads the OC photograph."""
    w,h=1280,620
    im=oc_frame(w,h,'wide')
    d=ImageDraw.Draw(im)
    polygon(d,[(0,0),(692,0),(608,576),(0,619)],K,W,11)
    polygon(d,[(0,0),(655,0),(628,134),(0,200)],R)
    # Keep the OC's face unobstructed: motion lines stay in the far-right margin.
    for j in range(14):
        yy=(j*47+int(t*17))%580
        if j%3==0: line(d,(1160,yy,1277,yy-45),W if j%2 else K,3)
    label(d,0,'PORTFOLIO / IDENTITY SYSTEM',w)
    if t < 2.7:
        anim_title(im,'VASSELL',(29,182),135,t,white=W,shadow=R)
        d=ImageDraw.Draw(im)
        polygon(d,[(43,385),(624,385),(606,456),(36,459)],R,W,5)
        text(d,'FULL-STACK  /  UI-UX',(67,401),34,W,mono=True)
        text(d,'DESIGN. DEVELOP. DEPLOY.',(55,491),30,W,mono=True)
    else:
        anim_title(im,'ADAPT',(45,115),110,t,white=W,shadow=K)
        anim_title(im,'IMPROVE',(50,244),96,t,white=R,shadow=W,angle=-2)
        anim_title(im,'OVERCOME',(28,365),83,t,white=W,shadow=R)
    # Red-white action flash is intentionally restricted to the hero.
    if .12 < (t%1.9) < .17:
        line(d,(20,315,665,273),W,9)
    signature(ImageDraw.Draw(im),w,h,t)
    return im


def draw_about(t):
    w,h=1200,520
    im=base(w,h,t,0);d=ImageDraw.Draw(im)
    polygon(d,[(26,96),(755,74),(718,474),(32,489)],K,W,8)
    label(d,1,'PERSONNEL RECORD',w)
    anim_title(im,'WHO IS',(55,111),96,t,white=W)
    anim_title(im,'VASSELL?',(76,231),99,t,white=R,shadow=W,angle=-3)
    d=ImageDraw.Draw(im)
    text(d,'INFORMATION SYSTEMS  /  TELKOM UNIVERSITY',(77,377),22,W,mono=True)
    polygon(d,[(791,82),(1172,69),(1137,467),(774,486)],W,K,8)
    # Abstract identity card, not a person/portrait/silhouette.
    ring(d,959,253,125,t,n=12,fg=R,thickness=8)
    origami(d,959,254,126,t,fg=R)
    text(d,'DIGITAL PRODUCT BUILDER',(808,409),22,K,mono=True,maxwidth=315)
    signature(d,w,h,t)
    return im


def draw_about_manifesto(t):
    w,h=1200,325
    im=base(w,h,t,1);d=ImageDraw.Draw(im)
    for i in range(5):
        shift=math.sin(t*2+i)*9
        polygon(d,[(15+i*12+shift,17+i*21),(739+i*4,12+i*19),
                   (675+i*6,245+i*9),(14+i*6,269+i*8)],K if i%2==0 else R,W if i%2==0 else K,3)
    anim_title(im,'FROM CONCEPT',(37,66),79,t,white=W,shadow=R)
    anim_title(im,'TO IMPLEMENTATION',(43,176),57,t,white=R,shadow=W,angle=-2)
    d=ImageDraw.Draw(im)
    for i,word in enumerate(('DISCOVER','DESIGN','ENGINEER','DELIVER')):
        y=23+i*65
        x=824+12*math.sin(t*3+i)
        polygon(d,[(x,y),(1174,y-5),(1155,y+50),(x-12,y+56)],W if i%2==0 else K,K,4)
        text(d,f'{i+1:02d}  {word}',(x+18,y+8),26,K if i%2==0 else W,mono=True,maxwidth=309)
    return im


def draw_skills(t):
    w,h=1200,510
    im=base(w,h,t,2);d=ImageDraw.Draw(im)
    label(d,2,'TECHNICAL ARSENAL',w)
    polygon(d,[(22,89),(692,66),(663,466),(26,478)],K,W,7)
    anim_title(im,'SYSTEMS',(35,112),107,t,white=W)
    anim_title(im,'& STACKS',(55,251),92,t,white=R,shadow=W,angle=-3)
    d=ImageDraw.Draw(im)
    text(d,'FRONTEND  /  BACKEND  /  WORKBENCH',(65,414),23,W,mono=True)
    cx,cy=941,280
    for j in range(6):
        ring(d,cx,cy,38+j*27,t,n=7+j,fg=K if j%2 else W,thickness=5,spin=1+j*.17)
    polygon(d,[(cx,cy-113),(cx+103,cy),(cx,cy+113),(cx-103,cy)],K,W,8)
    polygon(d,[(cx,cy-53),(cx+51,cy),(cx,cy+53),(cx-51,cy)],R,W,4)
    text(d,'</>',(cx-47,cy-21),40,W,mono=True)
    signature(d,w,h,t)
    return im


def draw_skill_deck(t):
    w,h=1200,458
    im=Image.new('RGB',(w,h),K);d=ImageDraw.Draw(im)
    rays(d,592,222,t,31,40,730,R)
    datasets=[
        ('01  FRONTEND',['HTML / CSS','JAVASCRIPT / TYPESCRIPT','REACT / VUE','TAILWIND CSS / FIGMA'],W,K),
        ('02  BACKEND',['PHP / LARAVEL','NODE.JS / MYSQL','PYTHON / REST APIs','ROLE-BASED ACCESS'],R,W),
        ('03  WORKBENCH',['GIT / GITHUB','POSTMAN / VS CODE','DOCKER / CLOUD','LUA / ROBLOX STUDIO'],K,W),
    ]
    for i,(title,rows,bg,fg) in enumerate(datasets):
        x=10+i*397; jitter=7*math.sin(t*2.2+i)
        polygon(d,[(x+21,22+jitter),(x+389,9+jitter),(x+366,415+jitter),
                   (x,440+jitter)],bg,W if i==2 else K,6)
        polygon(d,[(x+23,45+jitter),(x+347,35+jitter),(x+332,91+jitter),(x+13,99+jitter)],R if i!=1 else K)
        text(d,title,(x+36,54+jitter),24,W,mono=True,maxwidth=290)
        for j,row in enumerate(rows):
            yy=126+j*66+jitter
            text(d,row,(x+28,yy),22,fg,mono=True,maxwidth=328)
            end=x+326-15*math.sin(t*3+j+i)
            line(d,(x+30,yy+39,end,yy+39),fg,2)
        block=x+65+(t*40)%240
        box(d,(block,414+jitter,block+28,422+jitter),R if i!=1 else W)
    return im


def draw_project_gate(t):
    w,h=1200,360
    im=base(w,h,t,0);d=ImageDraw.Draw(im)
    polygon(d,[(18,18),(770,7),(737,323),(14,349)],K,W,9)
    polygon(d,[(35,31),(696,15),(690,87),(27,111)],R)
    text(d,'// 03  FEATURED WORK / PROJECT INDEX',(52,37),24,W,mono=True)
    anim_title(im,'SELECT',(44,114),105,t,white=W)
    anim_title(im,'A PROJECT',(68,209),77,t,white=R,shadow=W,angle=-2)
    d=ImageDraw.Draw(im)
    for i in range(6):
        x=825+i%3*118; y=64+i//3*116
        active=(int(t*1.8)%6)==i
        polygon(d,[(x+21,y),(x+107,y+8),(x+81,y+92),(x-4,y+79)],W if active else K,K if active else W,4)
        text(d,f'{i+1:02d}',(x+20,y+20),36,R if active else W,mono=True)
    text(d,'LIVE REPOSITORY LINKS BELOW',(809,314),18,K,mono=True)
    return im


def draw_portfolio(t):
    w,h=1200,470
    im=base(w,h,t,1);d=ImageDraw.Draw(im)
    # Browser-window artwork, not a repeated character portrait.
    polygon(d,[(25,40),(1096,17),(1166,378),(90,450)],K,W,11)
    polygon(d,[(30,45),(1096,23),(1107,106),(50,131)],R)
    for i in range(3):
        d.ellipse((77+i*33,65,95+i*33,83),fill=W)
    text(d,'TAKEYOURCODE.VERCEL.APP',(252,62),25,W,mono=True)
    for i in range(5):
        y=144+i*42
        x=62+11*math.sin(t*2+i)
        line(d,(x,y,650-(i%3)*65,y-19),W if i%2 else R,9 if i%2 else 5)
    # A staggered original UI screen, not a real screenshot or fact claim.
    polygon(d,[(742,147),(1050,129),(1087,323),(766,356)],W,K,6)
    for j in range(4):
        x=776+j%2*126; y=177+j//2*77
        polygon(d,[(x,y),(x+108,y-7),(x+98,y+65),(x-3,y+68)],R if j%3==0 else K)
        line(d,(x+16,y+28,x+81,y+25),W,4)
        line(d,(x+16,y+41,x+57,y+38),W,3)
    anim_title(im,'PERSONAL',(61,174),83,t,white=W)
    anim_title(im,'PORTFOLIO',(58,276),76,t,white=R,shadow=W,angle=-2)
    d=ImageDraw.Draw(im)
    polygon(d,[(142,395),(1068,377),(1099,430),(113,451)],W,K,5)
    text(d,'OPEN THE LIVE EXPERIENCE   /   CLICK TO VISIT',(153,402),27,K,mono=True,maxwidth=863)
    return im


def draw_portfolio_source(t):
    w,h=1200,218
    im=Image.new('RGB',(w,h),K);d=ImageDraw.Draw(im)
    rays(d,1042,100,t,count=25,inner=35,outer=570,color=R)
    polygon(d,[(18,19),(1081,3),(1033,193),(20,210)],W,R,7)
    polygon(d,[(48,36),(1100,20),(1022,101),(36,113)],K)
    anim_title(im,'SOURCE REPOSITORY',(38,41),70,t,white=W,shadow=R)
    d=ImageDraw.Draw(im)
    text(d,'PORTOFOLIO-VASSELL-PERSONA-INSPIRED   /   GITHUB',(77,150),22,K,mono=True,maxwidth=887)
    for j in range(5):
        xx=1013+j*27-20
        polygon(d,[(xx,115),(xx+19,123),(xx+4,139)],R)
    return im


def draw_project_map(t):
    w,h=1200,269
    im=Image.new('RGB',(w,h),R);d=ImageDraw.Draw(im)
    polygon(d,[(10,7),(1184,16),(1156,254),(18,262)],K,W,8)
    text(d,'PROJECT INDEX / SIX SELECTED DESTINATIONS',(49,31),25,W,mono=True)
    names=['BRREAD!','CATCH & CLASH','AMANIN','PHARVIA','VUE UI LAB','MORE WORK']
    for i,name in enumerate(names):
        x=52+i*189; y=101+(i%2)*18
        active=int(t*1.6)%6==i
        polygon(d,[(x+6,y),(x+169,y-8),(x+158,y+91),(x,y+99)],W if active else R,W,3)
        text(d,f'{i+1:02d}',(x+15,y+10),28,K if active else W,mono=True)
        text(d,name,(x+14,y+54),23,K if active else W,maxwidth=140)
    return im


PROJECTS=[
    ('BRREAD!','LARAVEL / PHP / MYSQL','COMMERCE AND INVENTORY', 'https://github.com/vassellenha/KWU-BRREAD'),
    ('CATCH & CLASH','ROBLOX STUDIO / LUA','INTERACTIVE GAMEPLAY', 'https://github.com/vassellenha/CatchAndClash_Roblox_Project'),
    ('AMANIN','AI / PRODUCT / SAFETY','ANTI-SCAM SUPPORT CONCEPT', 'https://github.com/vassellenha/AMANIN-Project'),
    ('PHARVIA','PRODUCT / TRACEABILITY','PHARMACEUTICAL RETURN CONCEPT', 'https://github.com/vassellenha/PHARVIA-Project'),
    ('VUE UI LAB','VUE / COMPONENTS / REST','INTERFACE SYSTEMS', 'https://github.com/vassellenha/PRAKTIKUM_UI-LANJUT_VASSELL-ENHA-ATTHAYYA_102042300140'),
    ('MORE WORK','GITHUB / REPOSITORIES','FURTHER PROJECT EXPLORATION', 'https://github.com/vassellenha?tab=repositories'),
]


def symbol_bread(d,x,y,s,t):
    # Animated loaf + storefront canopy.
    poly(d,[(x-s,y+s*.4),(x-s*.82,y-s*.17),(x-s*.44,y-s*.58),
            (x+s*.45,y-s*.58),(x+s*.87,y-s*.13),(x+s,y+s*.42)],W,K,6)
    for i in (-.4,0,.4):
        line(d,(x+i*s,y-s*.38,x+(i+.2)*s,y-.07*s),R,6)
    for i in range(4):
        bx=x-s*.65+i*s*.42; yy=y+s*.59+3*math.sin(t*4+i)
        polygon(d,[(bx,yy),(bx+s*.3,yy),(bx+s*.25,yy+s*.2),(bx,yy+s*.2)],GOLD,K,3)


def symbol_game(d,x,y,s,t):
    # Grappling hook, concentric water rings, original gameplay motif.
    for i in range(3):
        r=s*(.3+i*.21+(.04*math.sin(t*2+i)))
        d.arc((x-r,y-r,x+r,y+r),t*60+i*39,t*60+i*39+230,fill=W,width=5)
    line(d,(x-s*.55,y-s*.7,x+s*.19,y+s*.35),W,9)
    d.arc((x-s*.15,y+s*.18,x+s*.5,y+s*.82),-10,210,fill=GOLD,width=13)
    d.ellipse((x-s*.6,y-s*.76,x-s*.4,y-s*.56),fill=R,outline=W,width=4)


def symbol_shield(d,x,y,s,t):
    # Anti-scam concept: shield and linked verification nodes.
    polygon(d,[(x,y-s*.8),(x+s*.75,y-s*.48),(x+s*.63,y+s*.35),
               (x,y+s*.88),(x-s*.61,y+s*.36),(x-s*.74,y-s*.47)],W,K,8)
    polygon(d,[(x,y-s*.55),(x+s*.49,y-s*.29),(x+s*.41,y+s*.23),
               (x,y+s*.57),(x-s*.39,y+s*.23),(x-s*.48,y-s*.3)],K)
    line(d,(x-s*.26,y,x-s*.04,y+s*.19,x+s*.34,y-s*.26),GOLD,11)
    for a in (0,2.1,4.2):
        xx=x+math.cos(a+t*.25)*s*.95
        yy=y+math.sin(a+t*.25)*s*.95
        d.ellipse((xx-7,yy-7,xx+7,yy+7),fill=R,outline=W,width=3)


def symbol_pharma(d,x,y,s,t):
    # Capsule + chain-of-custody trace nodes.
    angle=math.sin(t*.7)*.2
    polygon(d,[(x-s*.7,y-s*.18),(x-s*.18,y-s*.67),(x+s*.68,y+s*.16),
               (x+s*.18,y+s*.7)],W,K,7)
    line(d,(x-s*.22,y-s*.62,x+s*.22,y-s*.18,x-s*.21,y+s*.21),R,7)
    for i in range(4):
        a=i*math.pi/2+t*.25+angle
        xx=x+s*.9*math.cos(a); yy=y+s*.9*math.sin(a)
        d.ellipse((xx-8,yy-8,xx+8,yy+8),fill=GOLD,outline=K,width=3)


def symbol_vue(d,x,y,s,t):
    # Browser component nesting and a rotating interface cursor.
    polygon(d,[(x-s*.9,y-s*.66),(x+s*.82,y-s*.68),
               (x+s*.71,y+s*.66),(x-s*.8,y+s*.71)],W,K,6)
    line(d,(x-s*.77,y-s*.37,x+s*.69,y-s*.36),K,5)
    for j in range(3):
        d.ellipse((x-s*.66+j*17,y-s*.53,x-s*.58+j*17,y-s*.45),fill=R)
    polygon(d,[(x-s*.55,y-s*.17),(x-s*.08,y+s*.47),(x+s*.43,y-s*.16),
               (x+s*.15,y-s*.16),(x-s*.06,y+s*.13),(x-s*.32,y-s*.17)],R)
    xx=x+s*.35+10*math.sin(t*2)
    polygon(d,[(xx,y+s*.09),(xx+s*.23,y+s*.35),(xx+s*.09,y+s*.4),(xx+s*.13,y+s*.59)],K,W,3)


def symbol_more(d,x,y,s,t):
    for i in range(5):
        a=i*SPEED/5+t*.25
        xx=x+math.cos(a)*s*.38; yy=y+math.sin(a)*s*.33
        polygon(d,[(xx-s*.28,yy-s*.3),(xx+s*.24,yy-s*.35),
                   (xx+s*.31,yy+s*.25),(xx-s*.19,yy+s*.31)],W if i%2==0 else R,K,4)
    text(d,'+', (x-s*.16,y-s*.32),66,GOLD)


SYMBOLS=[symbol_bread,symbol_game,symbol_shield,symbol_pharma,symbol_vue,symbol_more]


def project_card(i,t):
    """Six separate compositions; distinct colors, grids and subject icons."""
    w,h=650,355
    bg=[W,K,R,W,K,R][i]
    ink=K if bg==W else W
    im=Image.new('RGB',(w,h),bg);d=ImageDraw.Draw(im)
    # All six cards use different geometric architectures.
    if i==0:
        polygon(d,[(0,0),(408,0),(334,355),(0,355)],R)
        for k in range(12):
            x=20+k*30
            line(d,(x,295,x+70,290),W,2)
        polygon(d,[(410,0),(650,0),(650,355),(315,355)],W)
    elif i==1:
        rays(d,526,170,t,21,35,470,R)
        polygon(d,[(0,0),(452,0),(398,355),(0,355)],K,W,5)
    elif i==2:
        polygon(d,[(0,0),(500,0),(335,355),(0,355)],K)
        grid(d,426,30,9,12,20,t,W)
    elif i==3:
        for k in range(7):
            polygon(d,[(k*45,0),(k*45+30,0),(k*45+235,355),(k*45+207,355)],R if k%2 else K)
        polygon(d,[(18,12),(500,8),(447,342),(16,352)],W,K,6)
    elif i==4:
        circuit(d,0,0,625,355,t)
        polygon(d,[(0,0),(400,0),(322,355),(0,355)],K,W,6)
    else:
        rays(d,498,174,t,26,30,650,W)
        polygon(d,[(0,0),(480,0),(366,355),(0,355)],R)
    symbol=SYMBOLS[i]
    symbol(d,535,151,92,t)
    # Section-specific header mechanisms.
    fill=W if i%2==0 else R
    polygon(d,[(19,15),(300,10),(284,66),(12,72)],fill,K,4)
    text(d,f'MISSION // {i+1:02d}',(36,25),25,K if fill==W else W,mono=True)
    name,stack,subtitle,_=PROJECTS[i]
    fg=K if i in (3,) else W
    name_color=K if i in (3,) else W
    size=56 if i==4 else 65 if len(name)<12 else 53
    text(d,name,(29,123),size,name_color,maxwidth=390)
    text(d,subtitle,(34,213),22,name_color,mono=True,maxwidth=380)
    polygon(d,[(18,269),(611,262),(594,315),(14,324)],K if i in (0,3) else W, K if i in (0,3) else R,3)
    tint=W if i in (0,3) else K
    text(d,stack,(38,281),20,tint,mono=True,maxwidth=535)
    text(d,'OPEN REPOSITORY  >',(32,330),17,ink if i in (0,3) else W,mono=True)
    # Per-project motion is clearly visible: code bar, scanner, orbit, or metering.
    if i in (0,3):
        xx=45+(t*75)%350
        line(d,(xx,105,xx+34,105),GOLD,6)
    elif i in (1,5):
        d.ellipse((488+10*math.sin(t*2),308,504+10*math.sin(t*2),324),fill=GOLD)
    else:
        yy=72+(t*39)%150
        line(d,(435,yy,643,yy-25),GOLD,3)
    return im


def draw_activity(t):
    w,h=1200,465
    im=base(w,h,t,2);d=ImageDraw.Draw(im)
    label(d,4,'DEVELOPMENT COMMAND CENTER',w)
    polygon(d,[(25,89),(572,66),(547,416),(29,447)],K,W,7)
    anim_title(im,'ACTIVE',(30,108),98,t,white=W)
    anim_title(im,'BUILDING',(44,223),76,t,white=R,shadow=W,angle=-2)
    d=ImageDraw.Draw(im)
    text(d,'ILLUSTRATIVE STATUS / NOT LIVE METRICS',(58,372),17,W,mono=True)
    # Visualization is purely decorative: no fabricated numerical activity data.
    for j in range(9):
        for i in range(16):
            xx=621+i*33; yy=85+j*37
            k=.5+.5*math.sin(t*2.8-i*.36+j*.48)
            color=W if k>.77 else R if k>.43 else K
            polygon(d,[(xx,yy),(xx+26,yy-4),(xx+25,yy+24),(xx-2,yy+27)],color,K,2)
    line(d,(625,429,1178,421),W,5)
    for i in range(4):
        xx=659+i*128+26*math.sin(t+i)
        d.ellipse((xx-8,419,xx+8,435),fill=GOLD)
    return im


def draw_activity_diagram(t):
    w,h=1200,295
    im=Image.new('RGB',(w,h),W);d=ImageDraw.Draw(im)
    polygon(d,[(14,19),(1174,6),(1144,282),(9,288)],K,R,7)
    text(d,'/ / PRODUCT DELIVERY PIPELINE',(47,35),28,W,mono=True)
    stages=['PLAN','DESIGN','DEVELOP','TEST','DEPLOY']
    path=[]
    for j,st in enumerate(stages):
        x=54+j*219; y=131+22*math.sin(t*.7+j*.6)
        polygon(d,[(x+13,y-40),(x+189,y-44),(x+167,y+83),(x,y+94)],R if j%2==0 else W,W,3)
        text(d,st,(x+28,y+9),29,W if j%2==0 else K,maxwidth=140)
        path.append((x+87,y+26))
    for i in range(len(path)-1):
        line(d,(path[i][0]+104,path[i][1],path[i+1][0]-80,path[i+1][1]),GOLD,6)
    return im


def draw_activity_link(t):
    w,h=1200,189
    im=Image.new('RGB',(w,h),R);d=ImageDraw.Draw(im)
    for j in range(12):
        yy=j*22-30+6*math.sin(t*4+j)
        line(d,(839,yy,1199,yy+101),K,7)
    polygon(d,[(19,15),(1095,3),(1072,161),(9,178)],K,W,8)
    anim_title(im,'VIEW GITHUB ACTIVITY',(40,27),66,t,white=W,shadow=R)
    d=ImageDraw.Draw(im)
    text(d,'OPEN REAL CONTRIBUTIONS AND REPOSITORIES',(78,135),21,W,mono=True)
    return im


def draw_contact(t):
    w,h=1200,376
    im=base(w,h,t,0);d=ImageDraw.Draw(im)
    label(d,5,'CONTACT & COLLABORATION',w)
    polygon(d,[(29,92),(749,69),(705,335),(20,361)],K,W,8)
    anim_title(im,'CONNECT',(37,103),119,t,white=W)
    anim_title(im,'WITH ME',(77,236),74,t,white=R,shadow=W)
    d=ImageDraw.Draw(im)
    # Abstract network signal: no face, mask, body or OC-based insignia.
    for j in range(4):
        r=58+j*37+6*math.sin(t+j)
        d.arc((963-r,206-r,963+r,206+r),-75+t*25,185+t*25,fill=W if j%2 else K,width=5)
    for j in range(8):
        a=j*SPEED/8+t*.5
        x=963+142*math.cos(a);y=206+142*math.sin(a)
        polygon(d,[(x,y-12),(x+12,y),(x,y+12),(x-12,y)],GOLD if j%3==0 else W,K,2)
    d.ellipse((927,170,1000,242),fill=K,outline=W,width=7)
    text(d,'@',(941,171),57,W)
    return im


CONTACT=[
    ('GITHUB','@vassellenha','https://github.com/vassellenha'),
    ('LINKEDIN','VASSELL ENHA ATTHAYYA','https://www.linkedin.com/in/vassell-enha-atthayya-182661323/'),
    ('INSTAGRAM','@vassellenha','https://instagram.com/vassellenha'),
    ('PORTFOLIO','TAKEYOURCODE.VERCEL.APP','https://takeyourcode.vercel.app/#home'),
]


def contact_card(i,t):
    w,h=570,189
    im=Image.new('RGB',(w,h),K if i%2==0 else W);d=ImageDraw.Draw(im)
    # Four brand-specific but freshly constructed visual systems.
    if i==0:
        circuit(d,0,0,w,h,t)
        polygon(d,[(10,18),(433,0),(412,184),(6,177)],R,W,5)
        text(d,'{ }',(457,53),65,W,mono=True)
        fg=W
    elif i==1:
        rays(d,489,84,t,23,25,380,R)
        polygon(d,[(6,14),(435,9),(419,182),(5,188)],K,R,5)
        box(d,(469,62,536,127),R)
        text(d,'in',(474,65),46,W)
        fg=W
    elif i==2:
        rays(d,468,91,t,17,20,450,R)
        polygon(d,[(0,0),(431,0),(397,189),(0,189)],K,W,5)
        d.rounded_rectangle((451,54,534,134),radius=19,outline=W,width=7)
        d.ellipse((474,74,511,112),outline=R,width=6)
        d.ellipse((513,68,521,76),fill=W)
        fg=W
    else:
        polygon(d,[(1,11),(436,0),(414,180),(0,188)],R,K,4)
        polygon(d,[(451,46),(550,32),(532,142),(444,149)],K,R,5)
        line(d,(454,68,541,58),W,5)
        text(d,'</>',(460,89),34,W,mono=True)
        fg=W
    label_name,handle,_=CONTACT[i]
    text(d,f'0{i+1}  {label_name}',(25,29),43,fg,maxwidth=366)
    polygon(d,[(25,108),(415,100),(404,160),(18,171)],W if i%2==0 else K,K if i%2==0 else W,3)
    text(d,handle,(34,122),22,K if i%2==0 else W,mono=True,maxwidth=354)
    for j in range(5):
        xx=42+j*42+14*math.sin(t*3+j)
        line(d,(xx,178,xx+25,172),W if i in (0,3) else R,3)
    return im


def draw_collaboration(t):
    w,h=1200,200
    im=Image.new('RGB',(w,h),W);d=ImageDraw.Draw(im)
    for j in range(11):
        x=j*122-45+11*math.sin(t+j)
        polygon(d,[(x,0),(x+37,0),(x+163,200),(x+124,200)],R if j%2==0 else K)
    polygon(d,[(32,12),(1127,4),(1091,182),(24,190)],K,W,7)
    anim_title(im,'LET US BUILD SOMETHING MEANINGFUL.',(35,35),49,t,white=W,shadow=R)
    d=ImageDraw.Draw(im)
    text(d,'SOFTWARE  /  INTERFACES  /  PRODUCTS',(72,140),23,W,mono=True)
    return im


def draw_finale(t):
    w,h=1200,415
    im=base(w,h,t,2);d=ImageDraw.Draw(im)
    for j in range(11):
        r=54+j*37
        d.arc((953-r,202-r,953+r,202+r),t*38+j*24,t*38+j*24+59,fill=K if j%3==0 else W,width=5)
    polygon(d,[(25,34),(816,14),(772,371),(12,392)],K,W,9)
    anim_title(im,'BUILD WITH',(25,66),108,t,white=W)
    anim_title(im,'PURPOSE.',(109,205),121,t,white=R,shadow=W,angle=-3)
    d=ImageDraw.Draw(im)
    polygon(d,[(811,310),(1142,282),(1127,354),(802,380)],W,K,5)
    text(d,'THANK YOU FOR VISITING',(833,324),20,K,mono=True)
    return im


def draw_finale_signature(t):
    w,h=1200,151
    im=Image.new('RGB',(w,h),K);d=ImageDraw.Draw(im)
    rays(d,1084,74,t,29,24,390,R)
    polygon(d,[(9,14),(1053,1),(1035,136),(12,147)],W,R,6)
    text(d,'VASSELL ENHA ATTHAYYA',(37,39),48,K,maxwidth=929)
    text(d,'DESIGN  >  DEVELOPMENT  >  DEPLOYMENT',(52,112),17,R,mono=True)
    return im


NAVS=['ABOUT','ARSENAL','PROJECTS','ACTIVITY','CONTACT']


def nav_card(i,t):
    w,h=230,81
    im=Image.new('RGB',(w,h),K);d=ImageDraw.Draw(im)
    polygon(d,[(5,4),(228,0),(213,78),(0,78)],R if i%2==0 else W)
    polygon(d,[(12,13),(218,7),(204,68),(8,70)],K)
    x=10+int((t*53+i*17)%204)
    line(d,(x,65,x+30,60),GOLD,3)
    text(d,f'{i+1:02d}',(20,19),25,R if i%2 else W,mono=True)
    text(d,NAVS[i],(72,21),25,W,maxwidth=128)
    return im


def interlude(i,t):
    w,h=1200,127
    im=Image.new('RGB',(w,h),K if i%2==0 else R);d=ImageDraw.Draw(im)
    symbols=[('01','ANALYZE / DESIGN / BUILD'),('02','ENGINEERING IS CREATIVE WORK'),
             ('03','FROM IDEAS TO DIGITAL PRODUCTS')]
    number,message=symbols[i]
    rays(d,1066,64,t,count=23,inner=22,outer=390,color=R if i%2==0 else W)
    polygon(d,[(13,14),(1115,1),(1078,112),(14,124)],W if i%2==0 else K,K,6)
    text(d,f'// {number}',(35,26),40,K if i%2==0 else W,mono=True)
    text(d,message,(181,32),44,K if i%2==0 else W,maxwidth=840)
    return im


FULL=[
    ('01-hero-cinematic',draw_hero,6.0),
    ('02-personnel-record',draw_about,5.0),
    ('02b-concept-to-implementation',draw_about_manifesto,4.5),
    ('03-technical-arsenal',draw_skills,5.0),
    ('03b-stack-deck',draw_skill_deck,4.5),
    ('04-project-selector',draw_project_gate,4.5),
    ('04b-featured-portfolio',draw_portfolio,5.0),
    ('04c-source-repository',draw_portfolio_source,4.0),
    ('04d-project-index',draw_project_map,4.0),
    ('05-development-center',draw_activity,5.0),
    ('05b-delivery-pipeline',draw_activity_diagram,4.0),
    ('05c-live-activity-link',draw_activity_link,4.0),
    ('06-contact-portal',draw_contact,5.0),
    ('06b-collaboration',draw_collaboration,4.0),
    ('07-grand-finale',draw_finale,5.0),
    ('07b-signature',draw_finale_signature,4.0),
]


def encode(frames,destination,fps):
    palette=frames/'palette.png'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate',str(fps),
                    '-i',str(frames/'%04d.png'),'-vf','palettegen=stats_mode=diff',str(palette)],check=True)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate',str(fps),
                    '-i',str(frames/'%04d.png'),'-i',str(palette),'-filter_complex',
                    '[0:v][1:v]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle',
                    '-loop','0',str(destination)],check=True)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--fps',type=int,default=20)
    parser.add_argument('--preview-only',action='store_true')
    parser.add_argument('--only',help='optional asset basename substring')
    args=parser.parse_args()
    works=[('motion',name,func,duration) for name,func,duration in FULL]
    works += [('projects',f'project-{i+1:02d}',lambda t,j=i:project_card(j,t),4.0) for i in range(6)]
    works += [('contact',f'contact-{i+1:02d}',lambda t,j=i:contact_card(j,t),4.0) for i in range(4)]
    works += [('navigation',f'nav-{i+1:02d}',lambda t,j=i:nav_card(j,t),3.0) for i in range(5)]
    works += [('interludes',f'interlude-{i+1:02d}',lambda t,j=i:interlude(j,t),3.5) for i in range(3)]
    for folder,name,render,duration in works:
        if args.only and args.only not in name: continue
        dest=OUT/folder;dest.mkdir(parents=True,exist_ok=True)
        sample=render(duration*.38)
        sample.save(dest/f'{name}-preview.png',optimize=True)
        if args.preview_only:
            print(f'PREVIEW {folder}/{name}',flush=True);continue
        with tempfile.TemporaryDirectory(prefix='vassell-frames-') as td:
            frames=Path(td)
            count=max(2,round(duration*args.fps))
            for k in range(count):
                render(k/args.fps).save(frames/f'{k:04d}.png')
            encode(frames,dest/f'{name}.gif',args.fps)
        print(f'RENDERED {folder}/{name}: {(dest/f"{name}.gif").stat().st_size/1048576:.2f} MiB',flush=True)
    print(f'OVERDRIVE COMPLETE: {len([1 for _,name,_,_ in works if not args.only or args.only in name])} assets',flush=True)


if __name__=='__main__':main()
