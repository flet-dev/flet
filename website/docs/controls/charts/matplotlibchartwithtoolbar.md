---
class_name: "flet_charts.matplotlib_chart_with_toolbar.MatplotlibChartWithToolbar"
examples: "controls/core/charts/matplotlib_chart"
example_images: "test-images-charts/examples/golden/macos/matplotlib_chart"
example_media: "examples/controls/core/charts/matplotlib_chart/media"
title: "MatplotlibChartWithToolbar"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/toolbar.png'} imageWidth="65%" />

## Examples

### Basic

Based on an official [Matplotlib example](https://matplotlib.org/stable/gallery/lines_bars_and_markers/cohere.html#sphx-glr-gallery-lines-bars-and-markers-cohere-py).

<CodeExample path={frontMatter.examples + '/toolbar/main.py'} language="python" />

<Image src={frontMatter.example_images + '/toolbar.png'} width="65%" />

### 3D chart

<CodeExample path={frontMatter.examples + '/three_d/main.py'} language="python" />

<Image src={frontMatter.example_images + '/three_d.png'} width="65%" />

### Handle events

<CodeExample path={frontMatter.examples + '/handle_events/main.py'} language="python" />

<Image src={frontMatter.example_images + '/handle_events.png'} width="65%" />

### Animated chart

<CodeExample path={frontMatter.examples + '/animate/main.py'} language="python" />

<Image src={frontMatter.example_media + '/animate.png'} width="55%" />

<ClassMembers name={frontMatter.class_name} />
