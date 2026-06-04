---
class_name: "flet_charts.plotly_chart.PlotlyChart"
examples: "extensions/charts/plotly_chart"
example_images: "test-images-charts/examples/golden/macos/plotly_chart"
title: "PlotlyChart"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Bar chart based on official [Plotly example](https://plotly.com/python/bar-charts)" imageWidth="65%" />

## Examples

<CodeExample path={frontMatter.examples + '/plotly_line_chart/main.py'} language="python" />

<Image src={frontMatter.example_images + '/example_1.png'} width="65%" />

<CodeExample path={frontMatter.examples + '/plotly_bar_chart/main.py'} language="python" />

<Image src={frontMatter.example_images + '/example_2.png'} width="65%" />

<CodeExample path={frontMatter.examples + '/plotly_pie_chart/main.py'} language="python" />

<Image src={frontMatter.example_images + '/example_3.png'} width="65%" />

<CodeExample path={frontMatter.examples + '/plotly_box_plot/main.py'} language="python" />

<Image src={frontMatter.example_images + '/example_4.png'} width="65%" />

<ClassMembers name={frontMatter.class_name} />
