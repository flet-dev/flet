# Licensing of the bundled icon fonts (FluentIcons.ttf, SegoeIcons.ttf)

## Summary

fluent_ui bundles two Microsoft icon fonts, and its widgets use them, so every app that depends on fluent_ui ships both fonts on every platform. Neither font comes with a license that seems to allow this. The package's BSD-3 license covers fluent_ui's code, but not these fonts.

Microsoft publishes an MIT-licensed icon set, [Fluent UI System Icons](https://github.com/microsoft/fluentui-system-icons). It has an equivalent for every glyph fluent_ui uses internally. A font with only those glyphs is about 10 KB.

We found this while wrapping fluent_ui 4.17.0 for [Flet](https://flet.dev). We'd like to know how you'd prefer to handle it, and we're happy to help with a PR. We're not lawyers: this is what the files and Microsoft's public pages say, not a legal opinion.

## The fonts

Both fonts are declared in `pubspec.yaml`, so Flutter bundles them in every app.

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

**Not counting comments, the widgets use:**
- **12 glyphs from `FluentIcons`:** `caret_down_solid8`, `caret_up_solid8`, `check_mark`, `chevron_down`, `chevron_left`, `chevron_right`, `chevron_up`, `chrome_close`, `critical_error_solid`, `global_nav_button`, `info_solid`, `radio_bullet`.
- **27 glyphs from `WindowsIcons`:** `add`, `back`, `calendar`, `camera`, `caret_down_solid8`, `caret_left_solid8`, `caret_right_solid8`, `caret_up_solid8`, `check_mark`, `chevron_down`, `chevron_left`, `chevron_right`, `chevron_up`, `chrome_close`, `clear`, `copy`, `cut`, `delete`, `favorite_star`, `favorite_star_fill`, `global_nav_button`, `more`, `paste`, `red_eye`, `search`, `share`, `undo`.

**Two more points:**
- **Public API:** the `FluentIcons` and `WindowsIcons` classes are part of the public API, so apps also use the full fonts directly.
- **Material Icons:** `InfoBar` uses two Material icons, `Icons.check_circle` and `Icons.cancel`, for the success and error severities. A `TODO(fluent): Do not use Material Icons` comment is already there. Material Icons are Apache 2.0, so they raise no licensing problem, but this would be a good moment to move them too.

## The MIT alternative

[Fluent UI System Icons](https://github.com/microsoft/fluentui-system-icons) is Microsoft's open-source Fluent 2 icon set:
- It is MIT-licensed ("Copyright (c) Microsoft Corporation").
- It is published by `microsoft.com` on pub.dev as [`fluentui_system_icons`](https://pub.dev/packages/fluentui_system_icons).

| | Size |
|---|---|
| The package as a dependency (it declares only its Regular and Filled fonts, every icon at 10–48 px) | about 4.6 MB |
| `FluentSystemIcons-Resizable.ttf` from the repo (every icon once, regular and filled, drawn at 20 px and scalable) | 1.4 MB |
| The Resizable font cut down to the icons the widgets use (regular and filled) | about 10 KB |

Every glyph the widgets use has an equivalent:

| Used internally | Fluent UI System Icons equivalent |
|---|---|
| `chevron_*` | `chevron_*` |
| `caret_*_solid8` | `caret_*` (filled) |
| `chrome_close` | `dismiss` |
| `check_mark` | `checkmark` |
| `global_nav_button` | `navigation` |
| `info_solid` | `info` (filled) |
| `critical_error_solid` | `error_circle` or `warning` (filled) |
| `radio_bullet` | `circle` (filled) |
| `back` | `arrow_left` |
| `clear` | `dismiss_circle` |
| `more` | `more_horizontal` |
| `paste` | `clipboard_paste` |
| `red_eye` | `eye` |
| `undo` | `arrow_undo` |
| `favorite_star` and `favorite_star_fill` | `star` (regular and filled) |
| `add`, `calendar`, `camera`, `copy`, `cut`, `delete`, `search`, `share` | same names |
| `Icons.check_circle` and `Icons.cancel` (InfoBar) | `checkmark_circle` and `dismiss_circle` (filled) |

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

Our preference would be option 1 or 2. We can open a PR for either one, including the glyph mapping and a script that rebuilds the small font from Microsoft's repo, if you tell us which direction you prefer.
