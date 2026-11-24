# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## 0.85.1

### Fixed

- `Geolocator.get_last_known_position()` no longer crashes with `TypeError: argument after ** must be a mapping, not NoneType` when the platform has no cached fix; it now returns `Optional[GeolocatorPosition]` and yields `None` for the empty case ([#6487](https://github.com/flet-dev/flet/pull/6487)).
- `Geolocator.get_current_position()` no longer hangs indefinitely on web — added a Dart-side `Future.timeout` workaround for the upstream [`geolocator_web` 4.1.3](https://pub.dev/packages/geolocator_web) `inMicroseconds`/`inMilliseconds` timeout typo, and picked sensible web defaults (`time_limit: 30s`, `maximum_age: 5m`) for single-shot calls only (the position stream is left untouched) ([#6487](https://github.com/flet-dev/flet/pull/6487)).
- The Dart side reading `args["settings"]` instead of `args["configuration"]` silently dropped the configuration on every `getCurrentPosition` call; now resolved ([#6487](https://github.com/flet-dev/flet/pull/6487)).
- The position stream is now gated behind a registered `on_position_change` / `on_error` handler, and the previous subscription is cancelled on `update()` to prevent listener leaks and unsolicited CoreLocation prompts at service init ([#6487](https://github.com/flet-dev/flet/pull/6487)).
- Platform exceptions (`LocationServiceDisabledException`, `PermissionDeniedException`, `PermissionDefinitionsNotFoundException`, `PermissionRequestInProgressException`, `PositionUpdateException`, `TimeoutException`) are translated into actionable error messages via a private `_GeolocatorException` whose `toString()` drops the default `Exception:` prefix, so Python sees `RuntimeError("Location request timed out.")` rather than `RuntimeError("Exception: ...")` ([#6487](https://github.com/flet-dev/flet/pull/6487)).

### Documentation

- Added a "Web: cached vs. fresh positions" section explaining the default `maximum_age` and how to override it via `GeolocatorWebConfiguration` ([#6487](https://github.com/flet-dev/flet/pull/6487)).
- Added a macOS troubleshooting note for the recurring browser `POSITION_UNAVAILABLE` failure mode (`sudo killall locationd`) ([#6487](https://github.com/flet-dev/flet/pull/6487)).

## 0.80.0

### Added

- Deployed online documentation: https://flet.dev/docs/geolocator/
- `Geolocator` control new methods: `distance_between`
- `Geolocator` control new properties: `position`, `configuration`
- New dataclasses:
    - `GeolocatorConfiguration`
    - `GeolocatorWebConfiguration`
    - `GeolocatorIosConfiguration`
    - `GeolocatorAndroidConfiguration`
    - `ForegroundNotificationConfiguration`

### Changed

- Refactored `Geolocator` control to use `@ft.control` dataclass-style definition and switched to `Service` control type

#### Breaking Changes

- `Geolocator` must now be added to `Page.services` instead of `Page.overlay`.
- `Geolocator` method `get_current_position_async` parameters changed:
    - removed `accuracy`
    - `location_settings` renamed to `configuration` (type changed)
    - `wait_timeout` renamed to `timeout`
- In all `Geolocator` methods, parameter `wait_timeout` renamed to `timeout`.
- The following `Geolocator` sync methods were made [`async`](https://docs.python.org/3/library/asyncio.html):
    - `get_current_position`
    - `get_last_known_position`
    - `get_permission_status`
    - `request_permission`
    - `is_location_service_enabled`
    - `open_app_settings`
    - `open_location_settings`
- Enum `GeolocatorActivityType` renamed to `GeolocatorIosActivityType`

## 0.1.0

Initial release.


[0.2.0]: https://github.com/flet-dev/flet-geolocator/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/flet-dev/flet-geolocator/releases/tag/0.1.0
