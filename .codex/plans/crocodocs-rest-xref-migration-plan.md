# CrocoDocs reST Xref Migration Plan

## Goal

Migrate Python docstring cross-references under `sdk/python/packages/*/src` from the
current mkdocs-style form:

```text
[`Label`][target]
```

to reStructuredText inline roles:

```text
:class:`BarometerReadingEvent`
:meth:`FilePicker.pick_files`
:attr:`start_angle`
:func:`some_function`
:data:`SOME_CONSTANT`
```

The branch target is Docusaurus + CrocoDocs, not MkDocs. The immediate blocker is
not content conversion, but CrocoDocs/Docusaurus rendering support for reST roles in
docstrings.

Canonical source convention for this migration should follow normal Python/Sphinx
practice:

- prefer standard Sphinx roles in docstrings
- every migrated xref should be either:
  - local-context form, when the surrounding class/module context is sufficient
  - globally qualified form, when the target is outside the local context
- use `~` on globally qualified targets when only the final display segment should be
  shown
- avoid explicit-title syntax in docstrings

---

## Current Findings

Migration surface, scoped to actual docstring literals in package `src/` trees:

- `3010` mkdocs-style xrefs
- `248` source files
- `17` packages affected
- `flet` dominates the corpus with `2652` xrefs across `181` files
- `27` docstring xrefs use non-symbol/custom label text and will likely need prose
  rewrites

Most common xref variants found in real source docstrings:

| Variant | Count | Example |
| --- | ---: | --- |
| `absolute-prefix-dot` | 1601 | ``[`Page`][flet.]`` |
| `(c).` | 1032 | ``[`controls`][(c).]`` |
| `absolute-explicit` | 170 | ``[`Page.route`][flet.Page.route]`` |
| `(p).` | 140 | ``[`PieChartSection`][(p).]`` |
| `(c).member` | 35 | ``[`show()`][(c).show]`` |
| `(p).member` | 9 | ``[`selected`][(p).CandlestickChartSpot.selected]`` |
| `(m).member` | 9 | ``[`encrypt()`][(m).encrypt]`` |
| `(m).` | 7 | ``[`ColorPicker`][(m).]`` |
| `..` | 5 | ``[`fill_color`][..]`` |
| `(c)` | 2 | ``[`Once`][(c)]`` |

Variants supported by previous `python_xref` conventions but not found in this source
scan:

- `(p)` exact
- `(m)` exact
- `^` parent traversal
- `?` inventory false-positive bypass

Relevant current consumers:

- `website/src/components/crocodocs/utils.js`
- `website/plugins/remark-api-links.js`

Relevant current generator/data source:

- `tools/crocodocs/src/crocodocs/generate.py`

`generate.py` already emits `xref_map`. The missing piece is reST role parsing and
resolution in the Docusaurus/CrocoDocs consumers.

---

## Recommended Order

### 1. Add reST role support before content migration

Do not bulk-convert docstrings first.

Current website-side rendering only understands mkdocs-style references:

- markdown link references
- malformed inline-code reference repairs
- local shorthand targets such as `(c).`

If docstrings are converted now, generated API pages will render raw `:class:`,
`:attr:`, `:meth:` text.

### 2. Keep mkdocs-style support temporarily

During migration, both formats should resolve:

- old mkdocs-style xrefs continue to work
- new reST roles also work

This allows package-by-package conversion and avoids a flag day.

### 3. Convert docstrings with a docstring-aware tool

Rewriting must operate on parsed docstring literals only, not on raw file text.

Reason:

- raw regex replacement will hit ordinary string literals
- `flet-cli` already contains many bracket/indexing patterns that look like xrefs

### 4. Remove mkdocs-style compatibility only after the last package is migrated

That cleanup should be last, not bundled into the first parser change.

---

## Exact Support Changes

### Phase 1: Add reST role parsing to CrocoDocs docstring rendering

Primary target:

- `website/src/components/crocodocs/utils.js`

Recommended implementation:

1. Add a reST inline role preprocessor alongside `preprocessCrossReferenceMarkdown()`.
2. Process reST roles before markdown parsing, just as mkdocs-style xrefs are
   preprocessed before `remark-parse`.
3. Skip fenced code blocks and inline code spans while rewriting.
4. Resolve recognized reST roles using surrounding class/module/package context and
   the existing `xref_map`.
5. Convert resolved roles into normal markdown links before markdown parsing.
6. Reuse existing symbol resolution logic where possible.

Recommended new helpers in `utils.js`:

- `REST_XREF_RE`
- `parseRestCrossReference(roleText)`
- `resolveRestCrossReference(role, target, context)`
- `preprocessRestCrossReferenceMarkdown(text, context)`

