---
name: create-flet-example-projects
description: Use when asked to create Flet example projects from flat .py files with main.py and pyproject.toml metadata for Gallery/MCP indexing.
---

## When to use

Use this skill when a user asks to:
- create one control/example folder (for example `examples/controls/chip`) in the project-per-example format
- migrate existing flat examples to the project-per-example format
- normalize a partially converted folder so all examples follow the same structure

## Goal

Ensure each runnable example is a standalone project containing:

- `main.py`
- `pyproject.toml` with Gallery/MCP metadata
- `assets/` (if the example uses local assets)

## Workflow

1. Inspect source folder.
- Detect current state per example:
  - flat file: `foo.py`
  - project folder: `foo/main.py`
  - mixed/partial conversion: both styles present or missing metadata files
- Find candidate flat modules: `*.py` in the target folder (exclude helper files such as `__init__.py`).
- Keep existing `media/` unless an example needs local assets copied into its own `assets/`.

2. Convert or normalize examples.
- For `foo.py`, create `foo/` and move file to `foo/main.py`.
- If `foo/main.py` already exists, keep it and do not recreate/move files.
- If folder exists but `main.py` is missing, repair structure only when there is a clear source file.
- Do not create `foo/__init__.py`; import example modules directly in tests/docs (for example `import examples.controls.foo.bar.main as bar` or `import examples.controls.foo.bar as bar` when using namespace-package imports).

3. Add `pyproject.toml` for each example project.
- Infer from path and code.
- Create missing `pyproject.toml` files for existing project folders.
- Update obviously stale metadata when migrating existing examples (for example wrong title/description/categories).
- Required fields:
  - `[project]`: `name`, `version`, `description`, `requires-python`, `keywords`, `authors`, `dependencies`
  - `[dependency-groups].dev`: include `flet-cli`, `flet-desktop`, `flet-web`
  - `[tool.flet.gallery].categories`
  - `[tool.flet.metadata]`: `title`, `controls`, `layout_pattern`, `complexity`, `features`
  - `[tool.flet]`: `org`, `company`, `copyright`
- Add `[tool.flet].platforms` only when the example is platform-limited.
- Add permissions blocks only when code actually needs them.

4. Infer metadata.
- Title: readable version of file/folder intent.
- Short description: one line of what the example demonstrates.
- Categories: typically control-based, e.g. `Input/Chip`, plus optional `Apps/Basic controls`.
- Tags: from control/topic/behavior words.
- Controls used: list key controls from code.
- Layout pattern: choose closest practical value (e.g. `filter-bar`, `inline-actions`, `dashboard`, `list-detail`).
- Complexity: `basic` unless logic/state/architecture is non-trivial.
- Features: notable behaviors only (click handling, selection, async loading, drag-and-drop, etc.).

5. Infer dependencies from imports.
- Always include `flet` for standard examples.
- Include extra packages if imported (for example extension packages).
- Do not add unused dependencies.

6. Make examples mobile-safe.
- If `ft.context.disable_auto_update()` is not used, do not add explicit `page.update()` unless strictly necessary.
- Wrap app content in `ft.SafeArea` so example renders correctly on mobile.

7. Update references.
- Docs code includes: change from `.../example.py` to `.../example/main.py`.
- Tests/imports: use direct module imports and avoid relying on package-level `__init__.py` re-exports.
- For already-converted examples, only update references that are stale; avoid unnecessary churn.

8. Validate.
- Run `python -m compileall` on changed `main.py` files.
- Search for stale paths to old flat files.
- Check `git status` to confirm expected moves and edits.
- When integration tests exist for the touched control, run the targeted test file(s).

## Command checklist

- Discover files: `rg --files <target_dir>`
- Find docs links/imports: `rg -n "<old_path_or_module>" packages examples`
- Syntax check: `python -m compileall <changed_main_files>`

## Output expectations

Report:
- created example projects
- metadata added
- docs/tests updates
- validation results
