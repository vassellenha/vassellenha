# Motion asset manifest

All 21 `.gif` assets are real, looping images rendered locally from `scripts/render.py`. All images are included in the ZIP; none of the visuals depend on third-party image hosts. The character is Vassell's supplied OC art, preserved at `assets/source/vassell-oc.png`.

| File | Intended role | Canvas | Approximate loop |
| --- | --- | --- | --- |
| `motion/01-phantom-hero.gif` | Animated intro, Vassell's own OC and two-act identity/calling-card transformation | 1280×620 | 6 seconds |
| `motion/02-personnel-dossier.gif` | OC identity / Telkom University / introduction | 1200×480 | 6 seconds |
| `motion/02b-identity-board.gif` | Custom three-column role/status cards replacing Markdown table | 1200×345 | 5 seconds |
| `motion/02c-bio-manifesto.gif` | Illustrated introduction with OC crop | 1200×275 | 5 seconds |
| `motion/03-phantom-arsenal.gif` | Skills, animated reticles, cycling stack categories | 1200×520 | 6 seconds |
| `motion/03b-skill-board.gif` | Three custom all-graphic skill cards replacing Markdown table | 1200×440 | 5 seconds |
| `motion/04-mission-select.gif` | Selected projects overview | 1200×284 | 5 seconds |
| `motion/05-operation-pulse.gif` | Animated development motif, decorative tile grid | 1200×400 | 6 seconds |
| `motion/05b-status-link.gif` | Custom link to true GitHub activity | 1200×176 | 5 seconds |
| `motion/06-social-link.gif` | Contact sequence, animated orbiting message pips | 1200×360 | 5 seconds |
| `motion/07-professional-finale.gif` | Professional closing graphic sequence | 1200×378 | 6 seconds |
| `posters/mission-01.gif` | BRREAD! project card with moving scanner | 640×327 | 3.5 seconds |
| `posters/mission-02.gif` | Catch & Clash project dossier | 640×327 | 3.5 seconds |
| `posters/mission-03.gif` | AMANIN project dossier | 640×327 | 3.5 seconds |
| `posters/mission-04.gif` | PHARVIA project dossier | 640×327 | 3.5 seconds |
| `posters/mission-05.gif` | Vue UI Lab project dossier | 640×327 | 3.5 seconds |
| `posters/mission-06.gif` | All repositories entry card | 640×327 | 3.5 seconds |
| `links/contact-01.gif` | Custom animated GitHub social card | 560×154 | 3 seconds |
| `links/contact-02.gif` | Custom animated LinkedIn social card | 560×154 | 3 seconds |
| `links/contact-03.gif` | Custom animated Instagram social card | 560×154 | 3 seconds |
| `links/contact-04.gif` | Custom animated Portfolio social card | 560×154 | 3 seconds |

The eleven `motion/*-preview.png` files are crisp static inspection images and can replace GIFs if desired. The six `posters/mission-*.png` files serve as static fallbacks for cards. Five `navigation/nav-*.png` files are clickable section tab art.

## Technical details

- Default production frame rate: **20 FPS**.
- Output GIF palette: 256 colors using FFmpeg palettegen + paletteuse with Bayer dithering.
- Source visuals: the user's supplied original masked-character illustration, mathematically generated polygons, screen-print dots, angular label masks, animated radial bursts, and script-drawn typography.
- Presentation: actual GitHub-compatible Markdown and `<img>` embeds; `showcase/index.html` adds optional browser-only hover effects.

All assets are designed for a dark or light GitHub theme because the image artwork itself is opaque red/black/off-white, not theme-dependent transparent text.