Recommended supported roles for phase 1:

- `:class:`
- `:attr:`
- `:meth:`
- `:func:`
- `:data:`
- `:mod:`
- optional acceptance of `:py:class:`, `:py:attr:`, `:py:meth:`, `:py:func:`,
  `:py:data:`, `:py:mod:` as aliases
- optional support for `:obj:` as a compatibility fallback, but not as the preferred
  authoring style

Recommended normalization rules:

- accept leading `~` and strip it before lookup
- implement Sphinx-like shortened display for `~` targets:
  - `:class:`~flet.BarometerReadingEvent`` displays `BarometerReadingEvent`
  - `:meth:`~flet.FilePicker.pick_files`` displays `FilePicker.pick_files`
- support local member references when context is known:
  - `:attr:`start_angle``
  - `:attr:`use_center``
  - `:meth:`upload``
- support globally qualified public API references:
  - `:class:`flet.BarometerReadingEvent``
  - `:meth:`flet.FilePicker.pick_files``
- allow `~` on globally qualified references to shorten visible text:
  - `:class:`~flet.BarometerReadingEvent``
  - `:meth:`~flet.FilePicker.pick_files``
- accept method targets written with `()` and normalize them for lookup, but do not
  make parentheses the canonical migrated source form
- let CrocoDocs resolve unqualified targets from the surrounding object/module
  context before falling back to global candidate expansion
- prefer `:data:` for constants and enum-like values
- keep `:obj:` only as an internal/compatibility escape hatch for unresolved
  ambiguous symbols

Recommended non-goals for phase 1:

- do not parse full Sphinx/reST syntax generally
- do not change author-written Markdown docs yet
- do not remove mkdocs-style xref handling yet

### Phase 2: Optional parity in author-written docs

Secondary target, only if reST roles will also appear in hand-authored Markdown/MDX:

- `website/plugins/remark-api-links.js`

Recommended scope:

- add the same reST role rewrite there
- keep it separate from docstring runtime support unless docs authors begin using
  reST roles outside API docstrings

This is optional for the docstring migration itself because generated API docstrings
are rendered by `website/src/components/crocodocs/utils.js`, not by the remark plugin.

### Phase 3: Validation hooks

Recommended validation additions:

- fixture docstrings covering every supported role and target form
- one generated API page snapshot or DOM assertion for each role family
- regression checks for mixed old/new syntax during transition

---

## Conversion Table

This table covers every xref variant found in real source docstrings and the proposed
canonical reST equivalent.

Principle:

- convert custom mkdocs-style targets to standard Sphinx source forms, not to custom
  explicit-label links
- use the narrowest accurate reST role when symbol kind is known
- prefer local member refs when the surrounding context makes them unambiguous
- otherwise emit globally qualified targets
- use `~` only on globally qualified targets when shorter visible text is desirable
- use `:data:` for constants and enum-like values
- use `:obj:` only as a fallback when the safer standard role is still ambiguous

| Found variant | Meaning today | Proposed reST form | Example conversion |
| --- | --- | --- | --- |
| ``[`Name`][flet.]`` | Append label to module/package prefix | globally qualified target with `~` shortening | ``[`Page`][flet.]`` -> `:class:`~flet.Page`` |
| ``[`Name`][flet_map.]`` | Append label to package prefix | globally qualified target with `~` shortening | ``[`CircleLayer`][flet_map.]`` -> `:class:`~flet_map.CircleLayer`` |
| ``[`Member`][flet.Page.]`` | Append label to explicit prefix | globally qualified target with `~` shortening | ``[`route`][flet.Page.]`` -> `:attr:`~flet.Page.route`` |
| ``[`Page.route`][flet.Page.route]`` | Fully explicit attribute/property target | globally qualified target | ``[`Page.route`][flet.Page.route]`` -> `:attr:`flet.Page.route`` |
| ``[`upload()`][flet.FilePicker.upload]`` | Fully explicit method target | globally qualified target with `~` shortening | ``[`upload()`][flet.FilePicker.upload]`` -> `:meth:`~flet.FilePicker.upload`` |
| ``[`encrypt()`][(m).encrypt]`` | Module-local function/method | local `:func:` when module context is known | ``[`encrypt()`][(m).encrypt]`` -> `:func:`encrypt`` |
| ``[`ColorPicker`][(m).]`` | Current module symbol resolved to package export | globally qualified target with `~` shortening | ``[`ColorPicker`][(m).]`` -> `:class:`~flet_color_pickers.ColorPicker`` |
| ``[`Once`][(c)]`` | Current class name | current class name in standard Sphinx form | ``[`Once`][(c)]`` -> `:class:`Once`` |
| ``[`controls`][(c).]`` | Current class member, label appended | local member role | ``[`controls`][(c).]`` -> `:attr:`controls`` |
| ``[`show()`][(c).show]`` | Current class named member | local member role | ``[`show()`][(c).show]`` -> `:meth:`show`` |
| ``[`PieChartSection`][(p).]`` | Current package symbol resolved to package export | globally qualified target with `~` shortening | ``[`PieChartSection`][(p).]`` -> `:class:`~flet_charts.PieChartSection`` |
| ``[`selected`][(p).CandlestickChartSpot.selected]`` | Package-relative explicit member | globally qualified target with `~` shortening | ``[`selected`][(p).CandlestickChartSpot.selected]`` -> `:data:`~flet_charts.CandlestickChartSpot.selected`` |
| ``[`fill_color`][..]`` | Compact current-class member shorthand | same as `(c).` after normalization | ``[`fill_color`][..]`` -> `:attr:`fill_color`` |

