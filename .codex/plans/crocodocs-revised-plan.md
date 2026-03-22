# CrocoDocs — Python API Docs for Docusaurus + Docs Migration

## Context

Flet docs currently live under `sdk/python/packages/flet/docs` and are built with MkDocs, `mkdocstrings`, and Griffe. The project is moving docs to Docusaurus and moving the website into the monorepo under `website/`.

CrocoDocs should cover two related but distinct jobs:

1. Migrate the existing MkDocs markdown corpus to Docusaurus-compatible markdown/MDX.
2. Rebuild Python API rendering for Docusaurus using generated structured data from Griffe.

The key constraint is that these jobs must not depend on each other in a circular way.

---

## Goals

- Preserve the current Flet docs corpus with minimal hand-editing.
- Preserve current API rendering behavior, including deprecations and cross-references.
- Preserve per-page macro options used today, not just a simplified subset.
- Make migration repeatable and testable.
- Keep Docusaurus runtime logic thin and move as much work as possible to build-time.

---

## Non-goals

- Reproduce MkDocs internals exactly.
- Build a fully generic docs migration framework.
- Introduce a heavy runtime data-loading layer in the website for content that can be generated at build time.

---

## Current Constraints From The Flet Docs Corpus

The current docs use more than the basic `class_name` / `examples` / `example_images` front matter. Real pages also use values such as:

- `example_media`
- `example_images_examples`
- secondary API symbols such as `popup_menu_item_class_name`
- secondary API symbols such as `snack_bar_action_class_name`

The current docs also rely on richer macro options than a minimal component API would expose, including:

- `separate_signature=False`
- `members_order="source"`
- `group_by_category=False`
- `summary={...}` overrides
- `extra={...}` overrides

Examples such as `types/icons.md`, `types/colors.md`, and `types/cupertinoicons.md` depend on those options.

CrocoDocs must model the real docs surface area, not an idealized subset.

---

## Architecture

Use two generated artifacts with clear ownership:

```text
MkDocs docs + mkdocs.yml
  -> crocodocs inventory
  -> crocodocs migrate
  -> migrated docs + docs-manifest.json

Python source packages + docs-manifest.json
  -> crocodocs generate
  -> api-data.json

Docusaurus
  -> migrated docs + api-data.json
  -> rendered site
```

### Generated artifacts

#### `docs-manifest.json`

`docs-manifest.json` records page routes, symbol ownership, render options, and page-level metadata.

CrocoDocs uses two modes for generating it:

- **Bootstrap mode**: while migrating from MkDocs, generate the manifest from the MkDocs source docs plus `mkdocs.yml`. This avoids depending on partially migrated Docusaurus output.
- **Steady-state mode**: once Docusaurus is the canonical docs source, generate the manifest by scanning `website/docs` source files and applying Docusaurus routing rules such as `id`, `slug`, file path, and doc hierarchy.

Purpose:

- define page routes and destination paths
- record which API symbols belong to which page
- record the render options needed for each symbol block
- record asset references and page-level metadata

This is the source of truth for symbol-to-page ownership.

In steady state, the manifest is built from Docusaurus source docs, not from built site output.

#### `api-data.json`

Built from Python packages plus `docs-manifest.json`.

Purpose:

- serialized API objects from Griffe
- deprecation metadata
- resolved type/docstring link targets
- `xref_map` derived from manifest-owned page routes

`xref_map` is always generated from the manifest. The only thing that changes over time is where the manifest comes from:

- during migration: MkDocs source docs plus `mkdocs.yml`
- after migration: Docusaurus source docs under `website/docs`

---

## Monorepo Layout

Target layout after website import:

```text
flet/
├── sdk/python/packages/flet/src/flet/
├── sdk/python/packages/flet/docs/
├── sdk/python/examples/
├── tools/crocodocs/
│   ├── pyproject.toml
│   └── src/crocodocs/
└── website/
    ├── docs/
    ├── plugins/
    ├── src/components/crocodocs/
    └── .crocodocs/
        ├── docs-manifest.json
        └── api-data.json
```

Before CrocoDocs migration work begins, copy the current website into this repo from the `main` branch of the sibling website repository at `/Users/feodor/projects/flet-dev/website` for the initial `website/` import.

