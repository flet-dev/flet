# Handoff: flet-fluent-ui (temporary — delete this folder before merging)

Branch `fluent-ui`. The `flet-fluent-ui` extension wraps the Flutter package
[fluent_ui](https://pub.dev/packages/fluent_ui), through flet-dev's fork
[flet-dev/fluent_ui](https://github.com/flet-dev/fluent_ui) (4.18.1 plus fixes, see section 1),
modelled on `flet-shadcn-ui`. Python classes have no prefix (`fluent.Button`); Dart control
types do (`@ft.control("FluentButton")`).

Every control is implemented. The icon font licensing blocker is fixed in the fork, but the
fork isn't pushed yet, so flet still builds against a local clone (section 1, "Still to do").

Files in this folder:
- `icon-license-issue-draft.md`: the GitHub issue for the fluent_ui maintainers, **posted** as
  https://github.com/bdlukaa/fluent_ui/issues/1383 (the original 4.17.0 version). The file
  now holds the 4.18.1 refresh; a follow-up comment with those updates, the full-set option
  and the fork link is posted too (#issuecomment-7180724666). Waiting for the maintainers.
- `subset_internal_icons.py`: superseded by `tool/build_mit_icon_fonts.py` in the fork.

## Where things are

- **Python:** `sdk/python/packages/flet-fluent-ui/src/flet_fluent_ui/`
- **Dart:** `sdk/python/packages/flet-fluent-ui/src/flutter/flet_fluent_ui/lib/src/`
  - `utils/theme.dart`: `withFluentTheme`, `wrapAppWithFluentTheme`
  - `utils/menu.dart`, `utils/field_layout.dart`, `extension.dart`
- **Examples:** `sdk/python/examples/extensions/fluent_ui/`
- **Tests:**
  - Example tests: `sdk/python/packages/flet/integration_tests/examples/extensions/fluent_ui/`
  - Behavior tests: `sdk/python/packages/flet/integration_tests/extensions/fluent_ui/test_fluent_ui.py`
- **Docs:** `website/docs/controls/fluentui/`; the sidebar is in `website/sidebars.yml`.
- **Icons:**
  - `.github/scripts/generate_icons.py`: fluent section, set ID 4.
  - Templates: `.github/scripts/templates/fluent_icons.{dart,pyi}`.
  - Generated files: `fluent_icons.{py,pyi,json}` and `utils/fluent_icons.dart`.
- **Core change:** the `FletExtension.wrapApp(context, child)` hook, used to give the app a
  fallback FluentTheme and FluentLocalizations.
- **Lessons learned:** `.agents/skills/implement-flet-extension/SKILL.md`.

### Running tests (macOS)

1. Build the test app, from `client`:
   ```
   fvm flutter build macos --debug -t integration_test/app_test.dart
   ```
2. Set `FLET_TEST_APP_BINARY` to the built app:
   ```
   export FLET_TEST_APP_BINARY=$PWD/build/macos/Build/Products/Debug/Flet.app/Contents/MacOS/Flet
   ```
3. Run from `sdk/python`:
   ```
   uv run pytest -s packages/flet/integration_tests/examples/extensions/fluent_ui packages/flet/integration_tests/extensions/fluent_ui
   ```

Two environment variables help:
- `FLET_TEST_GOLDEN=1` regenerates the goldens.
- `FLET_TEST_VERBOSE=1` shows the Flutter log.

If a run hangs, kill the orphaned Flet.app **by PID**, not by name pattern.

Long runs (about 11 minutes) sometimes fail a few tests with "Timed out during start:
tester.pump_and_settle() did not complete", in different tests each run; they pass when re-run.
The test window opens unfocused (often on a secondary display), and macOS throttles frames for
background or occluded windows and during display sleep. Run under
`caffeinate -d -i uv run pytest ...`, leave the machine alone while it runs, and re-run the
modules that timed out.

---

## 1. The fluent_ui fork

fluent_ui bundles two Microsoft icon fonts that may not be redistributed (Fabric MDL2 Assets
and Segoe Fluent Icons), and Flutter bundles a dependency's fonts into every app. The full
analysis is in `icon-license-issue-draft.md`.

### The fork: flet-dev/fluent_ui

Local clone: `../fluent_ui` (next to this repo), remote `upstream` = bdlukaa/fluent_ui.
`master` tracks upstream (4.18.1). One branch per fix, each meant as its own upstream PR:

| Branch | What | Upstream |
|---|---|---|
| `fix/mit-icon-fonts` | Rebuilds `fonts/FluentIcons.ttf` and `fonts/SegoeIcons.ttf` (4–7 KB each) from MIT Fluent UI System Icons glyphs, at the codepoints the widgets use, each scaled to the bounding box of the glyph it replaces. Script: `tool/build_mit_icon_fonts.py` (run with `uvx --with fonttools python tool/build_mit_icon_fonts.py`); MIT notice in `fonts/LICENSE`. No Dart changes. | A stopgap: the upstream PR waits for the maintainers' answer to the issue. |
| `fix/time-picker-minute-padding` | `_formatMinute` uses `DateFormat('mm', locale)`: "05", not "5". Test added. | [#1384](https://github.com/bdlukaa/fluent_ui/pull/1384) |
| `fix/flyout-inherit-theme` | `FlyoutController.showFlyout` re-applies the target's themes (`InheritedTheme.capture`), so DropDownButton, SplitButton and every other flyout follow a nested `FluentTheme`. Tests added. | [#1385](https://github.com/bdlukaa/fluent_ui/pull/1385) |
| `flet` | `master` + the three branches above. **flet pins this branch's commit SHA.** | — |

Each branch passes the fork's full `flutter test` (445+ tests). To refresh after an upstream
release or merge: rebuild `flet` from the new `master` plus the still-open fix branches, re-run
the font script if the widgets' icons changed, push, and bump the SHA in
`flet_fluent_ui/pubspec.yaml`.

Known limit, not fixed: with a short minute list (for example 15-minute steps) the looping
copies of the selected minute are drawn with the selected (white) text style. Different cause
from the padding; note it in the TimePicker PR.

### flet side

- `flet_fluent_ui/pubspec.yaml`: `fluent_ui` is a git dependency on the fork, pinned to the
  `flet` branch SHA. `material_ui` is `^1.7.0` (4.18.1 needs it).
- `fluent.FluentIcons` is now Microsoft's MIT Fluent UI System Icons: 5,722 members
  (`<NAME>` for the regular style, `<NAME>_FILLED` for filled), drawn from `flet_fluent_ui/fonts/FluentSystemIcons-Resizable.ttf`
  (1.6 MB, MIT notice in `fonts/LICENSE`). `generate_icons.py` downloads the font and its
  name -> codepoint JSON at one pinned commit (`FLUENT_COMMIT`, keep it equal to `FSI_COMMIT`
  in the fork's script) and writes the font, its LICENSE, and the generated lists.
- Web: `flet_fluent_ui` is in `DEFERRED_FONT_PACKAGES` (flet-cli `web_fonts.py`), and
  `createIconData` calls `loadDeferredFonts("flet_fluent_ui")`, so the 1.6 MB font downloads
  only when an icon is drawn. fluent_ui's own fonts are now tiny and load up front.
- TabView uses fluent_ui 4.18's `TabViewController` (`tab_view.dart`). 4.18 makes every tab
  draggable; without an `on_reorder` handler the wrapper moves the tab back. With one, it
  records the moved `selected_index` without rebuilding, then sends `reorder`.
- `_withThemeOf` is gone from `flyout.dart`: the fork's flyout fix covers it.
- All examples, docs and tests use the new icon names. Renamed: CONTACT -> PERSON,
  FAVORITE_STAR(_FILL) -> STAR/STAR_FILLED, FOLDER_HORIZONTAL -> FOLDER, INBOX ->
  MAIL_INBOX, MAIL_FORWARD/REPLY -> ARROW_FORWARD/REPLY, OPEN_IN_NEW_WINDOW -> WINDOW_NEW,
  READ -> MAIL_READ, RINGER -> ALERT, SORT -> ARROW_SORT. The other 18 icons the examples
  use kept their names (HOME, SETTINGS, SAVE...).

### Still to do

1. ~~Push the fork branches~~ Done: all four are on flet-dev/fluent_ui.
2. ~~Remove the temporary override~~ Done: `client/pubspec.lock` resolves `fluent_ui` from
   git at `e6221b92`.
3. ~~Integration tests and goldens~~ Done against the local fork: all 118 Fluent tests pass.
   74 goldens were refreshed and reviewed (new MIT icons; 4.18's flyout padding and acrylic,
   CommandBar overflow sizing, compact NavigationView spacing). Re-run against the git
   dependency: everything passes (8 start timeouts in the full run passed when re-run).
4. Check a built app: `flet build macos` and `flet build web` on an example; the bundled
   `fluent_ui/fonts/*.ttf` must be the small MIT fonts, and the web build must list
   `packages/flet_fluent_ui/FluentIcons` in `DeferredFontManifest.json`.
5. ~~Follow-up comment on #1383~~ Posted. ~~Upstream PRs~~ Opened:
   https://github.com/bdlukaa/fluent_ui/pull/1384 (TimePicker) and
   https://github.com/bdlukaa/fluent_ui/pull/1385 (flyout theme). When they merge and release,
   drop those branches from `flet` (or move to the release) and bump the pin.

---

## 2. Other outstanding issues

1. **EditableComboBox shows no red underline when `error_text` is set.** The error text itself
   is shown; fluent_ui's EditableComboBox doesn't expose the highlight color. Now documented in
   the `error_text` docstring in `combo_box.py`.
2. **Possible flake:** `test_radio_group` errored once, then passed on rerun.
3. **Before merging:**
   - Delete this `HANDOFF-fluent-ui/` folder.
   - Check that CI workflow changes are limited to the `flet-fluent-ui` additions in `ci.yml`
     (`git diff main...HEAD -- .github`). The `macos-integration-tests.yml` workflow is not
     narrowed on this branch.
