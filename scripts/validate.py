#!/usr/bin/env python3
"""Check all local README image references and animated assets."""
import re
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[1]
text = (root / "README.md").read_text()
paths = re.findall(r'<img\s+[^>]*src="(\./[^\"]+)"', text)
missing = [p for p in paths if not (root / p).is_file()]
print(f"Local README image references: {len(paths)}")
print(f"Missing: {len(missing)}")
for p in missing:
    print("  MISSING", p)

gifs = sorted((root / "assets").rglob("*.gif"))
print(f"Animated assets: {len(gifs)}")
for path in gifs:
    with Image.open(path) as im:
        count = getattr(im, "n_frames", 1)
        print(f"  {path.relative_to(root)}: {im.size[0]}x{im.size[1]}, {count} frames, {path.stat().st_size/1048576:.2f} MiB")
        assert count > 1, f"Non-animated GIF: {path}"

expected = 21
assert len(gifs) == expected, f"Expected {expected} motion assets, got {len(gifs)}"
assert not missing, f"{len(missing)} local images missing"
assert (root / "assets/source/vassell-oc.png").is_file()
assert "VASSELL" in text, "Primary Vassell identity is missing"
assert "<table" not in text.lower(), "Plain HTML table remains"
assert not any(line.strip().startswith("|") for line in text.splitlines()), "Plain Markdown table remains"
assert 'https://github.com/vassellenha' in text
assert 'https://www.linkedin.com/in/vassell-enha-atthayya-182661323/' in text
assert '<script' not in text.lower()
print("PASS: all GitHub-compatible references and animated assets are present")
