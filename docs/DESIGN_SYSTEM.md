# Vassell / Absolute Overdrive — Motion and Art Direction

## Visual identity

An original high-contrast motion-design system inspired by the dramatic rhythm of Japanese game menus and the editorial geometry of modern comic book interfaces. No official game assets, logos or sounds are included.

Colors: crimson `#DE1024`, near-black `#0A090C`, off-white `#FAF7EC`, occasional yellow `#FDC331`. Source typography is DejaVu Sans Condensed / DejaVu Sans Mono, available locally for reproducible rendering.

## Intentional variety

- **Hero:** the sole character-driven section; carefully preserves Vassell's own OC facial details, outfit and mask. Two distinctive title acts communicate professional identity and ADAPT / IMPROVE / OVERCOME.
- **About:** paper-collage identity sheet with a purely geometric origami illustration and secondary staged process banners.
- **Arsenal:** radial technical dial and three independently colored technical cards; symbols represent systems rather than people.
- **Projects:** animated mission-selection gate, browser-interface feature, source-code CTA, project map, then six original project-specific illustrations.
- **Activity:** modular decorative status display paired with a true GitHub link and a software-delivery sequence.
- **Contact:** abstract signal/connection graphic plus four platform-appropriate animated interface cards.
- **Finale:** cinematic kinetic editorial title with an additional signature screen.

No portrait, character silhouette, mask logo, character-derived badge or other OC visual appears outside the hero section.

## Timing and production

Animations use deterministic waveform and interpolation timing with composited polygon masks, line work, changing radial arcs, traveling highlights, animated halftone/texture, and repeated print artifacts. `scripts/overdrive.py` generates lossless RGB master frames before FFmpeg palettegen/paletteuse converts them to 256-color looping GIFs. FPS defaults to 20 and can be adjusted.

Per-asset preview PNGs are included for fast inspection, and source code is retained for continuous iteration.
