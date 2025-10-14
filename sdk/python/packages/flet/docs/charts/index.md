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

> [!TIP]
> All chart services are regular controls—simply instantiate them and add to the page or to a layout container.

## Available Charts

- [`BarChart`](bar_chart.md)
- [`CandlestickChart`](candlestick_chart.md)
- [`LineChart`](line_chart.md)
- [`MatplotlibChart`](matplotlib_chart.md)
- [`PieChart`](pie_chart.md)
- [`PlotlyChart`](plotly_chart.md)
- [`ScatterChart`](scatter_chart.md)

Each chart page provides ready-to-run examples from `{{ examples }}`.
