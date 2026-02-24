# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.81.1

### Added

- Added `Map.get_camera()` to retrieve current map camera state.
- Added `MapEventType` enum and `MapEvent.event_type`.
- Added `MapEvent.old_camera`, `MapEvent.coordinates`, and `MapEvent.id` payload fields.
- Added support for [WMS](https://www.mngeo.state.mn.us/chouse/wms/index.html) tiles via `TileLayer.wms_configuration` of type `WMSTileLayerConfiguration`.
- Added more examples and `TileLayer` improved documentation.

### Fixed

- Corrected `MapEventSource.INTERACTIVE_FLAGS_CHANGED` value to `interactiveFlagsChanged`.

## 0.80.0

- Added configuration helpers for cameras, interaction flags, and stroke patterns.
- Introduced attribution controls and additional layer types for circles, polygons, and polylines.
- Published hosted documentation: https://docs.flet.dev/map/

## 0.1.0

- Initial release.
