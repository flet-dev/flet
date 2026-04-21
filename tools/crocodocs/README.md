<p align="center">
  <img src="media/crocodocs-logo.png" alt="Crocodocs"></a>
</p>

# CrocoDocs

CrocoDocs is the internal documentation toolchain that generates structured API artifacts for the Flet Docusaurus website.

It lives in [tools/crocodocs](./) and is invoked by the website build in [website/package.json](../../website/package.json).

## What It Does

CrocoDocs runs a single `generate` command that:

- renders `website/sidebars.js` from the hand-authored `website/sidebars.yml`
- extracts API data from Python packages using Griffe
- builds the `xref_map` for cross-reference resolution
- generates MDX partials (CLI docs, PyPI index, cross-platform permissions)
- generates code example data from `sdk/python/examples`
- syncs image assets into Docusaurus static paths

## Build Pipeline

```text
website/docs (hand-authored)
website/sidebars.yml (hand-authored)
sdk/python/packages/*/src (Python source)
sdk/python/examples (code examples + screenshots)
  -> crocodocs generate
  -> website/sidebars.js
  -> website/.crocodocs/api-data.json
  -> website/.crocodocs/code-examples.json
  -> website/.crocodocs/*.mdx (partials)
  -> website/static/docs/* (synced assets)

Docusaurus
  -> website/build
```

### Building locally

```bash
# Requires Node.js 20+
nvm use 20

cd website
yarn install
yarn build        # runs crocodocs generate + docusaurus build
yarn start        # runs crocodocs watch + docusaurus dev server
```

### Running CrocoDocs directly

```bash
uv --directory ./tools/crocodocs run crocodocs generate
```

`yarn start` runs the Docusaurus dev server through `crocodocs watch`, which:

- performs an initial `generate`
- watches CrocoDocs inputs for changes
- regenerates API data, sidebars, partials, manifests, and synced assets after saves

Watched inputs include:

- `website/sidebars.yml`
- `sdk/python/packages/*/src`
- `sdk/python/examples`
- configured CrocoDocs asset source directories

`website/docs/**/*.{md,mdx}` is intentionally excluded: Docusaurus hot-reloads
those directly, so regenerating on every prose edit would be redundant. If you
add a new `<ClassAll symbol="…">` (or similar structural change) to a markdown
file, run `crocodocs generate` manually or restart the watcher so the manifest
is refreshed.

Watch and regenerate without starting Docusaurus:

```bash
uv --directory ./tools/crocodocs run crocodocs watch
```

Watch and run a child process, using `--` to separate the child command:

```bash
uv --directory ./tools/crocodocs run crocodocs watch --child-cwd ../../website -- yarn exec docusaurus start
```

## Configuration

CrocoDocs is configured in [tools/crocodocs/pyproject.toml](./pyproject.toml).

### `[tool.crocodocs]`

Core paths and settings:

| Key                   | Purpose                                  |
|-----------------------|------------------------------------------|
| `docs_path`           | Path to `website/docs`                   |
| `api_output`          | Where to write `api-data.json`           |
| `manifest_output`     | Where to write `docs-manifest.json`      |
| `partials_output_dir` | Where to write generated `.mdx` partials |
| `sidebars_source`     | Path to `sidebars.yml`                   |
| `sidebars_output`     | Path to generated `sidebars.js`          |
| `base_url`            | Base URL for docs routes (e.g. `/docs`)  |
| `examples_root`       | Path to code examples directory          |
| `extensions`          | Griffe extensions to load                |

### `[tool.crocodocs.packages]`

Maps Python import names to source roots. These packages are scanned during API extraction.

### `[tool.crocodocs.asset_mappings.*]`

Defines directories to bulk-copy into `website/static/docs/` during generate. Each mapping has:

| Key              | Purpose                                                   |
|------------------|-----------------------------------------------------------|
| `source_path`    | Source directory to copy from                             |
| `static_subpath` | Destination under `website/static/`                       |
| `include_exts`   | File extensions to copy (e.g. `[".png", ".gif", ".svg"]`) |

Current mappings:

- `examples` — `sdk/python/examples` (screenshots alongside code examples)
- `test-images` — `sdk/python/packages/flet/integration_tests` (golden test images)
- `test-images-charts` — `sdk/python/packages/flet-charts/integration_tests`

### `[tool.crocodocs.member_filters]`

Controls which class members are hidden from API output (e.g. `init`, `before_update`).

## `sidebars.yml` Format

[website/sidebars.yml](../../website/sidebars.yml) is the hand-authored sidebar source.
CrocoDocs generates [website/sidebars.js](../../website/sidebars.js) from it during `crocodocs generate`.

### Rules

- Top-level keys become sidebar categories
- Nested mapping keys become nested categories
- `Label: path.md` — labeled doc item
- `- path.md` — doc item with label inferred from the page title
- `_index: path.md` — category links to that document
- `_meta` — category options (e.g. `collapsed`)
- `_generated_index` — Docusaurus auto-generated index page with `title`, `slug`, `description`

### Example

```yml
docs:
  Getting started:
    - index.md
    - getting-started/installation.md

  Tutorials:
    Calculator: tutorials/calculator.md
    ToDo: tutorials/todo.md

  Reference:
    Controls:
      _generated_index:
        title: Controls
        slug: /controls
        description: Browse the complete catalog of controls.
      AlertDialog: controls/alertdialog.md
      AppBar: controls/appbar.md

    Services:
      _index: services/index.md
      _meta:
        collapsed: false
      Audio: services/audio/index.md
```

