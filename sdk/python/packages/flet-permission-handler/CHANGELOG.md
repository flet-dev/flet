# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-06-26

## Added

- Deployed online documentation: https://docs.flet.dev/permission-handler/
- `PermissionHandler` control new methods:
    - `get_status_async`
    - `request_async`
    - `open_app_settings_async`

### Changed

- Refactored `PermissionHandler` control to use `@ft.control` dataclass-style definition and switched to `Service` control type

### Breaking Changes

- Enum `PermissionType` renamed to `Permission`
- `PermissionHandler` method `check_permission_async` renamed to `get_status_async`, with parameters changed:
    - `of` → `permission` (type: `PermissionType` → `Permission`)
    - `wait_timeout` → `timeout`
- `PermissionHandler` method `request_permission_async` renamed to `request_async`, with parameters changed:
    - `of` → `permission` (type: `PermissionType` → `Permission`)
    - `wait_timeout` → `timeout`
- `PermissionHandler` method `open_app_settings_async` parameter `wait_timeout` renamed to `timeout` (type: `Optional[float]` → `int`)
- Removed sync methods from `PermissionHandler`:
    - `check_permission` → use `get_status_async` instead
    - `request_permission` → use `request_async` instead
  - `open_app_settings` → use `open_app_settings_async` instead
- `PermissionHandler` must now be added to `Page.services` before being used instead of `Page.overlay`.
- `PermissionHandler` can now only be used on the following platforms: Windows, iOS, Android, and Web. A `FletUnimplementedPlatformEception` will be raised if used on unsupported platforms.

## [0.1.0] - 2025-01-15

Initial release.


[0.2.0]: https://github.com/flet-dev/flet-permission-handler/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/flet-dev/flet-permission-handler/releases/tag/0.1.0
