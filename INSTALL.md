# Install on GitHub

**Upload the entire contents of this package to the root of `vassellenha/vassellenha`.** Do not upload only README.md, and do not upload the ZIP itself.

Required structure:

```text
README.md
.github/workflows/snake.yml          <- NEW: draws the contribution snake
assets/
  ccell-hero.gif, ccell-hero-preview.png        (unchanged sakura header)
  section-01.svg ... section-05.svg             (unchanged)
  project-brread.png, project-catchclash.png    (unchanged)
  development-loop.svg, footer.svg, icon-*.svg (unchanged)
  --- new in this version ---
  typing-roles.svg, terminal-whoami.svg, trophy-case.svg
  interlude-deploy.svg, divider-petals.svg
  stack-orbit.svg, journey-path.svg
  project-amanin.svg, project-pharvia.svg, project-vuelab.svg, project-more.svg
  btn-github.svg, btn-linkedin.svg, btn-instagram.svg, btn-portfolio.svg
```

On GitHub choose **Add file > Upload files** and drag the extracted files in. The `.github` folder starts with a dot, so on some systems it is hidden in the file picker: use "show hidden files", or create `.github/workflows/snake.yml` with **Add file > Create new file** and paste the contents.

## One-time step: wake up the snake

1. Open the repo's **Actions** tab and enable workflows if GitHub asks.
2. Pick **Generate contribution snake** and click **Run workflow**.
3. After it finishes there is an `output` branch holding `github-snake.svg` and `github-snake-dark.svg`. The README reads them from there. Until the first run the snake image shows as broken.

## Verify after upload

- https://github.com/vassellenha/vassellenha/blob/main/assets/stack-orbit.svg
- https://github.com/vassellenha/vassellenha/blob/main/assets/terminal-whoami.svg
- https://github.com/vassellenha/vassellenha/tree/output (after the workflow ran)

## What is what

- All new `assets/*.svg` are self-contained animated SVGs (pure SMIL, no scripts), so they animate inside a GitHub README.
- GitHub strips JavaScript and CSS from READMEs, so the interactivity is: expandable `<details>` cards, anchor navigation, the animated visuals, the 3D viewer (`stl` code block, drag to rotate) and the snake.
- The ASA portrait is still loaded from the Sony Music URL used before. If Sony Music changes that URL, that single picture stops loading.
- The streak, stats, language, activity-graph, trophy, followers and views images come from third-party services and depend on their uptime.
