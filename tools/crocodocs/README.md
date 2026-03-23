# CrocoDocs

CrocoDocs is the internal documentation toolchain that migrates Flet Python docs from MkDocs to Docusaurus and generates the structured API artifacts consumed by the website.

It lives in:

- [tools/crocodocs](./)

It is currently used by the website build in:

- [website/package.json](../../website/package.json)

## What It Does

CrocoDocs currently handles two related jobs:

1. Bootstrap-migrate the MkDocs docs corpus into `website/docs`.
2. Generate Docusaurus-side artifacts from migrated docs and Python packages.

The tool exists because the old docs system and the new site are different in three important ways:

- the source docs currently come from the MkDocs corpus under `sdk/python/packages/flet/docs`
- API rendering in MkDocs depended on `mkdocstrings` and Griffe
- Docusaurus needs generated MDX/docs data, sidebars, and static assets arranged differently

## Current Pipeline

```text
sdk/python/packages/flet/docs + mkdocs.yml
  -> crocodocs migrate --mode bootstrap
  -> website/docs
  -> website/sidebars.yml
  -> website/sidebars.js
  -> website/.crocodocs/docs-manifest.json

website/docs
  -> crocodocs generate
  -> website/.crocodocs/api-data.json
  -> website/.crocodocs/code-examples.json
  -> website/.crocodocs/*.mdx
  -> refreshed docs-manifest.json

Docusaurus
  -> website/build
```

At the moment the website runs both phases on every local build:

- `yarn start`
- `yarn build`

through:

- `yarn crocodocs:sync`

This is still the right tradeoff while the MkDocs docs remain the source of truth.

## Commands

All commands are run from the repository root:

```bash
uv --directory ./tools/crocodocs run crocodocs inventory
uv --directory ./tools/crocodocs run crocodocs migrate --mode bootstrap
uv --directory ./tools/crocodocs run crocodocs generate
```

### `inventory`

Scans the source docs corpus and reports what CrocoDocs needs to support.

Current use:

- inspect front matter keys
- inspect macro usage
- inspect directive/admonition patterns
- inspect reference link and asset patterns

### `migrate --mode bootstrap`

Converts the MkDocs docs corpus into Docusaurus-compatible markdown/MDX.

Current responsibilities:

- migrate docs from `sdk/python/packages/flet/docs` to `website/docs`
- convert macros to CrocoDocs components or generated partial imports
- convert MkDocs directives such as admonitions, tabs, and details
- normalize image handling for Docusaurus/MDX
- write the initial docs manifest
- write `website/sidebars.yml` from `mkdocs.yml`
- copy bootstrap asset roots needed by migrated docs

### `generate`

Runs on top of migrated docs and Python packages.

Current responsibilities:

- scan `website/docs`
- refresh `website/.crocodocs/docs-manifest.json`
- render `website/sidebars.js` from `website/sidebars.yml`
- extract API data with Griffe
- serialize classes, functions, aliases, members, docstrings, and deprecations
- build `xref_map`
- generate MDX partials
- generate code example data
- sync configured virtual asset roots into Docusaurus-served static paths

## Main Outputs

CrocoDocs writes these primary outputs:

- [website/docs](../../website/docs)
- [website/sidebars.yml](../../website/sidebars.yml)
- [website/sidebars.js](../../website/sidebars.js)
- [website/.crocodocs/docs-manifest.json](../../website/.crocodocs/docs-manifest.json)
- [website/.crocodocs/api-data.json](../../website/.crocodocs/api-data.json)
- [website/.crocodocs/code-examples.json](../../website/.crocodocs/code-examples.json)
- [website/.crocodocs](../../website/.crocodocs) generated partials such as:
  - `cli-build.mdx`
  - `controls-overview.mdx`
  - `cookbook-overview.mdx`
  - `services-overview.mdx`

## Configuration

CrocoDocs is configured in:

- [tools/crocodocs/pyproject.toml](./pyproject.toml)

Key sections:

### `[tool.crocodocs]`

Core paths and settings:

- source docs path
- `mkdocs.yml` path
- output docs path
- manifest output
- API output
- partial output directory
- sidebar source
- sidebar output
- base URL
- Griffe extensions

### `[tool.crocodocs.packages]`

Maps import package names to source roots under `sdk/python/packages/*/src`.

These are the packages scanned during API generation.

### `[tool.crocodocs.asset_mappings.*]`

Defines virtual docs asset roots.

Current important mappings:

- `examples` -> `sdk/python/examples`
- `test-images` -> `sdk/python/packages/flet/integration_tests`
- `assets` -> `sdk/python/packages/flet/docs/assets`
- `test-images-charts` -> `sdk/python/packages/flet-charts/integration_tests`

Each mapping has:

- `source_path`
- `static_subpath`
- `copy_during`

### `[tool.crocodocs.member_filters]`

Controls which members are hidden from generated API output.

Current use:

- hide framework/internal methods like `init` and `before_update`

## `sidebars.yml` Format

CrocoDocs now treats [website/sidebars.yml](../../website/sidebars.yml) as the canonical sidebar source and generates [website/sidebars.js](../../website/sidebars.js) from it during `crocodocs generate`.

Current flow:

- `crocodocs migrate --mode bootstrap` writes `sidebars.yml` from `mkdocs.yml`
- `crocodocs generate` reads `sidebars.yml` and emits `website/sidebars.js`

