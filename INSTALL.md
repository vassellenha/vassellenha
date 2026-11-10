# Install the Phantom Developer README

1. Extract `VASSELL-PERSONA5-README-PROFESSIONAL.zip`.
2. Open your GitHub profile repository: **`vassellenha/vassellenha`**. If it doesn't exist, create a public repository named exactly `vassellenha` under that account.
3. Upload `README.md` and the **complete `assets/` folder** to the repository root, preserving relative paths.
4. Commit the files, then open `https://github.com/vassellenha` to see the actual profile.

The project contains `showcase/` and `scripts/` for local previews and future editing. They are optional for display, but keep them if you want reproducible source assets. The original uploaded ZIP is retained separately from this redesigned package.

## Important differences from typical README templates

- **21 motion graphics** are pre-rendered GIF files: 11 full-width sequences, 6 project cards and 4 contact buttons. They require no inline JavaScript or CSS.
- **5 navigation cards** link directly to profile sections.
- The colors and shape vocabulary are Persona 5-inspired. The character art uses Vassell's supplied original-character image, with his existing face, mask and pose preserved.
- The README contains human-readable profile data, project descriptions, and meaningful alternative text for every animation.
- All visuals are local. The activity graphic is explicitly **decorative**, while its custom call-to-action links to real GitHub activity.
- Every profile section uses designed image assets and professional English copy. The README contains no ordinary Markdown tables, stock badges, or default blue-text links.

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
- The user-supplied original character image is preserved at `assets/source/vassell-oc.png`.

You may freely replace personal information or links in `README.md`. Nothing has been pushed to GitHub; upload/commit is your decision.
