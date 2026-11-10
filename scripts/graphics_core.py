"""Minimal reusable drawing toolkit for Overdrive V5.

Character input is available to the hero alone; this module deliberately
contains no old character badge, icon, or V4 rendering pipeline.
"""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
RED=(222,16,36)
BRIGHT=(250,34,47)
BLACK=(10,9,12)
INK=(22,18,22)
WHITE=(250,247,236)
YELLOW=(255,221,77)
GRAY=(164,163,166)
FONT_BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'
FONT_REG='/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf'
FONT_MONO='/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'


def font(size,mono=False,regular=False):
    return ImageFont.truetype(FONT_MONO if mono else FONT_REG if regular else FONT_BOLD,size)


def clamp(value,low=0,high=1):
    return max(low,min(high,value))


def ease(value):
    value=clamp(value)
    return 1-(1-value)**3


def poly(d,points,fill,outline=None,width=1):
    pts=[(int(x),int(y)) for x,y in points]
    d.polygon(pts,fill=fill)
    if outline: d.line(pts+[pts[0]],fill=outline,width=width,joint='curve')


def panel(d,x,y,w,h,color,cut=24,border=None,borderwidth=5):
    pts=[(x+cut,y),(x+w,y),(x+w-cut,y+h),(x,y+h),(x+cut//2,y+h//2)]
    poly(d,pts,color,border,borderwidth)


def dot_field(d,rect,step=21,radius=3,seed=1,color=BLACK,wobble=0):
    x0,y0,x1,y1=rect
    rnd=random.Random(seed)
    for x in range(int(x0),int(x1),step):
        for y in range(int(y0),int(y1),step):
            wave=.5+.5*math.sin((x+y)/70+wobble)
            rr=max(1,radius*(.5+wave)*(.7+rnd.random()*.4))
            d.ellipse((x-rr,y-rr,x+rr,y+rr),fill=color)


def burst(d,cx,cy,r0,r1,n,phase,colors=(RED,BLACK)):
    for i in range(n):
        a=2*math.pi*i/n+phase
        a2=a+.025+.012*math.sin(i*1.3)
        rr=r1*(.85+.23*math.sin(i*3.7+phase))
        poly(d,[(cx+r0*math.cos(a),cy+r0*math.sin(a)),
                (cx+rr*math.cos(a2),cy+rr*math.sin(a2)),
                (cx+r0*math.cos(a+.065),cy+r0*math.sin(a+.065))],colors[i%len(colors)])


def scratch(d,w,h,t,seed=4,count=44,color=WHITE):
    rnd=random.Random(seed)
    for i in range(count):
        x=rnd.randint(-100,w+150)+60*math.sin(t*2+i)
        y=rnd.randint(-100,h+100)
        length=rnd.randint(12,130)
        d.line((x,y,x+length,y-length*.34),fill=color,width=rnd.choice([1,2,3]))


def type_layer(im,txt,pos,size,fg=WHITE,shadow=BLACK,angle=0,
               stroke=0,stroke_fill=BLACK,skew=0,mono=False):
    f=font(size,mono)
    bb=f.getbbox(txt,stroke_width=stroke)
    lw=bb[2]-bb[0]+70;lh=bb[3]-bb[1]+60
    lay=Image.new('RGBA',(lw,lh),(0,0,0,0));d=ImageDraw.Draw(lay)
    at=(32-bb[0],28-bb[1])
    if shadow:
        d.text((at[0]+8,at[1]+8),txt,font=f,fill=shadow,
               stroke_width=stroke+2 if stroke else 0,stroke_fill=shadow)
    d.text(at,txt,font=f,fill=fg,stroke_width=stroke,stroke_fill=stroke_fill)
    if skew:
        ext=abs(skew)*lh
        lay=lay.transform((int(lw+ext),lh),Image.Transform.AFFINE,
                          (1,skew,-min(0,skew*lh),0,1,0),Image.Resampling.BICUBIC)
    if angle: lay=lay.rotate(angle,Image.Resampling.BICUBIC,expand=True)
    im.paste(lay,(int(pos[0]),int(pos[1])),lay)


_OC_CACHE={}


def oc_frame(width,height,mode='wide'):
    """Original supplied OC photograph. Call ONLY from V5's draw_hero()."""
    key=(width,height,mode)
    if key in _OC_CACHE:return _OC_CACHE[key].copy()
    source=Image.open(ROOT/'assets'/'source'/'vassell-oc.png').convert('RGB')
    if mode=='portrait':source=source.crop((515,25,1435,940))
    elif mode=='close':source=source.crop((225,0,1510,830))
    sw,sh=source.size
    scale=max(width/sw,height/sh)
    sized=source.resize((math.ceil(sw*scale),math.ceil(sh*scale)),Image.Resampling.LANCZOS)
    left=(sized.width-width)//2;top=(sized.height-height)//2
    result=sized.crop((left,top,left+width,top+height))
    _OC_CACHE[key]=result
    return result.copy()
