# GitHub profile compatibility / known constraints

This package favors compatibility over making unsupported claims about GitHub's Markdown sanitizer.

- GitHub does **not** provide arbitrary README JavaScript, WebGL, unrestricted inline CSS, or scroll-driven frontend animation. The motion is **pre-rendered GIF** inside ordinary `<img>` tags.
- Internal Markdown-style anchors use `<a id="...">` and work independently of animation. The images are linked to actual GitHub project destinations.
- Links are unchanged from the user's supplied profile/previous README; **not independently verified online** in this environment.
- GIFs may be expensive to download on mobile; this is a deliberate maximalist choice. GitHub or user accessibility settings may pause/reduce animation. The profile content is still present as text and alternative text.
- GitHub may proxy and cache images, so changes to replaced GIFs can take some time to show. Renaming changed assets avoids stale proxy caches.
- There are no remote status images. The animated grid is decorative, and the fully designed activity button links to the user's real GitHub overview.
- The old HTML/STL easter egg and unrelated editorial portrait were not reused in the live README; the old ZIP is preserved separately.

## Verification checklist

- [x] No script elements in README
- [x] Every local image path checked by validation script
- [x] Every local animated asset is pre-rendered as a real GIF
- [x] Profile facts and real project links retained
- [x] No ordinary Markdown tables or default visible links in the README
- [x] OC artwork uses the supplied character reference with natural eyes
- [x] Static first-frame previews provided
- [ ] Upload and verify on GitHub itself (requires the repository owner)

## GIF quality notes

Animated GIFs are 256-color by format. The renderer quantizes with FFmpeg palettegen / paletteuse and Bayer dithering to keep reds and whites clean. The master rendering is in full RGB. No web-hosted JavaScript or untrusted runtime animation is required.