The goal is to keep the authoring format compact and close to MkDocs nav, while still allowing Docusaurus-specific metadata when needed.

### Rules

- top-level section keys become sidebar categories
- nested mapping keys become nested categories
- `Label: path.md` means a labeled doc item
- `- path.md` means a doc item whose label is inferred from the page
- `_index: path.md` means the category links to that document
- `_meta` holds category options such as `collapsed`

### Compact Example

```yml
docs:
  Learn:
    Getting started:
      - index.md
      - getting-started/installation.md
      - getting-started/create-flet-app.md

    Tutorials:
      Calculator: tutorials/calculator.md
      ToDo: tutorials/todo.md

  API Reference:
    Services:
      _index: services/index.md
      - services/audio.md
      - services/clipboard.md
```

### Example With Metadata

```yml
docs:
  API Reference:
    Services:
      _index: services/index.md
      _meta:
        collapsed: false

      Audio: services/audio.md
      Clipboard: services/clipboard.md
```

### Why `_index` And `_meta` Are Separate

`_index` is structural: it identifies the doc used as the category link.

`_meta` is behavioral: it carries optional category settings such as:

- `collapsed`
- future Docusaurus-related options if we need them

This keeps the format compact for normal cases and still extensible when the sidebar needs extra control.

## How Rendering Works

CrocoDocs does not emit final HTML. It feeds the Docusaurus website runtime.

Main website pieces:

- [website/src/components/crocodocs/ClassBlock.js](../../website/src/components/crocodocs/ClassBlock.js)
- [website/src/components/crocodocs/ClassSummary.js](../../website/src/components/crocodocs/ClassSummary.js)
- [website/src/components/crocodocs/ClassMembers.js](../../website/src/components/crocodocs/ClassMembers.js)
- [website/src/components/crocodocs/ClassAll.js](../../website/src/components/crocodocs/ClassAll.js)
- [website/src/components/crocodocs/CodeExample.js](../../website/src/components/crocodocs/CodeExample.js)
- [website/src/components/crocodocs/utils.js](../../website/src/components/crocodocs/utils.js)

Current rendering features:

- Griffe-based class/function/alias rendering
- qualified anchors for symbols and members
- generated TOC injection
- xref resolution across pages and within local class pages
- structured method docs (`Parameters`, `Returns`, `Raises`)
- docstring rendering through remark/unified
- support for MkDocs-style admonitions in Python docstrings

## Why Some Things Still Look Transitional

CrocoDocs is still in migration mode.

That means some current behavior is intentionally transitional:

- bootstrap migration runs during normal website build
- some MkDocs syntax is still normalized rather than eliminated at the source
- some website-side logic exists to preserve behavior until the docs source becomes canonical in Docusaurus

This is expected for now.

## What Will Change After Migration

Once `website/docs` becomes the canonical docs source, CrocoDocs should shrink in scope.

Target long-term role:

- keep `generate`
- stop running bootstrap migration on every build
- keep API extraction, xref generation, manifest refresh, partial generation, and asset syncing
- remove compatibility logic that only exists to bridge the old MkDocs corpus

Expected post-migration build flow:

```text
website/docs
  -> crocodocs generate
  -> docusaurus build
```

At that point:

- `migrate --mode bootstrap` becomes an explicit maintenance tool, not a normal build step
- asset mappings should only point to tracked, reproducible source trees
- the website runtime should only keep the rendering logic that still adds clear value

## Notes For CI / Cloudflare

Two CI-specific issues already shaped the current implementation:

### API extraction

CrocoDocs no longer depends on nesting a second `uv run` into `sdk/python` for Griffe extraction. That was fragile in CI.

### Test-image sources

CrocoDocs must source `test-images` from tracked integration test directories, not from ignored `packages/flet/site` output.

That is why the current mapping uses:

- `sdk/python/packages/flet/integration_tests`

instead of:

- `sdk/python/packages/flet/site/test-images`

## Relevant Source Files

Core tool files:

- [tools/crocodocs/src/crocodocs/cli.py](./src/crocodocs/cli.py)
- [tools/crocodocs/src/crocodocs/config.py](./src/crocodocs/config.py)
- [tools/crocodocs/src/crocodocs/inventory.py](./src/crocodocs/inventory.py)
- [tools/crocodocs/src/crocodocs/migrate.py](./src/crocodocs/migrate.py)
- [tools/crocodocs/src/crocodocs/generate.py](./src/crocodocs/generate.py)
- [tools/crocodocs/src/crocodocs/griffe_extract_script.py](./src/crocodocs/griffe_extract_script.py)
- [tools/crocodocs/src/crocodocs/partials.py](./src/crocodocs/partials.py)
- [tools/crocodocs/src/crocodocs/sidebars.py](./src/crocodocs/sidebars.py)
- [tools/crocodocs/src/crocodocs/assets.py](./src/crocodocs/assets.py)

Website integration:

- [website/package.json](../../website/package.json)
- [website/plugins/remark-api-links.js](../../website/plugins/remark-api-links.js)
- [website/src/theme/DocItem/Layout/index.js](../../website/src/theme/DocItem/Layout/index.js)
- [website/src/css/custom.css](../../website/src/css/custom.css)