---

## Phase 0: Scope Freeze

Before writing migration logic, define a fixed fixture set of representative pages:

- controls page with extra symbols:
  - `sdk/python/packages/flet/docs/controls/popupmenubutton.md`
- controls page with multiple image roots:
  - `sdk/python/packages/flet/docs/controls/layoutcontrol.md`
- type page with non-default API rendering:
  - `sdk/python/packages/flet/docs/types/icons.md`
- generated markdown macro page:
  - `sdk/python/packages/flet/docs/reference/binary-packages-android-ios.md`
- large prose-heavy page with custom macros:
  - `sdk/python/packages/flet/docs/publish/index.md`
- overview page:
  - `sdk/python/packages/flet/docs/services/index.md`

All design and implementation decisions must be tested against these pages before scaling to the full corpus.

---

## Phase 1: Inventory Tooling

### Command

All CrocoDocs CLI examples below assume invocation from the repository root. Because the CrocoDocs Python project lives under `tools/crocodocs/`, use `uv --directory ./tools/crocodocs run crocodocs ...`.

Stable project settings should live in `tools/crocodocs/pyproject.toml` under `[tool.crocodocs]`. Paths in that section are resolved relative to `tools/crocodocs/pyproject.toml`. Command-line flags override config values when provided.

```bash
uv --directory ./tools/crocodocs run crocodocs inventory
```

### Responsibilities

The inventory pass should scan the source docs tree and report:

- front matter keys in use
- macro names and argument shapes in use
- markdown reference link targets in use
- admonition, tabs, details, and code annotation patterns in use
- pages with nonstandard constructs
- symbols referenced from macros and front matter
- asset path patterns in use

### Deliverables

- machine-readable JSON report
- concise human-readable summary
- allowlist for pages that need manual migration review

### Why this phase exists

Without this inventory pass, migration logic will drift toward the common case and silently drop edge-case content that is already present in the corpus.

---

## Phase 2: Migration Contract

### Command

```bash
uv --directory ./tools/crocodocs run crocodocs migrate --mode bootstrap
```

### Mode

`migrate` is a bootstrap-only command.

Use while MkDocs docs are still the source of truth.

- input: MkDocs source docs plus `mkdocs.yml`
- responsibilities: convert MkDocs markdown/macros to Docusaurus markdown/MDX and generate the initial manifest
- outputs:
  1. migrated docs under `website/docs`
  2. `docs-manifest.json`

After bootstrap migration is complete, `migrate` is no longer part of the normal docs build workflow. Steady-state docs scanning and manifest refresh move into `generate`.

### Manifest schema

At minimum:

```json
{
  "version": "1.0",
  "pages": [
    {
      "source_path": "controls/popupmenubutton.md",
      "output_path": "controls/popupmenubutton.md",
      "route": "/docs/controls/popupmenubutton",
      "title": "PopupMenuButton",
      "front_matter": {
        "class_name": "flet.PopupMenuButton",
        "examples": "../../examples/controls/popup_menu_button",
        "example_media": "../examples/controls/popup_menu_button/media",
        "example_images": "../test-images/examples/material/golden/macos/popup_menu_button",
        "popup_menu_item_class_name": "flet.PopupMenuItem"
      },
      "symbol_blocks": [
        {
          "kind": "class_summary",
          "symbol": "flet.PopupMenuButton",
          "options": {
            "show_bases": true,
            "summary": {
              "attributes": true,
              "functions": true
            }
          }
        },
        {
          "kind": "class_members",
          "symbol": "flet.PopupMenuButton",
          "options": {
            "separate_signature": true
          }
        },
        {
          "kind": "class_all_options",
          "symbol": "flet.PopupMenuItem",
          "options": {
            "show_root_toc_entry": true,
            "show_bases": true,
            "separate_signature": true,
            "extra": {
              "show_class_docstring": true,
              "show_children": true
            }
          }
        }
      ]
    }
  ]
}
```

### Key rule

Do not collapse current macro behavior into a tiny prop set during migration. Preserve the macro semantics in the manifest so rendering can stay faithful.

---

## Phase 3: Content Conversion Strategy

### Conversions to perform automatically

