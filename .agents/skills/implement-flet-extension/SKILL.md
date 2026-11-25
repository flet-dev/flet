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
3. Confirm that the parts of the package the extension uses don't build widgets from the Flutter SDK's `package:flutter/material.dart` or `package:flutter/cupertino.dart`, or take or return their types. Parts it doesn't use don't matter: `shadcn_ui`'s `ShadApp` is built on the SDK `MaterialApp`, but flet-shadcn-ui never uses it. Flet renders with the `material_ui` and `cupertino_ui` packages, so SDK `TextField`, `InkWell`, `ListTile` and similar widgets fail at runtime ("No Material widget found"), and SDK `ThemeData`/`ButtonStyle` values don't type-check against Flet's helpers. Prefer a release built on `material_ui`/`cupertino_ui` or on `widgets.dart` only.
4. Select a conservative version strategy:
- Pin exact version when behavior stability is critical.
- Use bounded ranges when required by ecosystem constraints.
5. Record key constraints and reasons in PR notes/commit message.
6. Read the package source from its pub.dev archive (`https://pub.dev/api/archives/<pkg>-<version>.tar.gz`). Extract it into the scratchpad, or stream single files with `tar -xzO <path>`. Never run `tar -xz`/`-xzv` without `-O` from inside the repo: it unpacks the whole package into the current directory.
7. Check which ancestors the widgets need. Design-system packages usually expect their app widget (`ShadApp`, `FluentApp`) to provide a theme and localizations, and throw or assert without them (`FluentTheme.of` uses `!`; many fluent_ui widgets call `debugCheckHasFluentLocalizations`). Plan a per-control fallback, plus `FletExtension.wrapApp` if the package opens routes itself (see "Required ancestors" below).
8. If the package needs a newer version of a dependency Flet already locks (for example `material_ui`), move `client/pubspec.lock` to the **lowest** compatible version with `fvm flutter pub downgrade <dep>`. `pub get` jumps to the newest release, which changes Flet's own dependency more than needed.

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
- A field whose `None` means something must default to `None`. On first render the protocol omits every `None` field, so `None` can't override a non-`None` default: `max_lines: Optional[int] = 1` set to `None` reaches Dart as "not sent", which reads as `1`. Either default to `None` and give `None` the "off" meaning (fluent `Checkbox.value`: `None` is unchecked, or indeterminate with `tristate`), or add a separate flag (`TextBox.multiline: bool = False` with `max_lines: Optional[int] = None`, like core `TextField`). Later diffs do send `null`, so the bug only shows on the first render.

## Flutter-side Rules

- Import `package:material_ui/material_ui.dart` (and `package:cupertino_ui/cupertino_ui.dart` for Cupertino), never `package:flutter/material.dart` or `package:flutter/cupertino.dart`. Files that use no Material or Cupertino API import `package:flutter/widgets.dart`. Add `material_ui` (and `cupertino_ui` if used) to the extension's `pubspec.yaml` with the same constraints as `packages/flet/pubspec.yaml`.
- Use `parseEnum()` for enums — it's exported from `package:flet/flet.dart`. Call it as `parseEnum(MyEnum.values, widget.control.getString("attr"), MyEnum.defaultVal)!`. Do NOT write a custom `_parseXxx()` switch helper.
- For control attributes, prefer `widget.control.getBool()/getDouble()/...` accessors.
- For non-control parsing, use shared `parseSomething()` helpers.
- Do not add one-off private parser utilities when standard helpers exist.
- Put control-specific helpers in `utils/<control>.dart`; shared helpers in `utils/<topic>.dart`.
- Prefer `parse`-prefixed helper names when converting input to Flutter structures.
- Avoid single-use local variables.
- When wrapping a widget in conditional decoration (a label or error text that appears and disappears), keep the widget tree the same shape (always wrap, key the children). Otherwise toggling the decoration rebuilds the inner widget and drops its state, for example focus while typing. Don't decorate by putting the widget in a `Column`: it loosens a fixed `width`, which shrinks button-like widgets.

