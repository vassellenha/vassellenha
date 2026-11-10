#!/usr/bin/env python3
"""Deterministic release checks for GitHub-compatible Overdrive V5."""
from __future__ import annotations

import ast
import re
from pathlib import Path
from PIL import Image, ImageChops

ROOT=Path(__file__).resolve().parents[1]
ASSET=ROOT/'assets'/'overdrive5'
README=(ROOT/'README.md').read_text(encoding='utf-8')
SHOWCASE=(ROOT/'showcase'/'index.html').read_text(encoding='utf-8')
SOURCE=(ROOT/'scripts'/'overdrive.py').read_text(encoding='utf-8')

paths=re.findall(r'<img\s+[^>]*src="([^"]+)"',README)
assert len(paths)==34,(len(paths),'Expected exactly 34 illustrated motion references')
assert all(p.startswith('./assets/overdrive5/') for p in paths),'Legacy asset reference'
assert len(set(paths))==34,'Repeating a GIF in multiple sections is prohibited'
assert all((ROOT/p).is_file() for p in paths),'A README asset is missing'
assets=sorted(ASSET.rglob('*.gif'))
assert len(assets)==34,(len(assets),'Expected 34 complete motion graphics')

for filename in assets:
    with Image.open(filename) as im:
        frames=im.n_frames
        assert frames>=48,(filename,frames,'Static/too-short GIF')
        im.seek(0); first=im.convert('RGB')
        im.seek(frames//2); midpoint=im.convert('RGB')
        diff=ImageChops.difference(first,midpoint)
        assert diff.getbbox(),(filename,'No frame changes')
        assert filename.stat().st_size<25*1024*1024,('Browser upload size limit',filename)
        print(f'OK {filename.relative_to(ROOT)} | {frames} frames | {filename.stat().st_size/1048576:.2f} MiB')

for document in (README,SHOWCASE):
    lower=document.lower()
    assert 'ccell' not in lower
    assert 'i steal' not in lower
    assert 'stealing bugs' not in lower
    assert 'websiteportofoliokelompok5' not in lower
    assert 'https://takeyourcode.vercel.app/#home' in document
    assert 'https://github.com/vassellenha/Portofolio-Vassell-Persona-Inspired' in document
    assert 'https://www.linkedin.com/in/vassell-enha-atthayya-182661323/' in document
assert not re.search(r'<(?:table|script|iframe)\b',README,re.I)
assert not any(ln.strip().startswith('|') for ln in README.splitlines())
assert len(README.encode('utf-8'))<2*1024*1024

# Both character rendering and full OC source use are locked to the hero.
tree=ast.parse(SOURCE)
calls={}
for node in ast.walk(tree):
    if isinstance(node,ast.FunctionDef):
        count=sum(isinstance(c,ast.Call) and isinstance(c.func,ast.Name) and c.func.id=='oc_frame'
                  for c in ast.walk(node))
        if count: calls[node.name]=count
assert calls=={'draw_hero':1},f'OC unexpectedly used outside hero: {calls}'
assert not any('sigil' in p.lower() for p in paths),'OC-derived emblem should not repeat'
assert (ROOT/'assets/source/vassell-oc.png').is_file()

showcase_paths=re.findall(r'<img\s+[^>]*src="(\.\./[^"]+)"',SHOWCASE)
assert len(showcase_paths)>=34,(len(showcase_paths),'Incomplete showcase')
assert all((ROOT/'showcase'/path).is_file() for path in showcase_paths),'Broken showcase path'
print(f'PASS: {len(paths)} distinct and animated GIF references, 1 OC section, 0 missing assets.')
