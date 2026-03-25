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
- When a control folder has been fully converted to project-per-example layout, delete the control-level `examples/controls/<control>/__init__.py` too. The converted folders should behave like namespace packages, matching prior migrations such as commit `7e65ad566`.

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
- `[project].description` must be meaningful and example-specific; avoid generic placeholders like "Example N" or "<name> example for <control>".
- Description should mention the concrete behavior or interaction shown (for example: hover highlight, live updates, custom axes, event handling).
- Categories: typically control-based, e.g. `Input/Chip`, plus optional `Apps/Basic controls`.
- Tags: from control/topic/behavior words.
- Controls used: list key controls from code.
- Layout pattern: choose closest practical value (e.g. `filter-bar`, `inline-actions`, `dashboard`, `list-detail`).
- Complexity: `basic` unless logic/state/architecture is non-trivial.
- Features: notable behaviors only (click handling, selection, async loading, drag-and-drop, etc.).
- If an example supports exporting or downloading output, include `"save to file"` in `[tool.flet.metadata].features`.
- If an example module contains `async def` handlers or async control flow, append `"async"` to `keywords`.


5. Infer dependencies from imports.
- Always include `flet` for standard examples.
- Include extra packages if imported (for example extension packages).
- Do not add unused dependencies.

6. Make examples mobile-safe.
- If `ft.context.disable_auto_update()` is not used, do not add explicit `page.update()` unless strictly necessary.
- Apply this `page.update()` rule to all examples in the touched folder (new, migrated, and already converted).
- Wrap app content in `ft.SafeArea` so example renders correctly on mobile.
- Add `expand=True` to `ft.SafeArea` only when needed for correct layout/sizing (for example to avoid Infinity/NaN sizing issues), and avoid adding it when not necessary.
- When converting legacy `page.add(a, b, ...)` style examples, wrap the controls in `ft.Column(controls=[...])` inside `ft.SafeArea(content=...)` rather than `ft.Row`, unless the original code explicitly used a row layout.

- Apply this to all examples in the touched folder (new, migrated, and already converted), not only files changed by moves.
- During validation, confirm every `<example>/main.py` in scope includes a top-level `ft.SafeArea` around rendered content.
- For declarative examples using `@ft.component`, do not pass component instances as regular control children (for example `SafeArea(content=App())`) because this can raise runtime attribute errors.
- In declarative examples, ensure the component itself returns regular controls (including `SafeArea` when needed) and render it at page level with `page.render(App)` in `main()`.

7. Prefer `@ft.control` for custom controls in examples.
- If an example defines a custom control class inheriting from a Flet control (for example `class MyThing(ft.Column)`), prefer `@ft.control` style.
- Move constructor-style setup to declarative fields + `init()` where practical.
- Keep behavior unchanged and avoid refactors that alter public usage unless needed for compatibility.

8. Remove deprecated Material 3 toggle usage.
- If `use_material3` appears in example code, remove it and simplify the example to current API usage.
- Remove related Material 3 toggle logic/UI that exists only to switch `use_material3`.
- Update example metadata (`pyproject.toml`) to remove stale Material 3 references when code is changed.

9. Ensure runnable entrypoint.
- Every example `main.py` should end with:
  - `if __name__ == "__main__":`
  - `    ft.run(main)`
- Apply this to all examples in the touched folder (new, migrated, and already converted).

10. Update references.
- Docs code includes: change from `.../example.py` to `.../example/main.py`.
- Inspect the relevant docs pages for each touched control/service/example area (for example `sdk/python/packages/flet/docs/controls/<control>.md`) and update any `--8<--` includes or direct file-path references to the new `main.py` path.
- Tests/imports: use direct module imports and avoid relying on package-level `__init__.py` re-exports.
- For already-converted examples, only update references that are stale; avoid unnecessary churn.
- If removing a control-level `__init__.py`, confirm no remaining imports rely on `from examples.controls.<control> import ...`.

11. Validate.
- Run `python -m compileall` on changed `main.py` files.
- Run `uv run ruff check` on changed example files and fix violations until it passes (respecting repository `pyproject.toml` under `[tool.ruff]`).
- Search for stale paths to old flat files.
- Search docs and package sources for stale references to the migrated flat example paths and fix any hits in scope.
- Check `git status` to confirm expected moves and edits.
- When integration tests exist for the touched control, run the targeted test file(s).
- Confirm all in-scope `main.py` files include both top-level `ft.SafeArea` wrapping and the `if __name__ == "__main__": ft.run(main)` entrypoint.
- Confirm in-scope `ft.SafeArea` wrappers use `expand=True` only where needed for correct behavior and sizing; avoid forcing it by default.
- Confirm there are no unnecessary `page.update()` calls in in-scope examples (unless explicitly required by isolated-control or non-auto-update behavior).
- Confirm no in-scope examples use `use_material3`.
- Confirm each in-scope `pyproject.toml` has a meaningful, example-specific `[project].description` (not generic or templated text).
- Confirm metadata features include `"save to file"` when the example code supports file export/save behavior.
- Confirm there is no stale control-level `__init__.py` left behind once a touched control folder has been fully converted.
- Confirm the relevant docs pages were updated to reference `main.py` and that no stale doc includes remain for the touched examples.


## Code style

- When writing wrapped controls (`SafeArea`, `Column`, `Row`, `Container`, etc.), keep `content=` or `controls=` as the last named argument in that control call.
- Apply this ordering consistently when creating or refactoring examples.
- Follow code style and linting rules defined in the repository `pyproject.toml` under `[tool.ruff]` for all edits.

## Command checklist

- Discover files: `rg --files <target_dir>`
- Find docs links/imports: `rg -n "<old_path_or_module>" packages examples`
- Syntax check: `python -m compileall <changed_main_files>`
- Ruff check: `uv run ruff check <changed_example_files>`

## Output expectations

Report:
- created example projects
- metadata added
- docs/tests updates
- validation results
