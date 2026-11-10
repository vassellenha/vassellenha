# Vassell / Phantom Developer — motion design specification

## Art direction

An original, maximalist graphic design inspired by the dramatic UI vocabulary of Persona 5. It uses comic-book halftones, angular black slabs, giant typography, screen-printed textures, hard-edged title masks, rapid graphics, tilted labels, and white ink on vivid red. The main character asset is Vassell's **own supplied OC artwork**, with his masked face and pose preserved; it is **not** an official Persona character.

## Palette

| Role | Color |
| --- | --- |
| Phantom red | `#DE1024` |
| Signal red | `#FA222F` |
| Ink black | `#0A090C` |
| Off-white paper | `#FAF7EC` |
| Optional spotlight | `#FFDD4D` |

## Choreography

1. **Hero:** original OC art as the hero plate, branded type planes, analog glitch and a second-act dramatic wipe.
2. **Dossier:** dramatic identity title, angular portrait crop of the supplied OC, and character ID.
3. **Technical skills:** rotating target reticles and periodically highlighted technology categories.
4. **Projects:** selected-projects screen with a moving row of diamond markers.
5. **Pulse:** decorative commit-like tile field that undulates with a traveling wave; real stats are kept separate.
6. **Social:** orbiting message pips around oversized animated interface envelope.
7. **Outro:** offbeat graphic shards oscillate behind a large closing statement.
8. **Project cards:** all six get independent moving scanner sweeps and analog line distortions.

All frames are generated mathematically with deterministic seeds to preserve a coherent aesthetic. There is no JavaScript embedded in the README, no autoplay video requirement, and no external art asset host.

## Production and editability

`scripts/render.py` contains custom drawing geometry, layout, text and animation timing. It generates project posters, navigation cards, full-width GIF sequences, and preview PNGs, integrating the user's `assets/source/vassell-oc.png` unchanged into the collage. Source typography uses DejaVu Sans Condensed and DejaVu Sans Mono fonts, avoiding a remote-font dependency.

At GitHub's practical 800–900px article width, the important title text is large enough to remain legible. Essential identity and project information is also included as descriptive image alternative text in `README.md` while the visible presentation remains fully designed.
