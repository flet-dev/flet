---
slug: flet-v-1-1-release-announcement
title: "Flet 1.1: shadcn/ui controls, notifications and a fresh neutral look"
authors: [feodor, henri]
tags: [releases]
toc_max_heading_level: 2
---

{/* TODO: hero image, e.g. <img src="/img/blog/flet-1-1/flet-1-1.png" className="screenshot screenshot-70" style={{borderRadius: '7px'}} alt="Flet 1.1" /> */}

Flet 1.1.0 is here, the first feature release since [Flet 1.0](/blog/flet-1-0)!

When we shipped 1.0, the [roadmap](/roadmap) promised "more UI choices such as shadcn" and newer Flutter versions. 1.1 delivers the first of both: a full set of **shadcn/ui-styled controls**, **local notifications** on every platform, a cleaner **neutral default theme**, and **Flutter 3.47** with the Impeller renderer on desktop. There's also a long list of `flet build` improvements and bug fixes, many of them from the community.

Highlights in this release:

* **[shadcn/ui controls](/docs/controls/shadcnui)** - 33 new controls styled after [shadcn/ui](https://ui.shadcn.com), with color schemes and the [Lucide](https://lucide.dev) icon set.
* **[Local notifications](/docs/services/notifications)** - show, schedule and cancel notifications on Android, iOS, macOS, Windows, Linux and web.
* **Neutral theme surfaces** - white and near-black backgrounds by default, plus new themes for text fields, dropdowns and Markdown.
* **Min and max sizes on every control** - `min_width`, `max_width`, `min_height` and `max_height` for responsive layouts without resize handlers.
* **Flutter 3.47.9** with Impeller as the default desktop renderer.
* **More `flet build` options** - Android intent filters and App Links, package visibility queries, iOS entitlements, per-platform permissions and more.
* **New APIs** - [`RefreshIndicator`](/docs/controls/refreshindicator), `Page.get_package_info()`, keyboard actions for text fields and an awaitable `page.run_task()`.
* **Faster web loading** - Flet serves web app files gzip-compressed, about 3x smaller.

{/* truncate */}

## How to upgrade

If you use pip:

```bash
pip install 'flet[all]' --upgrade
```

If you use uv with `pyproject.toml` and want to upgrade all dependencies:

```bash
uv sync --upgrade
```

To upgrade only the core Flet packages:

```bash
uv sync --upgrade-package flet \
  --upgrade-package flet-cli \
  --upgrade-package flet-desktop \
  --upgrade-package flet-web
```

Update any Flet extension packages you use, such as `flet-audio` or `flet-video`, to their 1.1 release as well.

Before upgrading an existing app, review the [1.1.0 breaking changes](/docs/updates/breaking-changes#released-in-flet-110). Most apps need no changes, but the new default theme will make your app look a little different.

## shadcn/ui controls

[shadcn/ui](https://ui.shadcn.com) is one of the most popular design systems on the web, and now you can use its look in Flet. The new `flet-shadcn-ui` extension is built on the Flutter [`shadcn_ui`](https://pub.dev/packages/shadcn_ui) package and brings **33 controls**:

* **Buttons and display:** `Button`, `IconButton`, `Badge`, `Alert`, `Avatar`, `Card`, `Breadcrumb`, `Separator`, `Progress`, `Table`.
* **Forms:** `Input`, `Textarea`, `Checkbox`, `Switch`, `Slider`, `RadioGroup`, `Select`, `InputOTP`.
* **Dates and times:** `Calendar`, `DatePicker`, `DateRangePicker`, `TimePicker`.
* **Layout and navigation:** `Tabs`, `Accordion`, `ResizablePanelGroup`, `Menubar`, `ContextMenu`.
* **Overlays:** `Tooltip`, `Popover`, `Dialog`, `Sheet`, `Toast`, `Sonner`.

Add the package to your project:

```bash
uv add flet-shadcn-ui
```

and import it, typically as `shad`:

```python
import flet as ft
import flet_shadcn_ui as shad


def main(page: ft.Page):
    page.add(shad.Button("Continue", leading=shad.LucideIcons.ARROW_RIGHT))


ft.run(main)
```

The controls work without any setup and follow the page's light or dark mode. To pick another color scheme, a fixed brightness or a different corner radius, wrap them in a `shad.Theme`:

```python
shad.Theme(
    color_scheme=shad.ColorScheme.VIOLET,
    content=ft.Column([shad.Button("Save"), shad.Switch(label="Notify me")]),
)
```

The extension also ships the full **Lucide icon set** as `shad.LucideIcons`, and you can use those icons anywhere Flet accepts an icon, including core controls like `ft.Icon` and `ft.IconButton`.

Building forms is simpler too: value controls such as `Input`, `Select`, `DatePicker` and `RadioGroup` have `label`, `description` and `error_text` properties, so a validated form is just a column of fields and a few lines of Python. See the [form example](/docs/controls/shadcnui#forms).

<img src="/img/blog/flet-1-1/shadcn.png" className="screenshot screenshot-70" style={{borderRadius: '7px'}} alt="Shadcn Card, Input, Select, Switch, Button, Calendar and Badge controls in a Flet app" />

You can try every shadcn control in the Gallery of [Flet Studio](https://studio.flet.dev/gallery/shadcn?utm_source=flet.dev&utm_medium=blog&utm_campaign=flet-v-1-1-release-announcement). Big thanks to [@InesaFitsner](https://github.com/InesaFitsner) for building this extension!

More info:

* PR: [#6918](https://github.com/flet-dev/flet/pull/6918)
* Docs: [Shadcn controls](/docs/controls/shadcnui)

## Local notifications

The new `flet-notifications` extension adds a `Notifications` service that shows, schedules and cancels **local notifications** on Android, iOS, macOS, Windows, Linux and web. It wraps the [`flutter_local_notifications`](https://pub.dev/packages/flutter_local_notifications) Flutter package.

```python
import flet as ft
import flet_notifications as ftn


def main(page: ft.Page):
    def handle_tap(e: ftn.NotificationEvent):
        page.show_dialog(ft.SnackBar(f"Opened notification {e.payload}"))

    notifications = ftn.Notifications(on_tap=handle_tap)

    async def notify(e: ft.Event[ft.Button]):
        if not await notifications.request_permissions():
            page.show_dialog(ft.SnackBar("Notifications are turned off."))
            return
        await notifications.show(
            id=1,
            title="Notification Title",
            body="This is the notification body...",
            payload="notif-1",
        )

    page.add(ft.SafeArea(content=ft.Button("Notify", on_click=notify)))


ft.run(main)
```

Beyond showing a notification right away, you can:

* **Schedule** notifications for later, once or repeating (every morning at 9, every hour), and the OS delivers them even when your app isn't running.
* Request **permissions**, set up **Android channels**, and use rich styles such as big pictures, inbox lists and progress bars.
* Add **action buttons**, including inline reply, and handle taps and actions with typed event handlers.

Notifications are local: your app posts them itself. Push notifications sent from a server through Firebase or APNs aren't covered by this extension.

To make this possible, `flet build` learned a few new things that every extension can use now:

* Extensions can declare their own build settings, such as Android compile options and Gradle dependencies, in a `flet-extension.toml` file. They're applied to every app that installs the extension. See [Build settings](/docs/extend/user-extensions#build-settings).
* `[tool.flet.android].res_dir` bundles your own Android resources, such as a notification icon or sound. See [Resources](/docs/publish/android#resources).
* `[tool.flet.ios.entitlement]` and `--ios-entitlements` sign iOS apps with entitlements such as push notifications, universal links, App Groups or critical alerts. See [Entitlements](/docs/publish/ios#entitlements).

Big thanks to [@Nwokike](https://github.com/Nwokike) for creating the extension!

More info:

* Issue: [#6948](https://github.com/flet-dev/flet/issues/6948), PR: [#6999](https://github.com/flet-dev/flet/pull/6999)
* Docs: [Notifications](/docs/services/notifications)

## A fresh neutral look

Material 3 tints every surface with the seed color, which can make an app look like it's been dipped in purple. Starting with 1.1, themes built from a seed color, including the default theme, have **neutral surfaces**: white in light mode, near-black (`#121212`) in dark mode, and neutral greys for containers, outlines and text. The seed color still drives accents such as buttons, switches and focus rings.

{/* TODO: before/after screenshot, e.g. /img/blog/flet-1-1/neutral-surfaces.png */}

If you prefer the tinted Material 3 look, it's one line away:

```python
page.theme = ft.Theme(surfaces=ft.ThemeSurfaces.TONAL)
page.dark_theme = ft.Theme(surfaces=ft.ThemeSurfaces.TONAL)
```

The default dark splash and loading screen of web apps changed to `#121212` to match.

We also added more ways to style your whole app from one place:

* **`Theme.input_decoration_theme`** styles every `TextField` and `Dropdown` at once: border, label, hint, helper and error styles, padding, density and fill. Borders can be set per state (default, hovered, focused, error, disabled), and unset states keep the Material defaults, so a soft resting border still darkens on hover and turns primary on focus:

  ```python
  page.theme = ft.Theme(
      input_decoration_theme=ft.InputDecorationTheme(
          border=ft.OutlineInputBorder(
              border_radius=8,
              side=ft.BorderSide(
                  color=ft.Colors.with_opacity(0.24, ft.Colors.ON_SURFACE)
              ),
          ),
      ),
  )
  ```

* **`Theme.text_field_theme`** sets the style of the text being edited in every `TextField`.
* **`Theme.markdown_theme`** sets a default style sheet for every `Markdown` control. Markdown links and blockquotes now take their colors from the color scheme instead of always being blue.
* **`ft.MaterialTapTargetSize`** with `Theme.material_tap_target_size` and `Switch.material_tap_target_size`: `SHRINK_WRAP` drops Material's 48px minimum tap area for dense, desktop-style layouts.
* **`Dropdown.height`** now sizes the field itself, down to compact heights like 32 or 40.
* **`PopupMenuButton.border_radius`** and `PopupMenuTheme.border_radius` round the hover highlight around custom content.

More info:

* Issue: [#6921](https://github.com/flet-dev/flet/issues/6921)
* Migration: [Default theme surfaces are now neutral](/docs/updates/breaking-changes/v1-1-0/neutral-default-surfaces)

## Min and max sizes on every control

Every layout control now has `min_width`, `max_width`, `min_height` and `max_height`. They are applied by the client on every layout pass, so a centered column with a capped width stays correct while the window resizes:

```python
page.add(
    ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                max_width=760,
                content=ft.Text("This text never gets wider than 760 pixels."),
            ),
        ],
    )
)
```

No more computing widths in Python from `page.width` in an `on_size_change` handler, which always lagged a frame or more behind the window.

## Flutter 3.47 and Impeller on desktop

Flet 1.1 bundles [Flutter 3.47.9](https://github.com/flutter/flutter/blob/stable/CHANGELOG.md#3478) (up from 3.44.8). Android builds use Gradle 9.3.1, Android Gradle Plugin 8.13.2 and Kotlin 2.3.21.

Desktop apps, including the window that `flet run` opens, now render with **Impeller**, Flutter's new default desktop renderer, instead of Skia. If you run into a rendering issue, you can switch back to Skia with `flet build --no-impeller`, `impeller = false` under `[tool.flet]`, `flet run --no-impeller`, or the `FLET_NO_IMPELLER` environment variable. See [Renderer](/docs/publish#renderer).

A few things to know:

* Apps built with `flet build` and the macOS desktop client now require **macOS 12** or later, and iOS apps require **iOS 15** or later. This also fixes builds on Xcode 27, which rejects older deployment targets. See the [macOS 12 and iOS 15 minimum](/docs/updates/breaking-changes/v1-1-0/minimum-macos-12-ios-15) guide.
* Android plugins that still use `jcenter()` or other APIs removed in Gradle 9 no longer build.
* Flet's Dart code now takes Material and Cupertino from the `material_ui` and `cupertino_ui` packages. If you maintain a Flet extension with Dart code, see the [migration guide](/docs/updates/breaking-changes/v1-1-0/material-ui-cupertino-ui).

More info:

* PRs: [#6916](https://github.com/flet-dev/flet/pull/6916), [#7023](https://github.com/flet-dev/flet/pull/7023)

## `flet build` improvements

This release closes many gaps in what you can configure for a packaged app, and fixes a lot of rough edges we found while writing tests for `flet build` settings.

**Android:**

* `[[tool.flet.android.activity.intent_filter]]` adds intent filters to the main activity, for verified App Links, link paths or share targets. See [Activity intent filters](/docs/publish/android#activity-intent-filters).
* `[tool.flet.android.queries]` declares the apps, intents and content providers your app looks up, which Android 11+ hides otherwise, for example to open a payment app or check a URL scheme with `UrlLauncher.can_launch_url()`. See [Queries](/docs/publish/android#queries).
* New settings for [Java compile options](/docs/publish/android#java-compile-options), [Gradle dependencies](/docs/publish/android#gradle-dependencies), and manifest [receivers](/docs/publish/android#receivers) and [services](/docs/publish/android#services).

**All platforms:**

* [Deep links](/docs/publish#deep-linking) need only a scheme: `--deep-linking-scheme myapp` alone opens your Android or iOS app from any `myapp://` link.
* Permissions can be set per platform with `[tool.flet.<platform>].permissions`.
* An empty value in `[tool.flet.<platform>]` for `artifact`, `org`, `bundle_id`, `icon_background` or `splash` now clears the global value for that platform.
* `--log-format github` prints a collapsible group per build step and annotations for warnings and errors in GitHub Actions. See [Log formats](/docs/cli/flet-build#log-formats).
* App icons and the splash screen are always generated, from the Flet logo if your app has no icon of its own.

**Desktop:**

* On macOS, the `.app` bundle is now named after the product name, so Finder, the Dock and Spotlight show your app's real name. See [macOS .app named after the product name](/docs/updates/breaking-changes/v1-1-0/macos-app-named-after-product).
* On Linux, apps register a hidden desktop entry while they run, so GNOME's dock shows the app's icon and name instead of a generic icon. See [App icon](/docs/publish/linux#app-icon).
* The prebuilt Windows desktop client that `flet run` downloads is now **code-signed**, so it starts with Windows Smart App Control turned on.
* Release Windows apps no longer ship Python's debug modules, which saves about 10 MB each.

**Reliability:**

* `flet build` no longer hangs at "Packaging Python app..." on Windows when pip prints a lot of warnings.
* Errors such as a `SyntaxError` in your app are now shown without having to re-run with `-vv`.
* Rebuilds after upgrading Flet, changing build options or editing `requirements.txt` work without cleaning the build directory first.
* Names, copyrights and settings that contain `&`, `<`, `"` or other special characters no longer break Android, iOS, macOS or Windows builds.
* iOS apps no longer fail App Store Connect validation with ITMS-90683 (missing photo library and camera purpose strings).

**Python runtime:** the bundled CPython is updated to 3.12.16, 3.13.18 and 3.14.10, security releases that distrust compromised eMudhra CA keys. Native Python extensions such as `pydantic-core` now import in Windows debug builds and on Linux.

## More new APIs

* **[`RefreshIndicator`](/docs/controls/refreshindicator)** adds pull-to-refresh to a scrollable control: pulling down calls your async `on_refresh` handler and shows a progress indicator until it returns. `show()` triggers a refresh without a pull, for desktop and web. Thanks to [@osamalzabidi](https://github.com/osamalzabidi)!
* **`Page.get_package_info()`** returns an [`ft.PackageInfo`](/docs/types/packageinfo) with the app's name, package name, version, build number, installer store and install and update times. An app built with `flet build` gets the `--build-version` and `--build-number` it was built with, so it no longer needs its own copy of the version.
* **`TextField.text_input_action`** (and `CupertinoTextField.text_input_action`) chooses the action button of the onscreen keyboard. `ft.TextInputAction.NEXT` moves focus to the next field and keeps the keyboard open.
* **`InteractiveViewer`** gets `get_scale()`, `get_transform()` and `on_transform_changed` to read the current zoom, translation and transformation matrix. Thanks to [@ada-koki](https://github.com/ada-koki)!
* **`await page.run_task(handler)`** now returns the value of `handler`.
* **`flet-audio`:** `Audio.audio_context` configures the mobile audio session and focus behavior. Thanks to [@BartoszKog](https://github.com/BartoszKog)!
* **`flet test --update-failed-goldens`** overwrites only the golden screenshots that are missing or no longer match.
* **Faster web loading:** web apps served by Flet, such as with `flet run --web`, send `main.dart.wasm`, `main.dart.js`, CanvasKit and fonts gzip-compressed, about 3x smaller.

## Notable bug fixes

1.1 includes more than 60 bug fixes. Some of the most noticeable ones:

* `use_effect()` cleanups now always run, including `async` cleanups when a dependency changes, and a pending `async` setup is cancelled on unmount.
* A declarative component moved to a different parent, for example when a responsive layout switches from a `Column` to a `Row`, now keeps its state.
* `ResponsiveRow` resizes its children when their `col` changes and works with `spacing=0`.
* `page.query` is no longer empty in `main()` when the app is opened with a query string, and `TemplateRoute.match()` handles query strings and fragments.
* The desktop window no longer flashes endlessly after a `flet run` hot reload, and `flet run -r` no longer restarts when the app writes files to its working directory.
* `FilePicker` dialogs no longer time out after being open for an hour.
* `Window.skip_task_bar` hides the app from the taskbar on Windows.
* `flet-audio-recorder` records to `output_path` on desktop, Android and iOS.
* Embedded `FletApp` no longer steals keyboard focus, the browser tab title or the host's Cupertino colors.

See the full [CHANGELOG](https://github.com/flet-dev/flet/blob/main/CHANGELOG.md#110) for the complete list.

## Breaking changes

Following our [compatibility policy](/docs/updates/compatibility-policy), 1.1 has only a few breaking changes, mostly in how apps look or are packaged:

* [Default theme surfaces are now neutral](/docs/updates/breaking-changes/v1-1-0/neutral-default-surfaces) - set `surfaces=ft.ThemeSurfaces.TONAL` to keep the tinted look.
* [macOS 12 and iOS 15 minimum](/docs/updates/breaking-changes/v1-1-0/minimum-macos-12-ios-15) for apps built with `flet build` and the macOS desktop client.
* [macOS .app named after the product name](/docs/updates/breaking-changes/v1-1-0/macos-app-named-after-product) - set `[tool.flet.macos] artifact` to keep the old name.
* [Material and Cupertino now come from material_ui and cupertino_ui](/docs/updates/breaking-changes/v1-1-0/material-ui-cupertino-ui) - affects extensions with Dart code only.
* Custom `flet build` templates must read settings from `cookiecutter._options` and `cookiecutter._pyproject` (were `cookiecutter.options` and `cookiecutter.pyproject`).
* `flet build` for macOS and Windows no longer writes a placeholder copyright, and Windows builds escape company and product names themselves: remove any `""` or `\\` you added by hand.
* The Flet desktop client is no longer built for Debian 10 on ARM64. Debian 10 on x86-64 is still supported.

## Thank you, contributors!

Many of the changes in this release came from the community. Thank you all:

* [@InesaFitsner](https://github.com/InesaFitsner) - the `flet-shadcn-ui` extension.
* [@Nwokike](https://github.com/Nwokike) - the `flet-notifications` extension.
* [@osamalzabidi](https://github.com/osamalzabidi) - the `RefreshIndicator` control.
* [@ada-koki](https://github.com/ada-koki) - zoom and transform API for `InteractiveViewer`.
* [@BartoszKog](https://github.com/BartoszKog) - `Audio.audio_context` in `flet-audio`.
* [@mangod12](https://github.com/mangod12) - `use_effect()` cleanup fixes.
* [@mmporong](https://github.com/mmporong) - `use_state()` and `use_ref()` type inference in mypy and ty.
* [@RezaShamsipour](https://github.com/RezaShamsipour) - finding `Tab` and `PopupMenuItem` by key in `flet test`.
* [@inchang-ing](https://github.com/inchang-ing) - the `GestureDetector.on_tap_move` fix.
* [@LaoChouPro](https://github.com/LaoChouPro) - per-platform `hide_window_on_start`.
* [@AbhayPhalswal](https://github.com/AbhayPhalswal) - clearing global `flet build` settings per platform.

## Conclusion

Flet 1.1 is about choice: a second design system next to Material and Cupertino, a theme that stays out of your app's way, and more control over how your app is packaged for each platform. And we're just getting started: more UI libraries from the [roadmap](/roadmap) are on the way.

Try it in your apps and share your feedback in [GitHub Discussions](https://github.com/flet-dev/flet/discussions) or on [Discord](https://discord.gg/dzWXP8SHG8).

Happy Flet-ing!
