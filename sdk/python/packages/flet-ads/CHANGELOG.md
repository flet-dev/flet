# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## 0.82.0

### Changed

- Refactored ads controls: `BaseAd` is now based on `flet.BaseControl`, `InterstitialAd` is now a `flet.Service`, `BannerAd` is now a `flet.LayoutControl`, and examples were updated ([#6194](https://github.com/flet-dev/flet/issues/6194), [#6235](https://github.com/flet-dev/flet/pull/6235)).

## 0.80.0

### Added

- Deployed online documentation: https://flet-dev.github.io/flet-ads/

### Changed

- Refactored all controls to use `@flet.control` dataclass-style definition.

## 0.1.0

Initial release.
