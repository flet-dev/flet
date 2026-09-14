# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## 1.0.0

### Added

- Windows and Linux support, via the [`webview_all_windows`](https://pub.dev/packages/webview_all_windows) (WebView2) and [`webview_all_linux`](https://pub.dev/packages/webview_all_linux) (WebKitGTK) Flutter packages. All `WebView` properties, methods and events that work on Android, iOS and macOS now work on Windows and Linux too — including `on_scroll`, which remains unsupported on macOS ([#6530](https://github.com/flet-dev/flet/issues/6530)) by @ndonkoHenri.

### Fixed

- The platform conditional import was keyed on `dart.library.html`, which `dart2wasm` does not define, so a `--wasm` build selected the native (non-web) implementation rather than the web one. This had no user-visible effect while that implementation was an empty stub, but would have broken every Wasm build once it gained a `dart:io` dependency. Re-keyed to `dart.library.io` ([#6530](https://github.com/flet-dev/flet/issues/6530)) by @ndonkoHenri.

### Notes

- On Linux the `WebView` is a native GTK widget rather than a Flutter texture: other controls cannot be drawn over it, and a scale, rotation or skew transform — or a non-rectangular clip, such as a `Container.border_radius` or an enclosing `Card` — hides it entirely.
- Running a Linux app that uses `WebView` requires `libwebkit2gtk-4.1-0`, which is unavailable before Debian 12 and Ubuntu 22.04. The prebuilt `light` desktop client does not bundle the extension, so `flet run` on Linux needs the `full` flavor.
- `on_javascript_alert_dialog` does not fire on Windows, where Edge WebView2 always shows its own alert dialog. On Linux, setting the handler suppresses the built-in dialog, so leave it unset to keep the native one.
- On Windows, `load_file()` serves the file from an internal virtual host, so `get_current_url()` and `on_url_change` report an `https://...webview.invalid/` URL rather than the original `file://` one.
- On Linux, `WebViewConsoleMessageEvent.severity_level` is always `LogLevelSeverity.LOG`.

## 0.80.0

### Added

- Deployed online documentation: https://flet.dev/docs/webview/

### Changed

- Refactored all controls to use `@flet.control` dataclass-style definition.

## 0.1.0

Initial release.
