---
name: implement-flet-extension
description: Implement a new Flet extension/control that wraps a third-party Flutter package end-to-end, including dependency selection, version pinning, compatibility checks, Python/Flutter integration, docs, examples, tests, and CI updates. Use when adding any flet_* package backed by an external pub.dev package.
---

Implement a Flet extension around an external Flutter package using existing `flet_*` packages as implementation templates.

## Inputs

- Control/service name and Python package name (`flet_<extension>`).
- Target pub.dev package and intended version/range.
- API surface to expose in Python (properties, methods, events, types/enums).

## Third-party Dependency Gate

1. Confirm package health: maintenance activity, null-safety, platform support, and open issue risk.
2. Confirm license is compatible with Flet distribution.
3. Select a conservative version strategy:
- Pin exact version when behavior stability is critical.
- Use bounded ranges when required by ecosystem constraints.
4. Record key constraints and reasons in PR notes/commit message.

## Control/Service Classification

- Classify wrapped functionality before implementation:
1. `LayoutControl` for visual controls that participate in page/layout positioning.
2. Base `Control` for simple visual controls that do not require page positioning or define their own positioning rules/props (for example `Draggable`, `Divider`, `MenuBar`, `NavigationRail`).
3. Non-visual Service when functionality is not a renderable UI control.
- Inspect the wrapped Flutter package API to determine whether it includes non-visual/service functionality.
- For service patterns, follow existing extension examples: `sdk/python/packages/flet-audio`, `sdk/python/packages/flet-flashlight`, `sdk/python/packages/flet-secure-storage`.

## API Mapping Rules

- Expose only stable and useful features first; avoid mirroring every upstream option.
- Keep Python API idiomatic and concise; avoid redundant control-name prefixes.
- Map upstream naming inconsistencies to Flet conventions when needed.
- Add custom enums/types only when they improve correctness and discoverability.

## Python-side Rules

- Use `LayoutControl`, base `Control`, or Service base class according to classification.
- Implement typed properties, methods, and events exactly for chosen public API.
- Reuse existing serialization/event patterns from sibling controls/services.

## Flutter-side Rules

- Use `parseEnum()` for enums — it's exported from `package:flet/flet.dart`. Call it as `parseEnum(MyEnum.values, widget.control.getString("attr"), MyEnum.defaultVal)!`. Do NOT write a custom `_parseXxx()` switch helper.
- For control attributes, prefer `widget.control.getBool()/getDouble()/...` accessors.
- For non-control parsing, use shared `parseSomething()` helpers.
- Do not add one-off private parser utilities when standard helpers exist.
- Put control-specific helpers in `utils/<control>.dart`; shared helpers in `utils/<topic>.dart`.
- Prefer `parse`-prefixed helper names when converting input to Flutter structures.
- Avoid single-use local variables.

### Default Value Matching (Critical)

Properties with default values on the Python side are **not sent to Flutter** when unchanged from the default. Every Dart property read **must provide the same default** as its Python counterpart:

- `control.getDouble("size", 100.0)!` when Python has `size: float = 100.0`
- `control.getBool("animate", true)!` when Python has `animate: bool = True`
- `parseDuration(value["dur"], const Duration(milliseconds: 500))!` when Python has `dur: DurationValue = field(default_factory=lambda: Duration(milliseconds=500))`
- `control.get<List>("items")?.map(...).toList() ?? const []` when Python has `items: list[str] = field(default_factory=list)`

Without matching defaults, Dart receives `null` and either crashes or silently uses the wrong value. This applies to all property types: bools, numbers, strings, enums, durations, collections, and nested `@ft.value` types.

## Integration Checklist

- Register in the Flet client app — two files:
  1. `client/pubspec.yaml`: add `flet_<ext>: path: ../sdk/python/packages/flet-<ext>/src/flutter/flet_<ext>` under `dependencies`.
  2. `client/lib/main.dart`: add `import 'package:flet_<ext>/flet_<ext>.dart' as flet_<ext>;` and `flet_<ext>.Extension()` to the `extensions` list.
