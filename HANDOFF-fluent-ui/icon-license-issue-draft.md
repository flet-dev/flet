# Licensing of the bundled icon fonts (FluentIcons.ttf, SegoeIcons.ttf)

## Summary

fluent_ui bundles two Microsoft icon fonts, and its widgets use them, so every app that depends on fluent_ui ships both fonts on every platform. Neither font comes with a license that seems to allow this. The package's BSD-3 license covers fluent_ui's code, but not these fonts.

Microsoft publishes an MIT-licensed icon set, [Fluent UI System Icons](https://github.com/microsoft/fluentui-system-icons). It has an equivalent for every glyph fluent_ui uses internally. A font with only those glyphs is under 10 KB.

We found this while wrapping fluent_ui for [Flet](https://flet.dev). Everything below is checked against 4.18.1. We'd like to know how you'd prefer to handle it, and we're happy to help with a PR. We're not lawyers: this is what the files and Microsoft's public pages say, not a legal opinion.

## The fonts

Both fonts are declared in `pubspec.yaml`, so Flutter bundles them in every app. Since 4.18.0, release builds tree-shake the two fonts down to the glyphs an app uses. That makes them smaller, but every app still ships Microsoft's outlines for the glyphs the widgets use.

| Font family | File | Font metadata | Glyphs | Size |
|---|---|---|---|---|
| `FluentIcons` | `fonts/FluentIcons.ttf` | Fabric MDL2 Assets 4.46, "© 2017 Microsoft Corporation. All Rights Reserved." | 2,214 | 500 KB |
| `SegoeIcons` | `fonts/SegoeIcons.ttf` | Segoe Fluent Icons 1.34, "© 2024 Microsoft Corporation. All Rights Reserved." | 1,374 | 452 KB |

**`SegoeIcons.ttf` (Segoe Fluent Icons):**
- The license description embedded in the font (name ID 13) reads:
  > Microsoft supplied font. You may use this font to create, display, and print content as permitted by the license terms or terms of use, of the Microsoft product, service, or content in which this font was included.
- [Microsoft's page for the font](https://learn.microsoft.com/en-us/windows/apps/design/style/segoe-fluent-icons-font) says:
  > You can download the font for use in design and development, but you may not ship it to another platform.
- Microsoft's [font FAQ](https://learn.microsoft.com/typography/fonts/font-faq) says that fonts supplied with Windows generally may not be redistributed.

**`FluentIcons.ttf` (Fabric MDL2 Assets):**
- The font has no license text embedded.
- Fabric icons are covered by the Microsoft Fabric Assets License. The copies of it we could find (for example [this one](https://docs.oracle.com/en/cloud/saas/enterprise-performance-management-common/ethrd/microsoft_lic.html)) limit use to developing for Microsoft products such as Office and Office 365.
- We couldn't find Microsoft's current official text.

## How fluent_ui uses them

**Not counting comments, the widgets in 4.18.1 use:**
- **21 glyphs from `FluentIcons`:** `add`, `calendar`, `caret_down_solid8`, `caret_left_solid8`, `caret_right_solid8`, `caret_up_solid8`, `check_mark`, `chevron_down`, `chevron_left`, `chevron_right`, `chevron_up`, `chrome_close`, `clear`, `completed_solid`, `critical_error_solid`, `global_nav_button`, `info_solid`, `more`, `radio_bullet`, `red_eye`, `status_error_full`.
- **30 glyphs from `WindowsIcons`:** `add`, `back`, `calendar`, `camera`, `caret_down_solid8`, `caret_left_solid8`, `caret_right_solid8`, `caret_up_solid8`, `check_mark`, `chevron_down`, `chevron_left`, `chevron_right`, `chevron_up`, `chrome_close`, `clear`, `completed_solid`, `copy`, `cut`, `delete`, `favorite_star`, `favorite_star_fill`, `global_nav_button`, `info_solid`, `more`, `paste`, `red_eye`, `search`, `share`, `status_error_full`, `undo`.

**Public API:** the `FluentIcons` and `WindowsIcons` classes are part of the public API, so apps also use the fonts directly.

## The MIT alternative

[Fluent UI System Icons](https://github.com/microsoft/fluentui-system-icons) is Microsoft's open-source Fluent 2 icon set:
- It is MIT-licensed ("Copyright (c) Microsoft Corporation").
- It is published by `microsoft.com` on pub.dev as [`fluentui_system_icons`](https://pub.dev/packages/fluentui_system_icons).

| | Size |
|---|---|
| The package as a dependency (it declares only its Regular and Filled fonts, every icon at 10–48 px) | about 4.6 MB |
| `FluentSystemIcons-Resizable.ttf` from the repo (every icon once, regular and filled, drawn at 20 px and scalable) | 1.6 MB |
| The Resizable font cut down to the icons the widgets use | 4–7 KB per font |

Every glyph the widgets use has an equivalent:

| Used internally | Fluent UI System Icons equivalent |
|---|---|
| `chevron_*` | `chevron_*` |
| `caret_*_solid8` | `caret_*` (filled) |
| `chrome_close` | `dismiss` |
| `check_mark` | `checkmark` |
| `global_nav_button` | `navigation` |
| `info_solid` | `info` (filled) |
| `critical_error_solid` | `error_circle` (filled) |
| `radio_bullet` | `circle` (filled) |
| `back` | `arrow_left` |
| `clear` | `dismiss` |
| `more` | `more_horizontal` |
| `paste` | `clipboard_paste` |
| `red_eye` | `eye` |
| `undo` | `arrow_undo` |
| `favorite_star` and `favorite_star_fill` | `star` (regular and filled) |
| `add`, `calendar`, `camera`, `copy`, `cut`, `delete`, `search`, `share` | same names (`calendar` is drawn as `calendar_ltr`) |
| `completed_solid` and `status_error_full` (InfoBar) | `checkmark_circle` and `dismiss_circle` (filled) |

## Options

1. **Switch the widgets to Fluent UI System Icons, and drop the two Microsoft fonts.**
   - Bundle a small MIT font with the glyphs the widgets need, keeping the MIT notice.
   - Deprecate the `FluentIcons` and `WindowsIcons` classes, and point users to `fluentui_system_icons` or a full MIT font.
   - *Pros:* this removes the problem entirely and makes the package smaller.
   - *Cons:* a breaking change for apps that use `FluentIcons` or `WindowsIcons`, and a few glyphs will look slightly different.

2. **Switch the widgets as in option 1, but move the two classes and their fonts to a separate opt-in package.**
   - The core package becomes clean.
   - Apps that want the old icons add the separate package, with a note about Microsoft's terms.
   - *Pros:* the core package becomes clean while existing users keep a migration path.
   - *Cons:* the licensing question remains for the separate package, which has to be maintained too.

3. **Keep the fonts and document the situation.**
   - Add a note to the README explaining the terms that come with the fonts, so app developers can decide for themselves.
   - *Pros:* no code change.
   - *Cons:* the redistribution question stays, and every downstream app inherits it.

4. **Draw the internal glyphs as widgets instead of font glyphs.**
   - `ChevronDown` in `custom_icons.dart` already works this way.
   - *Pros:* no icon font is needed for the widgets.
   - *Cons:* the most work, it doesn't cover the public icon classes, and it still needs one of the options above for those.

Our preference would be option 1 or 2. We can open a PR for either one, if you tell us which direction you prefer.

For Flet we've done a stopgap on our fork, [`fix/mit-icon-fonts`](https://github.com/flet-dev/fluent_ui/tree/fix/mit-icon-fonts), that could be a starting point:
- `tool/build_mit_icon_fonts.py` (fonttools) finds the glyphs the widgets use and rebuilds `FluentIcons.ttf` and `SegoeIcons.ttf` from the MIT glyphs, at the same codepoints. Each glyph is scaled to the bounding box of the one it replaces, so the widgets look almost the same. It fails if a used glyph has no mapping.
- No Dart code changes, and all tests pass. The other `FluentIcons` and `WindowsIcons` constants draw nothing, which is why it's a stopgap rather than a PR.
