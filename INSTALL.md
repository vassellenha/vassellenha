# VASSELL / ABSOLUTE OVERDRIVE V5 — Installation

This is a GitHub-compatible profile README with **34 locally rendered animated GIFs**. It requires no JavaScript, CSS or third-party image hosting to render on GitHub. The user-supplied original character appears only in the hero animation.

## Install to your GitHub profile

1. Extract `VASSELL-PERSONA5-ABSOLUTE-OVERDRIVE-V5.zip`.
2. Navigate to the GitHub profile repository **`vassellenha/vassellenha`**. Create a public repository named exactly `vassellenha` if it does not yet exist.
3. Upload the root `README.md` and the **entire `assets/overdrive5/` folder**, retaining their relative paths. These two elements are sufficient to display the animated README.
4. Commit the changes. Visit `https://github.com/vassellenha` to check the live rendering. No file has been pushed automatically.

If you want to regenerate the artwork, keep `scripts/` and `assets/source/vassell-oc.png` locally as well.

### Git CLI alternative

If the browser file upload process is inconvenient, extract the package into your existing local profile repository, then run:

```bash
git add README.md assets/overdrive5
git commit -m "Redesign profile with Overdrive V5 motion graphics"
git push
```

Do not remove old assets until you verify the new profile works; they are simply not referenced by the V5 README.

## Re-render or modify

Requires Python 3, Pillow, and FFmpeg:

```bash
python3 -m pip install pillow
python3 scripts/overdrive.py --preview-only
python3 scripts/overdrive.py --fps 20
python3 scripts/validate_v5.py
```

Use `--only 04b-featured-portfolio` to regenerate one asset. The renderer stores GIFs and first-frame inspection PNGs in `assets/overdrive5/`.

## Motion system

- 16 full-width motion sequences.
- 6 individually illustrated project graphics.
- 4 animated contact buttons.
- 5 animated navigation buttons.
- 3 animated typographic interludes.
- **34 unique GIF assets total.**

All artwork uses procedurally generated shapes, screen-print textures and typography, except for the **hero's original-character art** provided by Vassell. The reused OC-derived emblem from earlier versions is deliberately absent outside the hero.

## Important practical GitHub limits

- GitHub renders README Markdown, not arbitrary embedded web applications. The separate `showcase/index.html` is optional and has enhanced hover effects, but the README itself uses compatible animated images.
- Keep `README.md` reasonably small for dependable previews. This version stores artwork in separate local files.
- GitHub warns on individual tracked files over 50 MiB and blocks regular Git files over 100 MiB. GitHub browser uploads have a lower 25 MiB **per-file** limit. The finished assets are substantially below that per-file limit.
- GitHub may proxy/cache images. The new `assets/overdrive5/` namespace avoids stale V4 artwork being displayed under unchanged image URLs.
- The intentionally maximalist animated page may be expensive to download, especially on mobile. Alternative text is supplied for accessibility.

## Credibility and attribution

This is an original, Persona-inspired fan design, not an official game asset or Atlus product. All text uses Vassell's professional identity; do not interpret decorative activity cells as real GitHub statistics. Use the linked GitHub overview for actual contribution data. Project links were supplied by the profile owner and should be checked after publishing.

No misleading criminal slogans, stock badges, plain Markdown tables, or placeholder character art are present in the finished README.
