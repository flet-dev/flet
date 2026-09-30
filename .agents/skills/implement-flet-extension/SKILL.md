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
- Use `<ClassSummary name="pkg.ClassName" />` and `<ClassMembers name="pkg.ClassName" />` JSX from `@site/src/components/crocodocs` to render API docs.
- Include screenshots in the docs for every visual control (see "Example Tests and Docs Images" below). Only omit `image=`/`imageCaption=`/`imageWidth=` on `<ClassSummary>` for non-visual services or controls that cannot be screenshotted (continuously animating ones).
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

## Example Tests and Docs Images

Every example gets an integration test, and the goldens it produces are the docs images. Follow `sdk/python/packages/flet/integration_tests/examples/controls/material/test_checkbox.py`.

**Every docs image must be light and opaque.** Screenshots are transparent by default: on the website's dark mode dark text becomes unreadable, and `create_gif` flattens transparency to **black**, so flow GIFs come out dark. For every screenshot used in docs:

- set `page.theme_mode = ft.ThemeMode.LIGHT` (and `page.update()` after launching an example);
- pass `bgcolor=ft.Colors.SURFACE` to `assert_control_screenshot`, `wrap_page_controls_in_screenshot` and `take_page_controls_screenshot`;
- after generating, confirm the images (including every frame of each GIF) have a light background, not black or transparent.

1. Create **one test file per control** in `sdk/python/packages/flet/integration_tests/examples/extensions/<name>/test_<control>.py`. The file stem picks the golden folder (`golden/macos/<control>/`), so each control's images stay together.
2. In each file:
   - `test_image_for_docs` (uses `flet_app_function`): set `page.theme_mode = ft.ThemeMode.LIGHT` and call `assert_control_screenshot(request.node.name, bgcolor=ft.Colors.SURFACE, control=...)` with a compact showcase of the control (a few states/variants). Wrap rows in `ft.Column(intrinsic_width=True, ...)` so the image is not stretched to the page width.
   - One test per example, parametrized with `{"flet_app_main": example.main}` and `indirect=True`:
     - set `page.theme_mode = ft.ThemeMode.LIGHT` and `page.update()` (examples do not set a theme);
     - **interact like a user** (`tap`, `enter_text`, `mouse_hover`) and assert the example's visible result (`find_by_text(...).count == 1`);
     - screenshot only the page controls: `take_page_controls_screenshot(bgcolor=ft.Colors.SURFACE)` for a single image, or `scr = await wrap_page_controls_in_screenshot(bgcolor=ft.Colors.SURFACE)` + `scr.capture(pixel_ratio=...)` for several states;
     - for multi-step flows, save each state (`<example>_initial`, `<example>`, ...) and combine them with `create_gif([...], "<example>_flow", duration=1000)`.
   - `enter_text` needs a finder on the input itself, so give example inputs (and other controls the test must target) a `key=` and use `find_by_key`.
3. Generate goldens from `sdk/python`: `FLET_TEST_GOLDEN=1 uv run pytest -s packages/flet/integration_tests/examples/extensions/<name>`. **Open and review every PNG and GIF** (dark or transparent background, stretched rows, cramped spacing, oversized icons, clipping), fix the test or example, regenerate, then re-run without `FLET_TEST_GOLDEN` to confirm the comparisons pass. Commit the `golden/macos/<control>/*` files.
4. Reference the images in each control page:
   - front matter: `example_images: "test-images/examples/extensions/<name>/golden/macos/<control>"` (crocodocs' `test-images` mapping already serves `integration_tests`);
   - `<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="<ClassName>" imageWidth="30%"/>`, with the width tuned to the image;
   - under each `<CodeExample>`: `<Image src={frontMatter.example_images + '/<example>.png'} alt="<example>" width="45%" caption="<what the user did>" />`, pointing to the `_flow.gif` for flows; import `Image` from `@site/src/components/crocodocs`.
5. Run `uv --directory ./tools/crocodocs run crocodocs generate` from the repo root and check that the images appear under `website/static/docs/test-images/...` (generated, not committed).

## Upgrade and Compatibility Guardrails

- Add at least one test that catches upstream behavioral changes likely to break wrapper mapping.
- Avoid exposing experimental upstream APIs unless explicitly requested.
- Keep wrapper surface narrow enough to maintain backwards compatibility across upstream updates.

## Validation

- Run relevant Python and integration tests for touched areas.
- Verify Python import paths, client runtime registration, and docs navigation.
- Verify dependency resolution and lockfile updates are intentional.

### Temporary CI narrowing on the feature branch

- While developing an extension, the maintainer may narrow `.github/workflows/macos-integration-tests.yml` on purpose so CI runs only the new extension's suites: every entry of the `suite:` matrix is commented out and only the extension's suites are added (for example `- examples/extensions/<name>` and `- extensions/<name>`).
- This is intentional. Do NOT revert, "fix", or restore that matrix while working on the branch, and keep it when committing unless told otherwise.
- Before the branch is merged (when the user says the work is done), restore the original matrix: uncomment every suite and remove the extension-specific entries. The regular `examples/extensions` and `extensions` suites already include the new tests.