| Source pattern | Migration output |
|---|---|
| `{{ class_summary(...) }}` | `<ClassSummary ... />` plus manifest entry |
| `{{ class_members(...) }}` | `<ClassMembers ... />` plus manifest entry |
| `{{ class_all_options(...) }}` | `<ClassAll ... />` plus manifest entry |
| `` ```python\n--8<-- "{{ examples }}/basic.py"\n``` `` | `<CodeExample path="..." />` plus manifest entry |
| `{{ image(...) }}` | markdown image or `<Image />` with explicit props |
| `/// admonition` | Docusaurus admonition syntax |
| `/// tab` | `<Tabs>/<TabItem>` |
| `/// details` | `<details><summary>...</summary>...</details>` |
| markdown reference links like `[x][flet.Foo]` | keep as-is for remark plugin |
| front matter values used in expressions | preserve as front matter variables and reference them from migrated MDX/components |

### Example migrated MDX

When source docs use front matter variables such as `class_name`, `examples`, or `example_images`, keep them in front matter and reference them directly from MDX:

```mdx
---
title: FilePicker
class_name: flet.FilePicker
examples: services/file_picker
example_images: /test-images/services/filepicker
---

import {ClassSummary, ClassMembers, CodeExample} from '@site/src/components/crocodocs';

<ClassSummary
  name={frontMatter.class_name}
  image={`${frontMatter.example_images}/image_for_docs.png`}
/>

## Examples

<CodeExample path={`${frontMatter.examples}/basic.py`} />

<ClassMembers name={frontMatter.class_name} />
```

### Build-time materialization preferred for v1

For the following macros, prefer generating final markdown during migration instead of deferring to runtime:

- `flet_cli_as_markdown(...)`
- `flet_pypi_index()`
- `cross_platform_permissions()`

These should be converted during migration into imports of generated MDX partials, not expanded inline. Example shape:

```mdx
import CliPublish from '@site/.crocodocs/cli-publish.mdx';
import PypiIndex from '@site/.crocodocs/pypi-index.mdx';
import Permissions from '@site/.crocodocs/cross-platform-permissions.mdx';

<CliPublish />
<PypiIndex />
<Permissions />
```

For code includes, use `CodeExample` from the start:

- `--8<-- "{{ examples }}/basic.py"` -> `<CodeExample path="..." />`

`CodeExample` should resolve example files from a configured examples root during the Docusaurus build, not by expanding them into repo-tracked fenced code blocks during migration.

### Code annotations

For lines like `# (1)!`:

- strip the `!`
- keep numeric markers
- keep the corresponding explanatory list
- mark such pages in the manifest as requiring review

---

## Phase 4: API Generation

### Command

```bash
uv --directory ./tools/crocodocs run crocodocs generate
```

### Configuration

`tools/crocodocs/pyproject.toml` should define a `[tool.crocodocs]` section for stable project settings, with CLI flags overriding config values.

At minimum, this section should support:

- `docs_path`
- `manifest_output`
- `api_output`
- `partials_output_dir`
- `packages`
- `extensions`
- `examples_root`
- image/assets source roots used by migrated docs

CrocoDocs should include all Python packages under `sdk/python/packages` from the beginning, not a manually curated subset. Package configuration can still be stored explicitly in `[tool.crocodocs.packages]`, but the initial project config should cover every package currently present under `sdk/python/packages/*/src`.

Representative shape:

```toml
[tool.crocodocs]
docs_path = "../../website/docs"
manifest_output = "../../website/.crocodocs/docs-manifest.json"
api_output = "../../website/.crocodocs/api-data.json"
partials_output_dir = "../../website/.crocodocs"
extensions = ["flet.utils.griffe_deprecations"]

[tool.crocodocs.packages]
flet = "../../sdk/python/packages/flet/src"
flet_ads = "../../sdk/python/packages/flet-ads/src"
flet_audio = "../../sdk/python/packages/flet-audio/src"
flet_audio_recorder = "../../sdk/python/packages/flet-audio-recorder/src"
flet_camera = "../../sdk/python/packages/flet-camera/src"
flet_charts = "../../sdk/python/packages/flet-charts/src"
flet_cli = "../../sdk/python/packages/flet-cli/src"
flet_code_editor = "../../sdk/python/packages/flet-code-editor/src"
flet_color_pickers = "../../sdk/python/packages/flet-color-pickers/src"
flet_datatable2 = "../../sdk/python/packages/flet-datatable2/src"
flet_desktop = "../../sdk/python/packages/flet-desktop/src"
flet_flashlight = "../../sdk/python/packages/flet-flashlight/src"
flet_geolocator = "../../sdk/python/packages/flet-geolocator/src"
flet_lottie = "../../sdk/python/packages/flet-lottie/src"
flet_map = "../../sdk/python/packages/flet-map/src"
flet_permission_handler = "../../sdk/python/packages/flet-permission-handler/src"
flet_rive = "../../sdk/python/packages/flet-rive/src"
flet_secure_storage = "../../sdk/python/packages/flet-secure-storage/src"
flet_video = "../../sdk/python/packages/flet-video/src"
flet_web = "../../sdk/python/packages/flet-web/src"
flet_webview = "../../sdk/python/packages/flet-webview/src"
```

CLI flags should override any configured value, for example:

```bash
uv --directory ./tools/crocodocs run crocodocs generate \
  --docs-path ../../website/docs-preview \
  --output ../../website/.crocodocs/api-data.preview.json
```

### Responsibilities

- scan Docusaurus source docs under `website/docs`
- refresh `docs-manifest.json` from Docusaurus docs and route resolution
- load all configured Python packages from `sdk/python/packages` with Griffe
- serialize classes, functions, enums, and dataclass-like types
- classify members using current Flet behavior
- preserve deprecation information using the existing Griffe extension
- resolve docstring cross-reference syntax to intermediate qualified targets
- generate `xref_map` from the refreshed `docs-manifest.json`, not by scanning built site output
- generate MDX partial files for `flet_cli_as_markdown(...)`, `flet_pypi_index()`, and `cross_platform_permissions()`

### Generated partials

`crocodocs generate` is responsible for writing generated MDX partials to:

- `website/.crocodocs/*.mdx`

At minimum, this includes files such as:

- `website/.crocodocs/cli-run.mdx`
- `website/.crocodocs/cli-publish.mdx`
- `website/.crocodocs/cli-create.mdx`
- `website/.crocodocs/pypi-index.mdx`
- `website/.crocodocs/cross-platform-permissions.mdx`

CLI docs must be generated as a separate MDX partial for each command or subcommand page that needs one. Use a deterministic filename derived from the command path, for example:

- `flet run` -> `cli-run.mdx`
- `flet publish` -> `cli-publish.mdx`
- `flet build ios` -> `cli-build-ios.mdx`

The migration step rewrites source macro calls into imports/usages of those generated partials. In steady state, `generate` refreshes both the manifest and the partial contents before the Docusaurus build.

### `xref_map` generation

Build `xref_map` by using manifest ownership:

- page-level symbol -> page route
- member-level symbol -> `page_route#member-anchor`

Member anchors should use a deterministic normalization of the rendered member name, and the renderer should be the source of truth for anchor generation. CrocoDocs generation and rendering must share the same anchor-building helper so `xref_map` and rendered headings cannot drift.

This works in both phases:

- **Bootstrap mode**: the manifest is first created by `migrate` from MkDocs source docs and migration metadata
- **Steady-state mode**: the manifest is refreshed by `generate` from Docusaurus source docs and Docusaurus route resolution

This means every symbol rendered by `ClassSummary`, `ClassMembers`, or `ClassAll` can be mapped directly, without inferring routes from built HTML or other generated site output.

### Deprecations

Reuse the behavior in:

- `sdk/python/packages/flet/src/flet/utils/griffe_deprecations.py`

Do not duplicate deprecation extraction logic in CrocoDocs if it can be shared.

### Cross-reference behavior

CrocoDocs docstring resolution should remain compatible with the existing docs conventions and patch behavior in:

- `sdk/python/packages/flet/docs/extras/macros/python_xref_patch.py`

The goal is semantic parity, not a brand-new cross-reference dialect.

---

## Phase 5: Docusaurus Rendering Layer

Keep the website runtime small.

### Components

Use one real rendering primitive and thin wrappers:

- `ClassBlock`
- `ClassSummary`
- `ClassMembers`
- `ClassAll`
- `CodeExample`

