---
examples: ../../examples/controls/charts
---

# Charts

Interactive chart controls powered by [flet-charts](https://pypi.org/project/flet-charts/) let you display data as bar, line, pie, scatter and plotly visualisations directly in your Flet apps.

It is built on top of the [fl_chart](https://pub.dev/packages/fl_chart) Flutter package and ships with helper classes for axis labels, tooltips and more.

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅   |  ✅  |    ✅    |  ✅  |

## Usage

Add `flet-charts` to your project dependencies:

/// tab | uv
```bash
uv add flet-charts
```

///
/// tab | pip
```bash
pip install flet-charts  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
///

## Available Charts

- [`BarChart`](barchart.md)
- [`CandlestickChart`](candlestickchart.md)
- [`LineChart`](linechart.md)
- [`MatplotlibChart`](matplotlibchart.md)
- [`PieChart`](piechart.md)
- [`PlotlyChart`](plotlychart.md)
- [`RadarChart`](radarchart.md)
- [`ScatterChart`](scatterchart.md)
