# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-06-26

### Added

- Deployed online documentation: https://docs.flet.dev/geolocator/
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

## [0.1.0] - 2025-01-15

Initial release.


[0.2.0]: https://github.com/flet-dev/flet-geolocator/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/flet-dev/flet-geolocator/releases/tag/0.1.0
