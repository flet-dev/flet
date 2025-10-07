# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-06-26

Initial release.

### Added

- Deployed online documentation: https://docs.flet.dev/charts/
- New Chart control: `ScatterChart`

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


[0.2.0]: https://github.com/flet-dev/flet-charts/releases/tag/0.2.0
