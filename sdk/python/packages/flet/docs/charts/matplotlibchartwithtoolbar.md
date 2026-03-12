---
class_name: flet_charts.matplotlib_chart_with_toolbar.MatplotlibChartWithToolbar
examples: ../../examples/controls/charts/matplotlib_chart
example_images: ../test-images-charts/examples/golden/macos/matplotlib_chart
example_media: ../examples/controls/charts/matplotlib_chart/media
---

{{ class_summary(class_name, image_url=example_images + "/toolbar.png", image_width="80%") }}

## Examples

### Basic

Based on an official [Matplotlib example](https://matplotlib.org/stable/gallery/lines_bars_and_markers/cohere.html#sphx-glr-gallery-lines-bars-and-markers-cohere-py).

```python
--8<-- "{{ examples }}/toolbar/main.py"
```

{{ image(example_images + "/toolbar.png", width="80%") }}

### 3D chart

```python
--8<-- "{{ examples }}/three_d/main.py"
```

{{ image(example_images + "/three_d.png", width="80%") }}

### Handle events

```python
--8<-- "{{ examples }}/handle_events/main.py"
```

{{ image(example_images + "/handle_events.png", width="80%") }}

### Animated chart

```python
--8<-- "{{ examples }}/animate/main.py"
```

{{ image(example_media + "/animate.png", width="80%") }}

{{ class_members(class_name) }}
