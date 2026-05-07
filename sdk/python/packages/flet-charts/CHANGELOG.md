# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## 0.85.0

### Fixed

- Fixed `LineChartEvent.spots` returning undecoded MessagePack extension values instead of `LineChartEventSpot` objects ([#6443](https://github.com/flet-dev/flet/issues/6443), [#6468](https://github.com/flet-dev/flet/pull/6468)) by @ndonkoHenri.
- Fixed `LineChart` (and other charts) silently dropping custom `ChartAxisLabel` entries whose `value` matched a tick only after floating-point rounding (e.g. `0.1`, `0.2`, `0.3`) by switching label lookup to a tolerance-based comparison scaled to the axis interval ([#6445](https://github.com/flet-dev/flet/issues/6445), [#6459](https://github.com/flet-dev/flet/pull/6459)) by @KangZhaoKui.
- Fixed unbounded browser memory growth in `MatplotlibChart` on Flutter web (CanvasKit/WASM) during animations by replacing the generic `Canvas` + `capture()` rendering flow with a dedicated `MatplotlibChartCanvas` widget that composites matplotlib diff frames in CPU memory; also fixes Safari async PNG decode (`EncodingError: Loading error.`), a render/`figure.savefig()` race that crashed the toolbar Download, and pan/zoom playback lag from buffered pointer events ([#6473](https://github.com/flet-dev/flet/pull/6473)) by @FeodorFitsner.

## 0.80.0

Initial release.

### Added

- Deployed online documentation: https://flet.dev/docs/charts/
- New Chart control: `ScatterChart`
- New Chart control: `CandlestickChart`

#### BarChart

- New property: `tooltip`
- New enum: `BarChartTooltipDirection`
- In `BarChartRod`: new property `tooltip`

#### LineChart

- New property: `tooltip`
- In `LineChartDataPoint`: new property `tooltip` (now accepts a `LineChartDataPointTooltip` instance)

### Changed

All chart controls have been refactored to use `@ft.control` dataclass-style definition

#### BarChart

- Renamed properties:
    - `bar_groups` → `groups`
    - `groups_space` → `spacing`
    - `animate` → `animation`
    - `on_chart_event` → `on_event`
- Tooltip configuration has been redesigned:
    - Removed properties: `tooltip_bgcolor`, `tooltip_rounded_radius`, `tooltip_margin`, `tooltip_padding`, `tooltip_max_content_width`, `tooltip_rotate_angle`, `tooltip_horizontal_offset`, `tooltip_border_side`, `tooltip_fit_inside_horizontally`, `tooltip_fit_inside_vertically`, `tooltip_direction`
    - use the new `tooltip` property of type `BarChartTooltip`
- In `BarChartGroup`:
    - Renamed properties:
      - `bar_rods` → `rods`
      - `bars_space` → `spacing`
- In `BarChartRod`:
    - Renamed properties:
      - `rod_stack_items` → `stack_items`
      - `bg_color` → `bgcolor`
      - `bg_gradient` → `background_gradient`

#### LineChart

- Renamed properties:
    - `animate` → `animation`
    - `on_chart_event` → `on_event`
- `LineChart` Tooltip configuration has been redesigned:
    - Removed properties: `tooltip_bgcolor`, `tooltip_rounded_radius`, `tooltip_margin`, `tooltip_padding`, `tooltip_max_content_width`, `tooltip_rotate_angle`, `tooltip_horizontal_offset`, `tooltip_border_side`, `tooltip_fit_inside_horizontally`, `tooltip_fit_inside_vertically`, `tooltip_show_on_top_of_chart_box_area`
    - use the new `tooltip` property of type `LineChartTooltip`
- In `LineChartData`:
    - Renamed properties: `data_points` → `points`, `stroke_cap_round` → `rounded_stroke_cap`
    - Removed properties: `above_line_bgcolor`, `below_line_bgcolor`
    - Renamed property: `selected_below_line`
- In `LineChartDataPoint`:
    - Removed properties: `tooltip_align`, `tooltip_style` - use `tooltip` property instead which is now of type `LineChartDataPointTooltip`

#### PieChart

- Renamed properties:
    - `animate` → `animation`
    - `on_chart_event` → `on_event`
