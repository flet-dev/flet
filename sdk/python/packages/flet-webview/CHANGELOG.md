# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## 1.1.0

### Added

- Windows and Linux support. On web, the methods and events now work for same-origin pages and HTML loaded with `load_html()` ([#6530](https://github.com/flet-dev/flet/issues/6530), [#5934](https://github.com/flet-dev/flet/issues/5934)) by @ndonkoHenri.

### Changed

- Built on the [`webview_all`](https://pub.dev/packages/webview_all) Flutter package on every platform, instead of `webview_flutter` and `webview_flutter_web` ([#6530](https://github.com/flet-dev/flet/issues/6530)) by @ndonkoHenri.
- On Linux, apps using `WebView` need `libwebkit2gtk-4.1-0` to run (Debian 12, Ubuntu 22.04 and newer) and `libwebkit2gtk-4.1-dev` to build with `flet build linux` ([#6530](https://github.com/flet-dev/flet/issues/6530)) by @ndonkoHenri.

## 0.80.0

### Added

- Deployed online documentation: https://flet.dev/docs/webview/

### Changed

- Refactored all controls to use `@flet.control` dataclass-style definition.

## 0.1.0

Initial release.
