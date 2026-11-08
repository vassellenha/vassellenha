# Install on GitHub

**Upload the entire contents of this package to the root of `vassellenha/vassellenha`.** Do not upload only README.md, and do not upload the ZIP itself.

Required structure:

```text
README.md
assets/
  ccell-hero.gif, ccell-hero-preview.png        (unchanged sakura header)
  section-01.svg ... section-05.svg             (unchanged)
  project-brread.png, project-catchclash.png    (unchanged)
  development-loop.svg, footer.svg, icon-*.svg  (unchanged)
  --- new in this version ---
  typing-roles.svg, divider-petals.svg
  sakura-reef.svg, shark-vs-commits.svg
  stack-orbit.svg, journey-path.svg
  project-amanin.svg, project-pharvia.svg, project-vuelab.svg, project-more.svg
  btn-github.svg, btn-linkedin.svg, btn-instagram.svg, btn-portfolio.svg
```

On GitHub choose **Add file > Upload files** and drag the extracted files in (keep the `assets` folder structure).

## Notes

- All new `assets/*.svg` are self-contained animated SVGs (pure SMIL, no scripts, no external requests), so they cannot "error out" and they animate inside a GitHub README.
- GitHub strips JavaScript and CSS from READMEs. The interactive bits are the animated visuals, anchor navigation and the 3D torii (`stl` code block: drag to rotate).
- No third-party stat cards are used any more (stats, top languages, activity graph, trophies, snake): they broke when those services were down or not set up. The only external pictures left are the shields.io nav badges, the skillicons in About, the streak card and the ASA portrait (Sony Music URL).
