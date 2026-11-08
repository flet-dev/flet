---
class_name: "flet_charts.gauge_chart.GaugeChart"
examples: "extensions/charts/gauge_chart"
example_images: "test-images-charts/examples/golden/macos/gauge_chart"
title: "GaugeChart"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Gauge chart" imageWidth="45%" />

## Examples

<CodeExample path={frontMatter.examples + '/speedometer/main.py'} language="python" />

<Image src={frontMatter.example_images + '/speedometer.png'} width="45%" />

<CodeExample path={frontMatter.examples + '/activity_rings/main.py'} language="python" />

<Image src={frontMatter.example_images + '/activity_rings.png'} width="45%" />

<ClassMembers name={frontMatter.class_name} />
