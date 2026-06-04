---
class_name: "flet_charts.pie_chart.PieChart"
examples: "extensions/charts/pie_chart"
example_images: "test-images-charts/examples/golden/macos/pie_chart"
diagram: "/docs/assets/controls/charts/pie-chart-diagram.svg"
title: "PieChart"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.diagram} imageWidth="50%" />

## Examples

<CodeExample path={frontMatter.examples + '/pie_chart_with_hover_borders/main.py'} language="python" />

<Image src={frontMatter.example_images + '/example_1.png'} width="65%" />

<CodeExample path={frontMatter.examples + '/pie_chart_with_hover_sections/main.py'} language="python" />

<Image src={frontMatter.example_images + '/example_2.png'} width="65%" />

<CodeExample path={frontMatter.examples + '/pie_chart_with_icon_badges/main.py'} language="python" />

<Image src={frontMatter.example_images + '/example_3.png'} width="65%" />

<ClassMembers name={frontMatter.class_name} />
