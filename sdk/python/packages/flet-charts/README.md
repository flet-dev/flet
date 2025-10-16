# flet-charts

[![pypi](https://img.shields.io/pypi/v/flet-charts.svg)](https://pypi.python.org/pypi/flet-charts)
[![downloads](https://static.pepy.tech/badge/flet-charts/month)](https://pepy.tech/project/flet-charts)
[![license](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-charts/LICENSE)

A [Flet](https://flet.dev) extension for creating interactive charts and graphs.

It is based on the [fl_chart](https://pub.dev/packages/fl_chart) Flutter package.

## Documentation

Detailed documentation to this package can be found [here](https://docs.flet.dev/charts/).

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅   |  ✅  |    ✅    |  ✅  |

## Usage

### Installation

To install the `flet-charts` package and add it to your project dependencies:

- Using `uv`:
    ```bash
    uv add flet-charts
    ```

- Using `pip`:
    ```bash
    pip install flet-charts
    ```
    After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.

### Examples

For examples, see [these](https://github.com/flet-dev/flet/tree/main/sdk/python/examples/controls/charts).

### Available charts

- [`BarChart`](https://docs.flet.dev/charts/bar_chart/)
- [`CandlestickChart`](https://docs.flet.dev/charts/candlestick_chart/)
- [`LineChart`](https://docs.flet.dev/charts/line_chart/)
- [`MatplotlibChart`](https://docs.flet.dev/charts/matplotlib_chart/)
- [`PieChart`](https://docs.flet.dev/charts/pie_chart/)
- [`PlotlyChart`](https://docs.flet.dev/charts/plotly_chart/)
- [`RadarChart`](https://docs.flet.dev/charts/radar_chart/)
- [`ScatterChart`](https://docs.flet.dev/charts/scatter_chart/)