Wrappers should mostly translate props into a normalized `ClassBlock` render config.

In steady state, symbol ownership for manifest generation should come from explicit CrocoDocs directives/components in docs source, such as `ClassSummary`, `ClassMembers`, and `ClassAll`. Front matter alone should not imply API symbol ownership.

### Suggested prop model

Do not expose only:

- `name`
- `separateSignature`

Instead allow rendering props that match the manifest-driven options needed by existing pages, including:

- `groupByCategory`
- `membersOrder`
- `showSummary`
- `showMembers`
- `showDocstring`
- `showBases`
- `summary`
- `extra`

### Remark plugin

Implement a remark plugin to resolve markdown reference links:

- input: `[text][flet.FilePicker]`
- source of truth: `.crocodocs/api-data.json` `xref_map`
- output: concrete links in the built page

The plugin should resolve any mapped identifier, not just `flet.*`, so extension packages continue to work.

### Images

For external images, use a build-time copy step plus stable output URLs.

Keep image handling simple:

- migrate source image references to concrete output URLs
- copy external image directories during build
- avoid complex runtime asset lookup where possible

### Code examples

`CodeExample` should render external example files referenced by migrated docs.

- input: a normalized example path recorded during migration
- source of truth: configured examples root in the CrocoDocs/Docusaurus build
- output: syntax-highlighted code block in the built page

`CodeExample` should be part of the steady-state docs model, not a temporary migration bridge.

### Generated markdown content

The content produced by these source macros:

- `flet_cli_as_markdown(...)`
- `flet_pypi_index()`
- `cross_platform_permissions()`

should be emitted by `crocodocs generate` as MDX partial files under `website/.crocodocs/` and then rendered by Docusaurus natively via MDX imports in migrated pages.

Phase 5 does not require a dedicated React component for them. The display mechanism is:

- CrocoDocs generate writes `.mdx` partial files into `website/.crocodocs/`
- the migrated page imports those partial files directly
- Docusaurus renders the resulting markdown/MDX using its normal docs pipeline

This keeps runtime complexity low and avoids building specialized client-side renderers for content that is already fully known at build time.

---

## Phase 6: Website Integration

### `website/package.json`

The build sequence should become:

```json
{
  "scripts": {
    "crocodocs:inventory": "cd .. && uv --directory ./tools/crocodocs run crocodocs inventory",
    "crocodocs:generate": "cd .. && uv --directory ./tools/crocodocs run crocodocs generate",
    "crocodocs:migrate:bootstrap": "cd .. && uv --directory ./tools/crocodocs run crocodocs migrate --mode bootstrap",
    "start": "yarn crocodocs:generate && docusaurus start",
    "build": "yarn crocodocs:generate && docusaurus build"
  }
}
```

`crocodocs:migrate:bootstrap` is a one-time or rare maintenance command. Normal local builds and CI should use `crocodocs:generate`.

### Build artifacts

Gitignore generated files:

- `website/.crocodocs/docs-manifest.json`
- `website/.crocodocs/api-data.json`
- `website/.crocodocs/*.mdx`

Generated MDX partials under `website/.crocodocs/` should be treated as generated build artifacts and gitignored. CI and local builds should regenerate them via `crocodocs generate`.

---

## Implementation Files

### Python CLI

`tools/crocodocs/pyproject.toml` should define both:

- a console script entry point so the CLI command inside that project is `uv run crocodocs ...`
- a `[tool.crocodocs]` section for project configuration, with CLI flags overriding config values

From the repository root, invoke it as `uv --directory ./tools/crocodocs run crocodocs ...`.

All CLI commands must provide:

- progress output while running, with clear stage names and useful item counts
- a final summary block at the end, even on partial-success runs

Minimum summary expectations by command:

- `inventory`: number of docs scanned, macro/front matter patterns found, and pages flagged for manual review
- `migrate`: number of pages converted, imports/components inserted, and files or pages needing follow-up
- `generate`: number of docs scanned, packages loaded, symbols serialized, partials generated, and unresolved references or warnings

Progress and summaries should be human-readable first. Structured output such as JSON can be added separately if needed, but should not replace the default terminal summary.