- Add extension package to `sdk/python/pyproject.toml` in **two places**: the `dependencies` list and `[tool.uv.sources]` as `{ workspace = true }`.
- Add extension to `sdk/python/packages/flet/pyproject.toml` in the `[dependency-groups] extensions` list.
- Add extension to `sdk/python/examples/apps/flet_build_test/pyproject.toml` in **three places**: `[project] dependencies`, `[tool.uv.sources]` as `{ path = "...", editable = true }`, and `[tool.flet.dev_packages]` as a relative path string.
- Add extension to `tools/crocodocs/pyproject.toml` under `[tool.crocodocs.packages]` as `<pkg_name> = "../../sdk/python/packages/<pkg-dir>/src"`. This fixes "Missing API entry" errors in the docs. Note: `api-data.json` is gitignored (generated at build time); only the `pyproject.toml` change needs committing.
- Add extension to `.github/workflows/ci.yml` in both places:
  - `build_flet_extensions` -> `PACKAGES` list.
  - `py_publish` -> `for pkg in ...` publish loop.
- Add `.gitignore` to Flutter extension project if missing.
- Remove `[tool.uv.sources]` local path overrides from example `pyproject.toml` files before opening a PR (they are development-only conveniences).

## Docs, Examples, Tests

- Add control/service docs under `website/docs/controls/<name>` for controls and `website/docs/services/<name>` for services.
- Always create one doc page per control, even for extensions with many similar controls. Use `index.md` for the overview (install instructions, examples, list of links) and individual `<controlname>.md` files for each control — consistent with `flet-color-pickers` and other extensions.
- Use `<ClassSummary name="pkg.ClassName" />` and `<ClassMembers name="pkg.ClassName" />` JSX from `@site/src/components/crocodocs` to render API docs. Do NOT add `image=`, `imageCaption=`, or `imageWidth=` props to `<ClassSummary>` when no screenshots exist yet.
- In the `## Examples` section, do NOT add `###` subtitles above `<CodeExample>` blocks — titles are injected automatically from the example file itself.
- Add all custom enums/types docs and update `website/sidebars.yml` navigation.
- Use markdown filenames without underscores (`codeeditor.md`, not `code_editor.md`).
- Add examples under `sdk/python/examples/extensions/<name>/` for extension controls.
- Use `import flet_<ext> as <short_alias>` in examples (e.g., `import flet_spinkit as spins`). Keep alias short but readable.
- Use `ft.Colors.SURFACE_CONTAINER_HIGHEST` for card/cell backgrounds in showcase examples — it adapts to light and dark system themes automatically.
- Do NOT set an explicit dark theme in examples; let the app use system theme (no `page.theme_mode`).
- Add integration tests under `packages/flet/integration_tests/extensions/<name>/` — **not** inside the extension package's own directory (no `tests/` folder in the package itself, matching the pattern of `flet-code-editor`, `flet-color-pickers`, etc.).
- For controls with continuously-running animations, do NOT use `assert_control_screenshot` or `pump_and_settle` — they will timeout waiting for animations to settle. Instead use `await flet_app.tester.pump(duration=ft.Duration(milliseconds=500))` which advances the clock by a fixed amount. This still runs real Flutter rendering and catches crashes, without screenshot comparison.
- Ensure generated screenshots are suitable for docs usage when visual examples are added.

## Upgrade and Compatibility Guardrails

- Add at least one test that catches upstream behavioral changes likely to break wrapper mapping.
- Avoid exposing experimental upstream APIs unless explicitly requested.
- Keep wrapper surface narrow enough to maintain backwards compatibility across upstream updates.

## Validation

- Run relevant Python and integration tests for touched areas.
- Verify Python import paths, client runtime registration, and docs navigation.
- Verify dependency resolution and lockfile updates are intentional.
