# GitHub profile compatibility / known constraints

This package favors compatibility over making unsupported claims about GitHub's Markdown sanitizer.

- GitHub does **not** provide arbitrary README JavaScript, WebGL, unrestricted inline CSS, or scroll-driven frontend animation. The motion is **pre-rendered GIF** inside ordinary `<img>` tags.
- Internal Markdown-style anchors use `<a id="...">` and work independently of animation. The images are linked to actual GitHub project destinations.
- Links are unchanged from the user's supplied profile/previous README; **not independently verified online** in this environment.
- GIFs may be expensive to download on mobile; this is a deliberate maximalist choice. GitHub or user accessibility settings may pause/reduce animation. The profile content is still present as text and alternative text.
- GitHub may proxy and cache images, so changes to replaced GIFs can take some time to show. Renaming changed assets avoids stale proxy caches.
- The external GitHub Streak Stats image remains outside this package and depends on the provider's uptime. No false local count is drawn in the animated grid.
- The old HTML/STL easter egg and unrelated editorial portrait were not reused in the live README; the old ZIP is preserved separately.

## Verification checklist

- [x] No script elements in README
- [x] Every local image path checked by validation script
- [x] Every local animated asset is pre-rendered as a real GIF
- [x] Profile facts and real project links retained
- [x] Static first-frame previews provided
- [ ] Upload and verify on GitHub itself (requires the repository owner)

## GIF quality notes

Animated GIFs are 256-color by format. The renderer quantizes with FFmpeg palettegen / paletteuse and Bayer dithering to keep reds and whites clean. The master rendering is in full RGB. No web-hosted JavaScript or untrusted runtime animation is required.