## Doc Page Format

### Front matter

```yaml
---
class_name: "flet.Container"
examples: "controls/container"              # relative to examples_root
example_images: "test-images/examples/material/golden/macos/container"  # relative to /docs/ static root
example_media: "examples/controls/container/media"  # relative to /docs/ static root
title: "Container"
---
```

- `examples` — path relative to the configured `examples_root`, used by `<CodeExample>`
- `example_images` / `example_media` — paths relative to `/docs/` static root, used by `<Image>`. No `../` navigation needed regardless of doc file depth.

### Cross-references in docstrings

Python docstrings use reST-style cross-references:

```python
"""See :class:`~flet.Page` and :attr:`flet.Control.visible`."""
```

Supported roles: `:class:`, `:attr:`, `:meth:`, `:func:`, `:data:`, `:mod:`, `:obj:`

The website strips a leading `flet.` or `ft.` from rendered labels automatically
and renders reST API cross-references as inline code links
(for example, `:attr:`flet.Control.visible`` displays as ``Control.visible``).
The `~` prefix still shortens the display to the last component
(for example, `:attr:`~flet.Control.visible`` displays as ``visible``).

### Cross-references in Markdown

Hand-written docs use standard Markdown links with relative `.md` paths:

```markdown
See [`Page`](../controls/page.md) and its [`visible`](../controls/control.md#flet.Control.visible) property.
```

Anchor format uses dots: `#flet.ClassName.member_name`

### Admonitions in docstrings

Google-style docstring sections are rendered as Docusaurus admonitions:

```python
"""
Note:
    This only works on mobile platforms.

Warning:
    Deprecated since v0.80.
"""
```

Supported admonition types: `note`, `tip`, `info`, `warning`, `danger`, `caution`. Other section types (like `Example:`) are rendered as `tip` admonitions. Non-recognized titles are rendered as plain text.

## How Rendering Works

CrocoDocs generates data; the Docusaurus website renders it.

Website components in [website/src/components/crocodocs/](../../website/src/components/crocodocs/):

| Component         | Purpose                                                 |
|-------------------|---------------------------------------------------------|
| `ClassAll.js`     | Full class page (summary + members)                     |
| `ClassSummary.js` | Class header with signature, image, inherits            |
| `ClassMembers.js` | Properties, events, and methods listing                 |
| `ClassBlock.js`   | Individual member rendering                             |
| `CodeExample.js`  | Inline code example with syntax highlighting            |
| `Image.js`        | Doc image with `/docs/` prefix for root-relative paths  |
| `utils.js`        | Markdown rendering, xref resolution, admonition support |

### Key rendering features

- Griffe-based class/function/alias rendering with Google-style docstring sections
- Qualified anchors: `#flet.ClassName.member_name`
- reST cross-reference resolution (`:class:`, `:attr:`, `:meth:`, etc.)
- Inherited member resolution via base class walking
- Public alias resolution (e.g. `flet_ads.BaseAd` → `flet_ads.base_ad.BaseAd`)
- Generated TOC injection for properties, events, and methods

## Verification

### Broken link check

Docusaurus checks for broken links and anchors during `yarn build`. The build fails if any are found.

### Broken image check

Run after building:

```bash
bash .github/scripts/check_docs.sh website/build
```

This scans all built HTML for `<img>` tags pointing to missing files and for unresolved reST xrefs (`:attr:`, `:class:`, etc.) in the output.

## CI Integration

The `docs_build` job in [.github/workflows/ci.yml](../../.github/workflows/ci.yml) runs the full build and verification on every push. It gates the publishing jobs — no release can proceed with broken documentation.

Cloudflare Pages runs the same build via `pip install uv && yarn build` with root directory set to `website/`.

## Source Files

Core tool:

- [cli.py](./src/crocodocs/cli.py) — CLI entry point
- [config.py](./src/crocodocs/config.py) — Configuration loading
- [generate.py](./src/crocodocs/generate.py) — Main generate command
- [griffe_extract_script.py](./src/crocodocs/griffe_extract_script.py) — Griffe API extraction
- [partials.py](./src/crocodocs/partials.py) — MDX partial generation
- [sidebars.py](./src/crocodocs/sidebars.py) — Sidebar YAML → JS conversion
- [assets.py](./src/crocodocs/assets.py) — Asset bulk copying
- [docs.py](./src/crocodocs/docs.py) — Markdown/MDX parsing helpers
- [pypi_index.py](./src/crocodocs/pypi_index.py) — PyPI package index renderer
- [scripts/](./src/crocodocs/scripts/) — CLI and permissions renderers (run via subprocess in `sdk/python` venv)

Website integration:

- [website/package.json](../../website/package.json) — Build scripts
- [website/plugins/remark-api-links.js](../../website/plugins/remark-api-links.js) — Remark plugin for xref resolution in Markdown
- [website/src/components/crocodocs/](../../website/src/components/crocodocs/) — React rendering components
- [website/src/theme/DocItem/Layout/index.js](../../website/src/theme/DocItem/Layout/index.js) — Swizzled doc layout
- [website/src/theme/DocCard/index.js](../../website/src/theme/DocCard/index.js) — Swizzled card component (compact, no emoji)
- [website/src/css/custom.css](../../website/src/css/custom.css) — Custom styles including generated-index grid
