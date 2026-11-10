# GitHub Rendering and Release QA

## Actual README behavior

- GitHub README contains only standard Markdown plus image/link HTML supported by GitHub's renderer. No README scripts, iframes, CSS animations, canvas elements or web-hosted media players are required.
- Every image path points to the local, fresh `assets/overdrive5/` namespace to avoid prior cache collisions.
- Animated navigation and project cards are clickable `<a><img /></a>` pairs, not interactive web applications.
- Main text is embedded in the motion artwork; all 34 image references have descriptive alternative text.
- Activity graphics are labeled as illustrative, while the real GitHub overview link remains functional.
- The separate HTML `showcase/index.html` has decorative hover/reveal effects, but it is not needed for GitHub playback.

## Limitations

GitHub image proxies and client accessibility controls may pause or cache animation; GIF playback on some mobile devices may lag. These are intrinsic constraints of an intentionally extravagant profile. A single GIF never requires external authentication or remote media service.

GitHub browser uploads accept regular files up to 25 MiB each; Git tracks larger files with warnings above 50 MiB and blocks files above 100 MiB in ordinary repositories. The release verifier checks that every individual GIF stays beneath the browser upload ceiling.

## Release checklist

- [x] 34 separate locally packaged animated GIFs, not static placeholders.
- [x] Exactly one hero function composits the supplied OC illustration.
- [x] Distinct original art for projects, skills, identity, activity and contact.
- [x] Personal portfolio and source repository links use owner-specified URLs.
- [x] No stale placeholder identity or misleading crime-themed copy.
- [x] No normal Markdown tables or default stock badges in the README.
- [x] Current source, previews, installation instructions and compatibility notes bundled.
- [ ] Verify the committed result directly on GitHub after the repository owner uploads it.

`python3 scripts/validate_v5.py` is the final mechanical asset/path/frame check.
