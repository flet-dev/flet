# flet-charts

[![pypi](https://img.shields.io/pypi/v/flet-charts.svg)](https://pypi.python.org/pypi/flet-charts)
[![downloads](https://static.pepy.tech/badge/flet-charts/month)](https://pepy.tech/project/flet-charts)
[![python](https://img.shields.io/badge/python-%3E%3D3.10-%2334D058)](https://pypi.org/project/flet-charts)
[![docstring coverage](https://flet.dev/docs/assets/badges/docs-coverage/flet-charts.svg)](https://flet.dev/docs/assets/badges/docs-coverage/flet-charts.svg)
[![license](https://img.shields.io/badge/License-Apache_2.0-green.svg)](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-charts/LICENSE)

A [Flet](https://flet.dev) extension for creating interactive charts and graphs.

It is based on the [fl_chart](https://pub.dev/packages/fl_chart) Flutter package.

## Documentation

Detailed documentation to this package can be found [here](https://flet.dev/docs/charts/).

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

- [`BarChart`](https://flet.dev/docs/charts/bar_chart/)
- [`CandlestickChart`](https://flet.dev/docs/charts/candlestick_chart/)
- [`LineChart`](https://flet.dev/docs/charts/line_chart/)
- [`MatplotlibChart`](https://flet.dev/docs/charts/matplotlib_chart/)
- [`PieChart`](https://flet.dev/docs/charts/pie_chart/)
- [`PlotlyChart`](https://flet.dev/docs/charts/plotly_chart/)
- [`RadarChart`](https://flet.dev/docs/charts/radar_chart/)
- [`ScatterChart`](https://flet.dev/docs/charts/scatter_chart/)
