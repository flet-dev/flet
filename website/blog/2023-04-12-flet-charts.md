---
slug: flet-charts
title: Flet Charts
authors: feodor
tags: [releases]
---

Last year we introduced support for [Matplotlib and Plotly charts](/blog/matplotlib-and-plotly-charts). Both libraries are able to export charts as SVG images which are then displayed in a Flet app. However, such charts, while serving the purpose of visualization, are lacking interactivity and animation.

Today we are releasing [Flet 0.5.2](https://pypi.org/project/flet/) with built-in charts 📊 based on the awesome [fl_chart](https://pub.dev/packages/fl_chart) library!

<!-- truncate -->

Three new chart controls have been introduced:

## LineChart

<img src="/img/docs/controls/charts/linechart-sample-1.gif" className="screenshot-50"/>

[Docs](https://docs.flet.dev/charts/line_chart/) · [Examples](https://github.com/flet-dev/examples/tree/main/python/controls/charts)

## BarChart

<img src="/img/docs/controls/charts/barchart-sample-2.gif" className="screenshot-50"/>

[Docs](https://docs.flet.dev/charts/bar_chart/) · [Examples](https://github.com/flet-dev/examples/tree/main/python/controls/charts)

## PieChart

<img src="/img/docs/controls/charts/piechart-sample-2.gif" className="screenshot-30"/>

[Docs](https://docs.flet.dev/charts/pie_chart/) · [Examples](https://github.com/flet-dev/examples/tree/main/python/controls/charts)

:::note
We spent a lot of time studying `fl_chart` library while trying to implement most of its features in a Flet way. However, if you see anything missing in Flet, but available in a library please [submit a new feature request](https://github.com/flet-dev/flet/issues).
:::

## Other changes

### Pyodide 0.23

Pyodide, which provides Python runtime in a browser and is used to run Flet app as a static website, was upgraded to version 0.23 which is based on Python 3.11.2 and giving some [size and performance improvements](https://blog.pyodide.org/posts/0.23-release/).

### Memory leak fixes

In this release we paid a lot of attention to memory leak issues in Flet apps. Now, when a user session is closed its memory is reliably released and garbage-collected. That makes Flet ready for production applications with a lot of users.

Upgrade Flet module to the latest version (`pip install flet --upgrade`), give charts a try and [let us know](https://discord.gg/dzWXP8SHG8) what you think!

Hey, [Flet project](https://github.com/flet-dev/flet) has reached ⭐️ 5K stars ⭐️ - thank you all for your continuing support!

