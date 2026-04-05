---
name: flet-release-announcement
description: Create or update a Flet release announcement blog post from changelog notes, matching existing /blog style. Use when asked to draft, plan, or revise posts like "Flet X.Y.Z release announcement" with major feature sections, screenshots, code samples, upgrade instructions (pip and uv/pyproject.toml), and a compact "other changes" summary.
---

# Flet Release Announcement

Use this skill when the user asks to plan/write/refine a Flet release blog post.

## Inputs to collect

- Release version (example: `0.81.0`)
- Target blog file path (or create one)
- Changelog source (local repo path or GitHub link)
- Preferred title (if provided)
- Any must-include or must-exclude topics

If inputs are missing, infer from open files and recent release posts.

## Style targets

- Match tone/structure of recent release posts in `/blog`.
- Keep writing practical and concise.
- Avoid excessive emoji and unnecessary bold formatting.
- Lead with substantial features; keep long tail in "Other changes and bug fixes".
- Format GitHub issue/PR references as Markdown link labels like `[#6190](https://github.com/.../issues/6190)`, not bare URLs.
- Wrap control/service/type names in backticks in prose and labels (for example, `` `Clipboard` docs ``).

## Workflow

1. Inspect prior release posts for structure
- Read 2-3 recent release posts in `/blog`.
- Reuse conventions: frontmatter, short intro, highlights bullets, `<!-- truncate -->`, upgrade section, major feature sections, improvements, other changes, conclusion.

2. Ground facts in changelog
- Use the exact release section from `CHANGELOG.md` or the release branch/tag anchor.
- Do not invent claims, platforms, or options.
- Keep issue/PR links for traceability.

3. Select major vs other items
- Promote 5-8 most substantial features to dedicated sections.
- Keep less substantial or niche items in compact bullets at the end.

4. Source screenshots
- Prefer existing docs/integration golden images.
- Typical sources:
  - `sdk/python/packages/flet/integration_tests/.../golden/...`
  - `sdk/python/examples/.../media/...`
- Copy selected assets into website repo:
  - `static/img/blog/flet-<version>/...`
- If an image is unavailable, explicitly note the gap.

5. Build each major feature section
For each major feature include:
- What it is
- What problem it solves
- Short code sample
- Screenshot (`<img src="..." className="screenshot-..." />`)
- "More info" links (docs + issue/PR)

6. Upgrade instructions
Always include both flows:

- pip:
```bash
pip install 'flet[all]' --upgrade
```

- uv + `pyproject.toml`:
```bash
uv sync --upgrade
```

```bash
uv sync --upgrade-package flet \
  --upgrade-package flet-cli \
  --upgrade-package flet-desktop \
  --upgrade-package flet-web
```

On Linux, mention that some setups use `flet-desktop-light` instead of `flet-desktop`; in that case `--upgrade-package flet-desktop-light` should be used.

7. Verify before handoff
- Title and slug align with repo naming conventions.
- All image paths exist in `static/img/...`.
- Docs/issue links resolve and match section claims.
- "Other changes" list mirrors changelog items accurately.

## Useful command patterns

```bash
rg --files blog | rg 'release-announcement|flet-v-0-'
sed -n '1,260p' blog/<recent-release-post>.md
sed -n '1,260p' <flet-repo>/CHANGELOG.md
rg --files <flet-repo>/sdk/python/packages/flet/integration_tests | rg '<feature>.*(png|gif|jpg)$'
mkdir -p static/img/blog/flet-<version>
cp <source-image> static/img/blog/flet-<version>/<name>.png
```

## Output checklist

- New or updated blog post in `/blog`
- Referenced screenshots copied under `static/img/blog/flet-<version>/`
- Final text includes major sections, upgrades (pip + uv), improvements, and concise other changes
