---
slug: matplotlib-and-plotly-charts
title: Matplotlib and Plotly charts
authors: feodor
tags: [release]
---

We are thrilled to introduce Matplotlib and Plotly charting controls in [Flet 0.1.63](https://pypi.org/project/flet/0.1.63/)!

[Matplotlib](https://matplotlib.org/) and [Plotly](https://plotly.com/python/) are the most recognized Python charting libraries with a ton of features. They are greatly compatible with other scientific Python libraries such as Numpy or Pandas.

No doubt, it would be nearly impossible to replicate their functionality as pure Flutter widgets. Fortunately, both Matplotlib and Plotly can export charts into various formats, such as SVG. On the other hand Flet can [display SVG images](https://github.com/flet-dev/examples/blob/main/python/controls/image/svg-image.py) and that gives a perfect combination - Flet charting controls for Matplotlib and Plotly!

The resulting solution works so great that it's possible to display almost any example from [Matplotlib](https://matplotlib.org/stable/gallery/index.html) and [Plotly](https://plotly.com/python/) galleries - your imagination is the only limit!

Plot a [simple bar chart](https://github.com/flet-dev/examples/blob/main/python/controls/charts/mpl-barchart.py):

<img src="/img/docs/controls/charts/matplotlib-barchart.png" className="screenshot-60"/>

a nice [scatter with legend](https://github.com/flet-dev/examples/blob/main/python/controls/charts/mpl-scatter.py):

<img src="/img/docs/controls/charts/matplotlib-scatter.png" className="screenshot-60"/>

or some multi-chart [contour plot](https://github.com/flet-dev/examples/blob/main/python/controls/charts/mpl-contour.py):

<img src="/img/docs/controls/charts/matplotlib-contour.png" className="screenshot-60"/>

Check the docs for Matplotlib and Plotly charting controls:

* [MatplotlibChart](https://docs.flet.dev/charts/matplotlib_chart/)
* [PlotlyChart](https://docs.flet.dev/charts/plotly_chart/)

Explore [Flet chart examples](https://github.com/flet-dev/examples/tree/main/python/controls/charts).

<!-- truncate -->

Learn Python libraries by examples:

* [Matplotlib gallery](https://matplotlib.org/stable/gallery/index.html)
* [Plotly gallery](https://plotly.com/python/)

In the future releases, we may add an interactive "toolbar" for Matplotlib charts by implementing a custom [backend](https://matplotlib.org/stable/users/explain/backends.html). Or maybe it's a great exercise for Flet users? 😉

Also, when it's time for Flet to support other languages we would need to re-visit charting to make it language-agnostic as the current charting implementation relies on Python libraries.

Upgrade Flet module to the latest version (`pip install flet --upgrade`), integrate auth in your app and [let us know](https://discord.gg/dzWXP8SHG8) what you think!

Enjoy!