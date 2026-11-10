# Install the Phantom Developer README

1. Extract `CCELL-PHANTOM-DEVELOPER.zip`.
2. Open your GitHub profile repository: **`vassellenha/vassellenha`**. If it doesn't exist, create a public repository named exactly `vassellenha` under that account.
3. Upload `README.md` and the **complete `assets/` folder** to the repository root, preserving relative paths.
4. Commit the files, then open `https://github.com/vassellenha` to see the actual profile.

The project contains `showcase/` and `scripts/` for local previews and future editing. They are optional for display, but keep them if you want reproducible source assets. The `archive/` folder preserves the previous ZIP; it does not need to be uploaded.

## Important differences from typical README templates

- **13 motion graphics** are actual pre-rendered animated GIF files (7 full-width sequences and 6 mission dossiers), so they do not depend on inline JavaScript or CSS in GitHub.
- **5 navigation cards** link directly to profile sections.
- The colors and shape vocabulary are Persona 5-inspired, but the illustrations, typography compositions and fictional mask design are custom-created for this project.
- The README contains human-readable profile data, project descriptions, and meaningful alternative text for every animation.
- The only remote visual is the live streak card, which may fail if the third-party provider is unavailable. The profile remains functional without it.
- The graphic contribution grid is explicitly **decorative**, not fake live statistics.

## Re-render the motion graphics

Requires Python 3, Pillow, and FFmpeg with palette filters:

```bash
python3 -m pip install pillow
python3 scripts/render.py --cards
```

The render pipeline creates RGB frames and converts them to 256-color looping GIFs with a dedicated motion palette. First-frame PNGs also live in `assets/motion/` for review/fallback. You can use `--only 01-phantom-hero` to regenerate only the hero, `--only static` for posters/navigation, or `--preview-only` to create static animation previews quickly.

## Source content preserved

- Name/alias, Telkom University, areas of work, learning interests, and competition mentions.
- Five individual project destinations and the all-repositories link.
- GitHub, LinkedIn, Instagram, and the portfolio link.
- The original input ZIP is preserved in `archive/`.

You may freely replace personal information or links in `README.md`. Nothing has been pushed to GitHub; upload/commit is your decision.
