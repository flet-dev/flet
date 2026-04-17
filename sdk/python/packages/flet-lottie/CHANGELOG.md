# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## 0.85.0

### Fixed

- Fix `Lottie` failing to load local asset files on Windows desktop (and unreliably on other desktop platforms), so animations referenced by `src="file.json"` from the app's `assets/` directory now display correctly ([#6386](https://github.com/flet-dev/flet/issues/6386)) by @ndonkoHenri.

## 0.80.0

## Added

- `Lottie` control new properties: `enable_merge_paths`, `enable_layers_opacity`, `headers`, `error_content`.
- Deployed online documentation: https://flet.dev/docs/lottie/

### Changed

- Refactored `Lottie` control to use `@ft.control` dataclass-style definition.

## 0.1.0

Initial release.