### Required ancestors (theme, localizations)

When the wrapped widgets need ancestors that a `*App` widget would normally provide, give each control a fallback wrapper, like `withShadTheme` in flet-shadcn-ui or `withFluentTheme` in flet-fluent-ui (`lib/src/utils/theme.dart`):

- Wrap only when the ancestor is missing (`XTheme.maybeOf(context) == null`), deriving brightness from the Material `Theme.of(context)` so the control follows the page's light/dark mode. Cache fallback theme data per brightness if building it is expensive.
- Missing localizations: add `Localizations.override(context: context, delegates: [...])` with a delegate that falls back to English for unsupported locales. Check that the package's delegate loads with a `SynchronousFuture`, or the first frame renders without it.
- Widgets that push a **route** (dialogs, sheets, picker popups, flyouts) build outside the control's tree, on the app's navigator. Widgets that use `OverlayPortal` (most popups, menus, tooltips) inherit the control's context and need nothing extra. Grep the package for `Navigator.of`/`showDialog`/`push(` versus `OverlayPortal` to tell which is which.
  - If the extension calls `showDialog` itself, wrap the route builder's content again.
  - If the package pushes the route internally (fluent_ui's `DatePicker`, `TimePicker`, `CalendarDatePicker`), override `FletExtension.wrapApp` to provide the theme and localizations above the navigator (`wrapAppWithFluentTheme` in flet-fluent-ui). It wraps every Flet app that includes the extension, so it must not change other controls: the design system's theme widget may also set an `IconTheme` (and a `DefaultTextStyle`) for its descendants; restore the app's `IconTheme` below it. Keep the per-control fallback too, and have it still wrap when the theme it finds is the app-level one, so controls follow a nested Material brightness and get the design system's text style.
  - Popups opened this way use the app-level theme, not the theme of the control's `Theme` ancestor; say so in the docs if it matters.
- Code that reads the theme (a custom `ButtonStyle`, for example) must take its `BuildContext` from **below** the wrapper. Put a `Builder` inside the wrapped child; the control's own `context` is above the fallback theme, and `XTheme.of(context)` throws there.
- Upstream widgets that take an `initial*` value (fluent_ui's `CalendarView`) or apply a new value after the frame without rebuilding (fluent_ui's `TimePicker`) don't follow values set from Python. Give the widget a key that changes when Python sets a value; when the widget reports a change, remember what it reported and don't change the key for that, or the widget loses state it keeps itself (a multiple selection). Pass the `initial*` values the widget was created with, not the latest reported ones: fluent_ui treats a changed `initialStart` as a new selection.
- A list property that Dart updates with `updateProperties` can break the next Python patch of that list. Send lists the user produced (selected dates) in the change event instead, as a typed `ft.Event` subclass.
- Look at disabled and other non-default states in the generated images. Upstream styles sometimes leave them indistinguishable (fluent_ui's disabled `OutlinedButton` and `HyperlinkButton`); patch only that state with a style that keeps upstream's values for the others, and say why in a comment.

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
- Add the extension's PyPI name to `FLET_PACKAGES` in `sdk/python/packages/flet-cli/src/flet_cli/utils/project_dependencies.py`, so `flet build`, `flet debug` and `flet publish` pin it to the Flet CLI version. A test fails if a folder in `sdk/python/packages` is missing from it.
- Add `.gitignore` to Flutter extension project if missing.
- Remove `[tool.uv.sources]` local path overrides from example `pyproject.toml` files before opening a PR (they are development-only conveniences).

## Docs, Examples, Tests

- Add control/service docs under `website/docs/controls/<name>` for controls and `website/docs/services/<name>` for services.
- Always create one doc page per control, even for extensions with many similar controls. Use `index.md` for the overview (install instructions, examples, list of links) and individual `<controlname>.md` files for each control — consistent with `flet-color-pickers` and other extensions.
- Use `<ClassSummary name="pkg.ClassName" />` and `<ClassMembers name="pkg.ClassName" />` JSX from `@site/src/components/crocodocs` to render API docs.
- Give sub-controls their own page too. A **sub-control** is a control that can only be used inside a specific parent control (e.g. `TableColumn`/`TableRow`/`TableCell` in `Table`, `MenuItem` in `ContextMenu`/`Menubar`, `Radio` in `RadioGroup`, `Tab` in `Tabs`, `AccordionItem` in `Accordion`), not any control placed in another's `controls`/`content`. Never render a second class's `<ClassSummary>`/`<ClassMembers>` on the parent's page: each page must document exactly one class, otherwise it gets two "Properties"/"Events" headings with the same anchor and the table of contents breaks.
  - Sub-control page: front matter `class_name` and `title`, then `<ClassSummary name={frontMatter.class_name} />` and `<ClassMembers name={frontMatter.class_name} />` (no example/images needed); file name is the lowercased class name (`tablecolumn.md`).
  - Nest sub-control pages under their parent in `website/sidebars.yml` (`Table: {_index: .../table.md, TableColumn: .../tablecolumn.md, ...}`), like core `DataTable → DataCell`. A sub-control shared by several parents (e.g. `MenuItem` for `ContextMenu` and `Menubar`) is listed once, under one parent.
  - Make sure each parent page links to its sub-controls: reference them with `:class:` roles in the parent's docstrings (class description or the property that holds them, e.g. `items`), which render as links to the sub-control page.
- Include screenshots in the docs for every visual control (see "Example Tests and Docs Images" below). Only omit `image=`/`imageCaption=`/`imageWidth=` on `<ClassSummary>` for non-visual services or controls that cannot be screenshotted (continuously animating ones).
- In the `## Examples` section, do NOT add `###` subtitles above `<CodeExample>` blocks — titles are injected automatically from the example file itself.
- Add all custom enums/types docs and update `website/sidebars.yml` navigation. List new extension controls under `Reference → Controls → Extensions` (alphabetically). Only an extension that brings its own design system gets its own folder next to Core/Material/Cupertino/Extensions, like `Shadcn` and `Fluent`. See the "Sidebar Navigation" section of `.agents/skills/docs-conventions/SKILL.md`.
- Use markdown filenames without underscores (`codeeditor.md`, not `code_editor.md`).
- Add examples under `sdk/python/examples/extensions/<name>/` for extension controls, **one example per control page**, including sibling controls that share one Python base class or Dart widget (FilledButton, OutlinedButton, HyperlinkButton and IconButton each get their own example, not one shared "buttons" example). Each example uses the control in a realistic situation, not a list of every variant.
- Make sure every code sample, in docstrings too, uses the current Flet API and runs (for example, URLs open through `await ft.UrlLauncher().launch_url(url)`; there is no `page.launch_url`).
- In an event handler that calls `page.pop_dialog()`, call `.update()` on any other control you change: `pop_dialog()` sends its own update, so the page is not auto-updated after that handler.
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
   - `test_image_for_docs` (uses `flet_app_function`): set `page.theme_mode = ft.ThemeMode.LIGHT` and call `assert_control_screenshot(request.node.name, bgcolor=ft.Colors.SURFACE, control=...)`. **The image must render exactly the code in the class docstring's `Example:`**, because `<ClassSummary>` shows that code right above the image. Copy the docstring's controls with the same labels and values, leaving out only event handlers. Add layout wrappers only: `ft.Row(tight=True)` or `ft.Column(intrinsic_width=True)` so the image is not stretched to the page width, or a fixed-width `ft.Column` (with `horizontal_alignment=STRETCH` for bars) for controls that need a width. To show more states (disabled, checked, indeterminate), add them to the docstring example first. Keep docstring examples screenshot-able: no indeterminate or otherwise endlessly animating controls.
   - One test per example, parametrized with `{"flet_app_main": example.main}` and `indirect=True`:
     - set `page.theme_mode = ft.ThemeMode.LIGHT` and `page.update()` (examples do not set a theme);
     - **interact like a user** (`tap`, `enter_text`, `mouse_hover`) and assert the example's visible result (`find_by_text(...).count == 1`);
     - screenshot only the page controls: `take_page_controls_screenshot(bgcolor=ft.Colors.SURFACE)` for a single image, or `scr = await wrap_page_controls_in_screenshot(bgcolor=ft.Colors.SURFACE)` + `scr.capture(pixel_ratio=...)` for several states;
     - for multi-step flows, save each state (`<example>_initial`, `<example>`, ...) and combine them with `create_gif([...], "<example>_flow", duration=1000)`.
   - `enter_text` needs a finder on the input itself, so give example inputs (and other controls the test must target) a `key=` and use `find_by_key`.
3. Generate goldens from `sdk/python`: `FLET_TEST_GOLDEN=1 uv run pytest -s packages/flet/integration_tests/examples/extensions/<name>`. **Open and review every PNG and GIF** (dark or transparent background, stretched rows, cramped spacing, oversized icons, clipping), fix the test or example, regenerate, then re-run without `FLET_TEST_GOLDEN` to confirm the comparisons pass. Commit the `golden/macos/<control>/*` files.
4. Reference the images in each control page:
   - front matter: `example_images: "test-images/examples/extensions/<name>/golden/macos/<control>"` (crocodocs' `test-images` mapping already serves `integration_tests`);
   - `<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="<ClassName>" imageWidth="30%"/>`, with the width derived from the image so controls appear at the same scale on every page (with 2x screenshots, about one percent per 16 image pixels);
   - under each `<CodeExample>`: `<Image src={frontMatter.example_images + '/<example>.png'} alt="<example>" width="45%" caption="<what the user did>" />`, pointing to the `_flow.gif` for flows; import `Image` from `@site/src/components/crocodocs`. Derive `width` from the image's pixel width with the same scale as the `<ClassSummary>` image (about one percent per 16 pixels), never a fixed percentage: a small GIF at a fixed 40% is shown 2-3 times its size and gets cut off on the page.
5. Run `uv --directory ./tools/crocodocs run crocodocs generate` from the repo root and check that the images appear under `website/static/docs/test-images/...` (generated, not committed).

## Upgrade and Compatibility Guardrails

- Add at least one test that catches upstream behavioral changes likely to break wrapper mapping.
- Avoid exposing experimental upstream APIs unless explicitly requested.
- Keep wrapper surface narrow enough to maintain backwards compatibility across upstream updates.

## Validation

- Run relevant Python and integration tests for touched areas.
- Verify Python import paths, client runtime registration, and docs navigation.
- Verify dependency resolution and lockfile updates are intentional.
- Run ruff from `sdk/python` on paths inside it only, with `--no-fix` to check. The config sets `fix = true`, and mixing in a path outside the project (for example `.github/scripts/...`) resolves different settings and rewrites `Optional[X]` to `X | None` across the files.
- On macOS, build the test app once (`fvm flutter build macos --debug -t integration_test/app_test.dart` in `client`, then set `FLET_TEST_APP_BINARY`) and rebuild after every Dart change. A test that fails with "Timed out during start: tester.pump_and_settle()" is usually the intermittent app-start hang; rerun that file before debugging it.

### Temporary CI narrowing on the feature branch

- While developing an extension, the maintainer may narrow `.github/workflows/macos-integration-tests.yml` on purpose so CI runs only the new extension's tests: the `include:` list of the matrix is cut to one group whose `dirs` lists only the extension's directories (for example `examples/extensions/<name>` and `extensions/<name>`).
- This is intentional. Do NOT revert, "fix", or restore that matrix while working on the branch, and keep it when committing unless told otherwise.
- Before the branch is merged (when the user says the work is done), restore the original matrix with its three groups. The `apps-extensions` group already includes the new tests through `examples/extensions` and `extensions`.
