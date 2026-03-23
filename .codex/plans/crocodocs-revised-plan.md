# CrocoDocs Revised Plan

## What CrocoDocs Is

CrocoDocs is the docs migration and API generation toolchain used to move Flet Python docs from MkDocs to Docusaurus inside this monorepo.

It currently handles two jobs:

1. Bootstrap-migrate the MkDocs docs corpus into `website/docs`.
2. Generate structured API and helper artifacts consumed by the Docusaurus site.

The tool lives in `tools/crocodocs` and is invoked with:

```bash
uv --directory ./tools/crocodocs run crocodocs ...
```

---

## Current Status

CrocoDocs is already doing real production work.

Implemented and in active use:

- bootstrap migration from `sdk/python/packages/flet/docs` to `website/docs`
- generated docs manifest at `website/.crocodocs/docs-manifest.json`
- generated API data at `website/.crocodocs/api-data.json`
- generated MDX partials under `website/.crocodocs/*.mdx`
- left sidebar generation from the structured `nav` in `sdk/python/packages/flet/mkdocs.yml`
- Griffe-based API extraction for all configured Python packages
- deprecation extraction through `flet.utils.griffe_deprecations`
- alias serialization and alias page rendering
- stable qualified anchors for symbols, sections, and members
- runtime TOC injection for generated API headings
- docstring rendering through a real remark/unified markdown pipeline
- docstring support for admonitions, lists, fenced code, inline markdown, xrefs, and local `(c).` links
- sync of docs assets into Docusaurus-served static locations
- Cloudflare CI fixes for nested Griffe extraction and generated overview partials
- Cloudflare asset fix for `test-images` by sourcing from tracked `integration_tests` instead of ignored `packages/flet/site`

Known current workflow tradeoff:

- `website/package.json` runs bootstrap migration on every `yarn start` and `yarn build` via `yarn crocodocs:sync`
- this is intentional for now because the migrated docs are still derived artifacts, not yet hand-maintained canonical docs

---

## Current Pipeline

```text
MkDocs docs + mkdocs.yml
  -> crocodocs migrate --mode bootstrap
  -> website/docs
  -> website/sidebars.js
  -> website/.crocodocs/docs-manifest.json

website/docs
  -> crocodocs generate
  -> website/.crocodocs/api-data.json
  -> website/.crocodocs/code-examples.json
  -> website/.crocodocs/*.mdx
  -> website/.crocodocs/docs-manifest.json (refreshed)

Docusaurus
  -> website/docs + website/.crocodocs/*
  -> website/build
```

Current website scripts:

- `yarn crocodocs:migrate:bootstrap`
- `yarn crocodocs:generate`
- `yarn crocodocs:sync`
- `yarn start`
- `yarn build`

From `website/package.json`:

- `start = yarn crocodocs:sync && docusaurus start`
- `build = yarn crocodocs:sync && docusaurus build`

---

## Current Configuration

CrocoDocs config lives in:

- `tools/crocodocs/pyproject.toml`

Important sections:

- `[tool.crocodocs]`
- `[tool.crocodocs.member_filters]`
- `[tool.crocodocs.asset_mappings.*]`
- `[tool.crocodocs.packages]`

Current notable config behavior:

- source docs come from `sdk/python/packages/flet/docs`
- migrated docs go to `website/docs`
- sidebars are written to `website/sidebars.js`
- API data is written to `website/.crocodocs/api-data.json`
- generated partials go to `website/.crocodocs`
- `test-images` now resolve from `sdk/python/packages/flet/integration_tests`
- `test-images-charts` resolve from `sdk/python/packages/flet-charts/integration_tests`
- `assets` are copied only during migration
- member filtering is configurable, for example hidden methods like `init` and `before_update`

---

## What Was Added Or Corrected In This Session

This session materially changed CrocoDocs in these areas:

- replaced shallow AST API extraction with Griffe-backed extraction used for rendered docs
- improved generated API rendering:
  - method docs now render structured `Parameters`, `Returns`, and `Raises`
  - member signatures use real code blocks with copy support
  - member summaries and section styling were refined
  - member icons were added and aligned
- fixed missing API entries for public aliases and extension classes
- added support for alias pages with per-alias headings and right-side TOC entries
- switched member and alias anchors to fully qualified, collision-safe ids
- fixed cross-page hash scrolling to generated headings
- improved xref resolution:
  - qualified symbols
  - local `(c).` references
  - enum value targets
  - malformed MkDocs code-label reference patterns