### Role selection rules

Use these rules in the migration tool:

1. Use `:meth:` for callable class members and labels ending in `()`.
2. Use `:func:` for module-level callables.
3. Use `:class:` for classes and dataclasses.
4. Use `:mod:` only for true module references.
5. Use `:attr:` for properties, fields, and documented data attributes.
6. Use `:data:` for constants and enum-like values.
7. Use `:obj:` only when the safer standard role is still ambiguous.

### Display text rules

VS Code compatibility changes the default recommendation here.

Preferred canonical output:

- `:class:`~flet.BarometerReadingEvent``
- `:meth:`~flet.FilePicker.pick_files``
- `:attr:`start_angle``
- `:data:`~flet.ControlState.SELECTED``

Guidelines:

1. Prefer local member refs when current class/module context makes them obvious.
2. Otherwise use globally qualified names, not short ambiguous qualifiers.
3. Use `~` on globally qualified names when only the final display segment should be shown.
4. Keep globally qualified names without `~` when the visible text should stay fully qualified.
5. For custom prose labels such as `example`, rewrite the sentence instead of encoding
   that prose in the xref itself.

Examples:

- preferred in local context: `:attr:`start_angle``
- preferred cross-type reference: `:class:`~flet.Page``
- preferred qualified method reference: `:meth:`~flet.FilePicker.upload``
- acceptable when disambiguation is needed: `:class:`flet.Page``
- acceptable when full visible qualification is wanted: `:meth:`flet.FilePicker.upload``

---

## Proposed Implementation Split

### A. Runtime support patch

Files:

- `website/src/components/crocodocs/utils.js`
- optionally `website/plugins/remark-api-links.js`

Deliverable:

- mixed old/new xrefs render correctly in generated API docs

### B. Migration tool

Suggested location:

- `tools/crocodocs/src/crocodocs/` as a dedicated migration helper
- or a one-off script under `.codex/` if we want to keep it branch-local until stable

Recommended approach:

- parse Python files
- locate real docstring literals
- resolve current class/module/package context
- expand mkdocs shorthand targets to explicit Python targets
- select role by symbol kind using CrocoDocs/Griffe API data
- rewrite docstring content only

### C. Validation pass

Checks:

- no remaining ``[...][...]`` xrefs in `sdk/python/packages/*/src`
- generated API pages no longer render raw `:class:` or `:meth:` text
- mixed-format transition works while migration is incomplete

---

## Suggested Execution Order

1. Implement reST role parsing in `website/src/components/crocodocs/utils.js`.
2. Add fixture coverage for all role families.
3. Convert one pilot file:
   - `sdk/python/packages/flet/src/flet/controls/material/reorderable_list_view.py`
4. Verify rendered output in generated API docs.
5. Build the docstring-aware bulk migrator.
6. Convert `flet` package first.
7. Convert extension packages.
8. Remove mkdocs-style compatibility after the last package is migrated.

---

## Open Decisions

These should be fixed before the bulk conversion starts:

1. Public alias target preference

Should reST targets prefer public package aliases like `flet.Page` over canonical
module paths like `flet.controls.page.Page` when both exist?

Recommended answer:

- prefer the public import path when it exists in API data
- fall back to canonical qualname otherwise

2. Enum/member role strictness

Should enum members use `:attr:` or `:obj:`?

Recommended answer:

- use `:obj:` for enum values and constant-like members
- use `:attr:` for normal data attributes and properties

3. Scope of initial support

Should phase 1 support reST roles only in generated API docstrings, or also in
author-written Markdown/MDX docs?

Recommended answer:

- API docstrings first
- extend the remark plugin only if author-written docs begin to use reST roles
