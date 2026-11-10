# CCELL.exe / Phantom Developer — motion design specification

## Art direction

An original, maximalist graphic design inspired by the dramatic UI vocabulary of Persona 5. It uses comic-book halftones, angular black slabs, giant typography, screen-printed textures, hard-edged title masks, rapid graphics, tilted labels, and white ink on vivid red. The masked figure is an original anonymous fictional illustration, **not** a photo of Vassell and **not** an official Persona character.

## Palette

| Role | Color |
| --- | --- |
| Phantom red | `#DE1024` |
| Signal red | `#FA222F` |
| Ink black | `#0A090C` |
| Off-white paper | `#FAF7EC` |
| Optional spotlight | `#FFDD4D` |

## Choreography

1. **Hero:** collage starburst and masked-phantom illustration, branded type planes, moving high-edge glint, occasional analog glitch and eye light.
2. **Dossier:** classified stamp breathing, ink-ray burst, exaggerated identity headline and character ID.
3. **Arsenal:** rotating target reticles and periodically selected technical loadouts.
4. **Missions:** mission select screen with a moving row of diamond marker cursors.
5. **Pulse:** decorative commit-like tile field that undulates with a traveling wave; real stats are kept separate.
6. **Social:** orbiting message pips around oversized animated interface envelope.
7. **Outro:** offbeat graphic shards oscillate behind a large closing statement.
8. **Mission posters:** all six get independent moving scanner sweeps and analog line distortions.

All frames are generated mathematically with deterministic seeds to preserve a coherent aesthetic. There is no JavaScript embedded in the README, no autoplay video requirement, and no external art asset host.

## Production and editability

`scripts/render.py` contains all original vector-like drawing geometry, layout, text and animation timing. It generates project posters, navigation cards, full-width GIF sequences, and preview PNGs. Source typography uses available DejaVu Sans Condensed and DejaVu Sans Mono fonts, avoiding a remote-font dependency.

At GitHub's practical 800–900px article width, the important title text is large enough to remain legible. The `README.md` repeats essential identity and project data as searchable selectable text outside the animations.
