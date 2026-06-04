---
class_name: "flet_charts.line_chart.LineChart"
examples: "extensions/charts/line_chart"
example_images: "test-images-charts/examples/golden/macos/line_chart"
diagram: "/docs/assets/controls/charts/line-chart-diagram.svg"
title: "LineChart"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.diagram} imageCaption="Line chart" imageWidth="80%" />

## Examples

<CodeExample path={frontMatter.examples + '/multi_series_line_chart/main.py'} language="python" />

<Image src={frontMatter.example_images + '/example_1.png'} width="65%" />

<CodeExample path={frontMatter.examples + '/line_chart_with_custom_axes/main.py'} language="python" />

<Image src={frontMatter.example_images + '/example_2.png'} width="65%" />

<ClassMembers name={frontMatter.class_name} />
