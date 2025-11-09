# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.2.0] - Unreleased

## Added

- Deployed online documentation: https://docs.flet.dev/flashlight/
- `Flashlight` control new properties: `on`, `on_error`
- `Flashlight` control new methods: `is_available`
- New exception classes:
    - `FlashlightException`
    - `FlashlightEnableExistentUserException`
    - `FlashlightEnableNotAvailableException`
    - `FlashlightEnableException`
    - `FlashlightDisableExistentUserException`
    - `FlashlightDisableNotAvailableException`
    - `FlashlightDisableException`

### Changed

- Refactored `Flashlight` control to use `@ft.control` dataclass-style definition and switched to `Service` control type.
- `Flashlight` must now be added to `Page.services` instead of `Page.overlay` due to control type change.

## [0.1.0] - 2025-01-15

Initial release.


[0.2.0]: https://github.com/flet-dev/flet-flashlight/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/flet-dev/flet-flashlight/releases/tag/0.1.0