- `tools/crocodocs/pyproject.toml`
- `tools/crocodocs/src/crocodocs/__main__.py`
- `tools/crocodocs/src/crocodocs/inventory.py`
- `tools/crocodocs/src/crocodocs/migrate.py`
- `tools/crocodocs/src/crocodocs/generate.py`
- `tools/crocodocs/src/crocodocs/schema.py`
- `tools/crocodocs/src/crocodocs/xref.py`
- `tools/crocodocs/src/crocodocs/assets.py`
- `tools/crocodocs/src/crocodocs/partials.py`

### Website side

- `website/plugins/crocodocs-plugin/index.js`
- `website/plugins/remark-api-links.js`
- `website/src/components/crocodocs/ClassBlock.js`
- `website/src/components/crocodocs/ClassSummary.js`
- `website/src/components/crocodocs/ClassMembers.js`
- `website/src/components/crocodocs/ClassAll.js`
- `website/src/components/crocodocs/CodeExample.js`
- `website/src/components/crocodocs/Image.js`
- `website/src/components/crocodocs/crocodocs.module.css`

---

## Implementation Steps

### Step 1: Inventory
1. Build inventory command.
2. Scan the full docs corpus.
3. Freeze the migration support matrix from actual usage.

### Step 2: Migration
4. Build migration pipeline.
5. Generate `docs-manifest.json`.
6. Migrate only fixture pages first.
7. Verify fixture parity before migrating the full corpus.

### Step 3: API data
8. Build Griffe extraction and serialization.
9. Reuse Flet deprecation handling.
10. Generate `xref_map` from the manifest.
11. Validate representative API objects and links.

### Step 4: Website rendering
12. Build the remark link plugin.
13. Build `ClassBlock` and thin wrapper components.
14. Wire asset copying and global data loading.
15. Validate rendering on fixture pages.

### Step 5: Full rollout
16. Migrate the full corpus.
17. Run parity review on high-value sections.
18. Fix edge cases found by inventory and validation.
19. Add CI checks to prevent drift.

---

## Validation

### Must-pass checks

1. Fixture pages render with no dropped content.
2. `docs-manifest.json` resolves all page routes and symbol owners.
3. `api-data.json` contains correct entries for representative symbols such as:
   - `flet.FilePicker`
   - `flet.Column`
   - `flet.AlertDialog`
   - `flet.Icons`
4. markdown reference links resolve correctly for:
   - class links
   - member links
   - extension package symbols
5. deprecations render correctly from current Griffe extension behavior.
6. migrated overview pages preserve navigation intent.
7. search indexes API headings and migrated prose content.

### Parity review pages

At minimum compare the Docusaurus result against current MkDocs output for:

- controls
- services
- types
- CLI docs
- publish/reference docs

### Failure conditions

Do not proceed to full migration if any of the following are true:

- manifest lacks symbol ownership for rendered API pages
- fixture pages lose secondary symbols or image paths
- type pages with non-default options render incorrectly
- cross-reference coverage depends on scanning migrated docs after the fact

### Default command failure policy

By default, CrocoDocs commands should warn and continue for recoverable issues such as:

- unresolved cross-references
- missing example files referenced by `CodeExample`
- missing optional assets
- partial-generation failures that affect only a subset of generated content

Commands should exit non-zero by default for hard failures such as:

- unreadable configured docs roots
- unreadable configured package roots
- invalid or unreadable CrocoDocs configuration
- manifest write failures
- API data write failures

A future `--strict` mode may promote warnings to errors, but the default behavior should favor producing usable output with a clear summary of warnings.

---

## Key Design Decisions

- `xref_map` must come from `docs-manifest.json`, not regex over migrated docs.
- migration must preserve real macro/front matter behavior used by current docs.
- build-time generation is preferred over runtime file reads for markdown partials and code examples.
- React components should be thin; Python tooling should do the heavy lifting.
- fixture-based validation is required before corpus-wide migration.

---

## References

- `sdk/python/packages/flet/src/flet/utils/griffe_deprecations.py`
- `sdk/python/packages/flet/docs/extras/macros/__init__.py`
- `sdk/python/packages/flet/docs/extras/macros/python_xref_patch.py`
- `sdk/python/packages/flet/docs/templates/python_xref/material/children.html.jinja`
- `sdk/python/packages/flet/mkdocs.yml`
