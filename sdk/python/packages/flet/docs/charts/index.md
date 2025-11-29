# Charts

Interactive chart controls powered by [flet-charts](https://pypi.org/project/flet-charts/) let you display data as bar, line, pie, scatter and plotly visualisations directly in your Flet apps.

It is built on top of the [fl_chart](https://pub.dev/packages/fl_chart) Flutter package and ships with helper classes for axis labels, tooltips and more.

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ✅       | ✅     | ✅     | ✅   | ✅       | ✅   |

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

/// admonition | Extra Dependencies
    type: tip
Some chart controls require additional dependencies to be installed:

* [`MatplotlibChart`][flet_charts.MatplotlibChart]: [`matplotlib`](https://matplotlib.org/)
* [`PlotlyChart`][flet_charts.PlotlyChart]: [`plotly`](https://plotly.com/python/) **and** [`kaleido`](https://github.com/plotly/Kaleido)

`flet-charts` provides extras to easily install these:

/// tab | uv
```bash
uv add "flet-charts[all]"   # (1)!
# or
uv add "flet-charts[plotly]"   # (2)!
# or
uv add "flet-charts[matplotlib]"   # (3)!
```

1. Additionally installs `matplotlib`, `plotly` and `kaleido`.
2. Additionally installs `plotly` and `kaleido`.
3. Additionally installs `matplotlib`.
///
/// tab | pip
```bash
pip install "flet-charts[all]"   # (1)!
# or
pip install "flet-charts[plotly]"   # (2)!
# or
pip install "flet-charts[matplotlib]"   # (3)!
```

 1. Additionally installs `matplotlib`, `plotly` and `kaleido`.
 2. Additionally installs `plotly` and `kaleido`.
 3. Additionally installs `matplotlib`.
///

///


## Available Charts

- [`BarChart`](bar_chart.md)
- [`CandlestickChart`](candlestick_chart.md)
- [`LineChart`](line_chart.md)
- [`MatplotlibChart`](matplotlib_chart.md)
- [`PieChart`](pie_chart.md)
- [`PlotlyChart`](plotly_chart.md)
- [`RadarChart`](radar_chart.md)
- [`ScatterChart`](scatter_chart.md)
