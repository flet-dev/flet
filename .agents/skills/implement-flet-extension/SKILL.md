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

- Use `parseEnum()` for enums.
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

- Add dependency and registration to Flet client app.
- Add extension package to `sdk/python/pyproject.toml`.
- Add extension to `sdk/python/packages/flet/pyproject.toml`.
- Add extension to `sdk/python/examples/apps/flet_build_test/pyproject.toml`.
- Add extension to `.github/workflows/ci.yml` in both places:
  - `build_flet_extensions` -> `PACKAGES` list.
  - `py_publish` -> `for pkg in ...` publish loop.
- Add `.gitignore` to Flutter extension project if missing.

## Docs, Examples, Tests

- Add control/service docs under `website/docs/controls/<name>` for controls and `website/docs/services/<name>` for services.
- Add all custom enums/types docs and update `website/sidebars.yml` navigation.
- Use markdown filenames without underscores (`codeeditor.md`, not `code_editor.md`).
- Add examples under `sdk/python/examples` in the appropriate category for control vs service.
- Add integration tests under `packages/flet/integration_tests` in the appropriate category for control vs service.
- Ensure generated screenshots are suitable for docs usage when visual examples are added.

## Upgrade and Compatibility Guardrails

- Add at least one test that catches upstream behavioral changes likely to break wrapper mapping.
- Avoid exposing experimental upstream APIs unless explicitly requested.
- Keep wrapper surface narrow enough to maintain backwards compatibility across upstream updates.

## Validation

- Run relevant Python and integration tests for touched areas.
- Verify Python import paths, client runtime registration, and docs navigation.
- Verify dependency resolution and lockfile updates are intentional.
