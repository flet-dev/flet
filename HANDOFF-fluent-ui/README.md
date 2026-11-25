# Handoff: flet-fluent-ui (temporary — delete this folder before merging)

Branch `fluent-ui`. The `flet-fluent-ui` extension wraps the Flutter package
[fluent_ui](https://pub.dev/packages/fluent_ui) 4.17.0 (exact pin), modelled on
`flet-shadcn-ui`. Python classes have no prefix (`fluent.Button`); Dart control
types do (`@ft.control("FluentButton")`).

Every control is implemented, and the full Fluent integration suite passes (118 tests).
The blocker before merging is **icon font licensing** (section 1).

Files in this folder:
- `icon-license-issue-draft.md`: a draft GitHub issue for the fluent_ui maintainers
  (bdlukaa/fluent_ui). **Not posted.** Post only with the user's approval.
- `subset_internal_icons.py`: a fonttools script that cuts the MIT Fluent UI System Icons
  Resizable font down to the glyphs fluent_ui uses internally.

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

---

## 1. Icon font licensing (blocker)

### The problem

fluent_ui declares two Microsoft icon fonts in its `pubspec.yaml`. Flutter bundles fonts
declared by a dependency into every app, and there is no way to exclude them. So every Flet
app that uses flet-fluent-ui ships both fonts on every platform.

| Family | File | What it is | Glyphs | Size | License |
|---|---|---|---|---|---|
| `FluentIcons` | `fonts/FluentIcons.ttf` | Fabric MDL2 Assets 4.46 | 2,214 | 500 KB | Microsoft Fabric Assets License: use limited to developing for Microsoft products |
| `SegoeIcons` | `fonts/SegoeIcons.ttf` | Segoe Fluent Icons 1.34 | 1,374 | 452 KB | Windows font. Microsoft's page says: "you may not ship it to another platform" |

fluent_ui's BSD-3 license covers its code, but not these fonts. fluent_ui bundles no text
font, so text is not affected.

The fonts are used in two ways:
- **Internally:** the widgets use 12 `FluentIcons` glyphs and 27 `WindowsIcons` glyphs
  (WindowsIcons maps to the SegoeIcons font). InfoBar also uses two Material icons, which are
  Apache 2.0 and fine. The full list and a mapping table are in `icon-license-issue-draft.md`.
- **In flet-fluent-ui's Python API:** `fluent.FluentIcons` exposes all 2,214 MDL2 glyphs. It is
  used in about 23 files across examples, docs and tests.

### The MIT alternative

Microsoft's [Fluent UI System Icons](https://github.com/microsoft/fluentui-system-icons) are
MIT-licensed, and are on pub.dev as `fluentui_system_icons`. Every internally used glyph has an
equivalent, for example:
- `chrome_close` → `dismiss`
- `global_nav_button` → `navigation`
- `caret_*_solid8` → `caret_*` (filled)

Sizes:

| Option | Size |
|---|---|
| `fluentui_system_icons` package as a dependency | about 4.6 MB (it bundles Regular and Filled fonts at 10–48 px) |
| `FluentSystemIcons-Resizable.ttf` from the repo (all icons, regular and filled, scalable) | 1.34 MB |
| Resizable font cut down to the internal glyphs | about 10 KB (made by `subset_internal_icons.py`) |

### Why a runtime override isn't enough

We could register a font at runtime under fluent_ui's family names with `FontLoader`. That only
changes how the icons look: the original `.ttf` files are still bundled, because they are
declared in fluent_ui's pubspec, and bundling them is the licensing problem.

### Suggested solution

1. **File the upstream issue first.** The draft is in this folder.
   - It proposes switching the widgets to a small MIT font and deprecating or moving the
     MDL2/Segoe classes.
   - It offers a PR from us.
   - Wait for the user's go-ahead before posting.
2. **Meanwhile, or if upstream declines, fork fluent_ui 4.17.0 and change only its fonts:**
   - Replace `fonts/FluentIcons.ttf` and `fonts/SegoeIcons.ttf` with MIT-glyph fonts.
   - Keep the **same family names and the same codepoints** for the internally used glyphs.
     For example, the MIT `chevron_down` goes at MDL2 `chevron_down`'s codepoint. With fonttools
     this is a cmap remap on a subset of the Resizable font: each font is about 10 KB.
   - Add the MIT notice. No Dart code changes, so rebasing means copying a new release and
     re-running the script.
   - Point `flet_fluent_ui/pubspec.yaml` at the fork. Either:
     - a git dependency, for example `flet-dev/fluent_ui`, pinned to a commit; or
     - a vendored path.

     Either works because Flet extensions are path-dependent and never published to pub.dev.
   - The same fork could also fix the TimePicker minute padding (section 2).
3. **Replace `fluent.FluentIcons` with `fluent.FluentSystemIcons` in Python.** This is needed
   whatever upstream does.
   - Generate it from the MIT Resizable font: about 1.34 MB, 5,192 icons, regular and filled.
   - Update `generate_icons.py`, the templates, the generated files, the docs
     (`types/fluenticons.md`), and every example and test that uses `fluent.FluentIcons.*`.
   - Bundle the font in the extension's Flutter package with its MIT notice.
4. **Regenerate and review all goldens.** Small control icons such as chevrons, close,
   checkmark, the radio dot and the InfoBar icons will look slightly different. Check the
   sizing of the 8 px `caret_*_solid8` replacements in particular.

**Net app size:** about +0.4 MB. Two fonts of about 10 KB plus a 1.34 MB MIT font replace
950 KB.

**Suggested first step:** a proof of concept.
- Write the remap script that builds both replacement fonts.
- Override fluent_ui's fonts locally, for example with `dependency_overrides` pointing to a
  local copy.
- Screenshot-compare the affected controls against the current goldens:
  - ComboBox
  - Expander
  - NavigationView
  - TreeView
  - Menus
  - InfoBar
  - NumberBox
  - PasswordBox
  - AutoSuggestBox
  - DatePicker / TimePicker
  - TabView
  - BreadcrumbBar

---

## 2. Other outstanding issues

1. **TimePicker shows minutes as "5", not "05".** This comes from fluent_ui's private
   `_formatMinute` (`DateFormat.m()` with no padding), which can't be overridden from outside.
   - It needs an upstream fix or the fork from section 1.
   - It is documented in the TimePicker docstring (`date_picker.py`).
   - Related: with a short minute list, such as 15-minute steps, the repeated rows of the
     selected minute are drawn white. The example uses 5-minute steps, where this doesn't show.
   - The user excluded this from the last batch.
2. **DropDownButton and SplitButton menus don't follow an enclosing `fluent.Theme`.** They use
   the app-level theme instead. ContextMenu, MenuBar and CommandBar re-apply the target's theme
   in the flyout route (`_withThemeOf(targetContext)` in `flyout.dart`); these two build their
   flyouts inside fluent_ui and don't.
3. **EditableComboBox shows no red underline when `error_text` is set.** The error text itself
   is shown. fluent_ui's EditableComboBox doesn't expose the highlight color. This is **not yet
   mentioned** in the `error_text` docstring in `combo_box.py`; add a note there (the
   underline is described in `text_box.py`).
4. **Possible flake:** `test_radio_group` errored once, then passed on rerun.
5. **Before merging:**
   - Delete this `HANDOFF-fluent-ui/` folder.
   - Check that CI workflow changes are limited to the `flet-fluent-ui` additions in `ci.yml`
     (`git diff main...HEAD -- .github`). The `macos-integration-tests.yml` workflow is not
     narrowed on this branch.