- switched docstring rendering to a standard remark/unified markdown pipeline
- added docstring support for MkDocs-style `/// admonition`
- fixed docstring markdown edge cases that broke Cloudflare SSG
- fixed docs landing page image path behavior on direct loads
- fixed Cloudflare CI failures caused by:
  - nested `uv` + Griffe environment assumptions
  - MkDocs-dependent overview partial generation
  - MDX-unsafe raw docstring content
  - ignored `packages/flet/site/test-images` source paths
- corrected docs asset source mapping so deployed example images resolve from tracked sources

---

## Current Rendering Model In Website

Main website components:

- `website/src/components/crocodocs/ClassBlock.js`
- `website/src/components/crocodocs/ClassSummary.js`
- `website/src/components/crocodocs/ClassMembers.js`
- `website/src/components/crocodocs/ClassAll.js`
- `website/src/components/crocodocs/CodeExample.js`
- `website/src/components/crocodocs/Image.js`
- `website/src/components/crocodocs/utils.js`

Supporting pieces:

- `website/plugins/remark-api-links.js`
- `website/src/theme/DocItem/Layout/index.js`
- `website/src/css/custom.css`

Current principle:

- keep the Docusaurus runtime as small as practical
- push discovery, parsing, normalization, and ownership mapping into CrocoDocs generation
- keep only rendering and TOC injection in the website layer

---

## Current Limitations

These areas are still not fully cleaned up:

- many broken anchor warnings remain in blog and some publish docs
- asset warnings still exist for genuinely missing or stale source paths in the docs corpus
- CrocoDocs still performs bootstrap migration during normal local build/start
- some docs-source constructs are still handled by compatibility patches rather than a cleaner canonical syntax
- the generated website still depends on custom runtime rendering for API blocks instead of pure build-time MDX emission

---

## Next Practical Steps

### 1. Stabilize Remaining Docs Warnings

- fix known broken anchor warnings in blog pagination and stale publish links
- audit genuinely missing assets and either restore or remove them from docs

### 2. Reduce Bootstrap Coupling

Current state:

- `migrate --mode bootstrap` runs on every site build

Target state:

- bootstrap migration is used only while MkDocs remains the source of truth
- once migration is accepted, `website/docs` becomes canonical
- `generate` remains in the normal site build
- `migrate` becomes an explicit maintenance or one-off refresh command

### 3. Simplify Asset Story

Current state:

- CrocoDocs mirrors virtual asset roots into Docusaurus-served static locations

Target state:

- keep only tracked, reproducible source roots
- avoid any dependence on ignored/generated MkDocs output such as `packages/flet/site`
- document the supported asset roots clearly and keep them config-driven

### 4. Reduce Runtime Special Cases

Possible later cleanup:

- move more API summary structure to generated MDX if it lowers runtime complexity
- keep the current runtime TOC approach only where Docusaurus cannot express the structure at build time

### 5. Add Focused Validation

CrocoDocs still needs better automated validation around:

- migrated image references
- generated partial presence
- alias and member anchor stability
- xref integrity for common docs patterns
- a small fixture set of representative pages to catch regressions early

---

## Intended Post-Migration State

After the migration is complete, CrocoDocs should remain in the repo, but with a narrower role.

Target long-term split:

- `website/docs` is the canonical docs source
- CrocoDocs `generate` remains as the normal API/partials/build helper
- CrocoDocs `migrate` is no longer part of every build

That post-migration CrocoDocs role should be:

- refresh manifest from canonical Docusaurus docs
- extract API data from Python packages
- refresh `xref_map`
- refresh generated MDX partials
- sync reproducible asset roots

Things that should disappear after migration settles:

- repeated bootstrap conversion of MkDocs syntax during every build
- dependence on transitional compatibility fixes that only exist to bridge the old docs corpus

---

## Reference Files

Core tool files:

- `tools/crocodocs/src/crocodocs/cli.py`
- `tools/crocodocs/src/crocodocs/config.py`
- `tools/crocodocs/src/crocodocs/inventory.py`
- `tools/crocodocs/src/crocodocs/migrate.py`
- `tools/crocodocs/src/crocodocs/generate.py`
- `tools/crocodocs/src/crocodocs/griffe_extract_script.py`
- `tools/crocodocs/src/crocodocs/partials.py`
- `tools/crocodocs/src/crocodocs/sidebars.py`
- `tools/crocodocs/src/crocodocs/assets.py`

Website integration:

- `website/package.json`
- `website/src/components/crocodocs/*`
- `website/plugins/remark-api-links.js`
- `website/src/theme/DocItem/Layout/index.js`
- `website/src/css/custom.css`
