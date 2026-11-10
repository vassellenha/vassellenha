# Motion asset manifest

Every `.gif` below is a real, looping image rendered locally from `scripts/render.py`. All images are included in the ZIP; none of the local visuals depend on third-party image hosts.

| File | Intended role | Canvas | Approximate loop |
| --- | --- | --- | --- |
| `motion/01-phantom-hero.gif` | Animated intro, masked figure, multi-act calling-card transformation | 1280×620 | 6 seconds |
| `motion/02-personnel-dossier.gif` | Identity / Telkom University / introduction | 1200×480 | 6 seconds |
| `motion/03-phantom-arsenal.gif` | Skills, animated reticles, cycling stack categories | 1200×520 | 6 seconds |
| `motion/04-mission-select.gif` | Project selection banner | 1200×284 | 5 seconds |
| `motion/05-operation-pulse.gif` | Animated development motif, decorative tile grid | 1200×400 | 6 seconds |
| `motion/06-social-link.gif` | Contact sequence, animated orbiting message pips | 1200×360 | 5 seconds |
| `motion/07-steal-the-show.gif` | Closing graphic sequence | 1200×378 | 6 seconds |
| `posters/mission-01.gif` | BRREAD! project dossier with moving scanner | 640×327 | 3.5 seconds |
| `posters/mission-02.gif` | Catch & Clash project dossier | 640×327 | 3.5 seconds |
| `posters/mission-03.gif` | AMANIN project dossier | 640×327 | 3.5 seconds |
| `posters/mission-04.gif` | PHARVIA project dossier | 640×327 | 3.5 seconds |
| `posters/mission-05.gif` | Vue UI Lab project dossier | 640×327 | 3.5 seconds |
| `posters/mission-06.gif` | All repositories entry card | 640×327 | 3.5 seconds |

The seven `motion/*-preview.png` files are crisp static inspection images and can replace GIFs if desired. The six `posters/mission-*.png` files serve as static fallbacks for cards. Five `navigation/nav-*.png` files are clickable section tab art.

## Technical details

- Default production frame rate: **20 FPS**.
- Output GIF palette: 256 colors using FFmpeg palettegen + paletteuse with Bayer dithering.
- Source visuals: mathematically generated polygons, screen-print dots, angular label masks, composited original masked figure, animated radial bursts, script-drawn type overlays.
- Presentation: actual GitHub-compatible Markdown and `<img>` embeds; `showcase/index.html` adds optional browser-only hover effects.

All assets are designed for a dark or light GitHub theme because the image artwork itself is opaque red/black/off-white, not theme-dependent transparent text.
