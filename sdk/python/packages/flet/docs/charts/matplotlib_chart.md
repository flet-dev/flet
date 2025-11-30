---
class_name: flet_charts.matplotlib_chart.MatplotlibChart
examples: ../../examples/controls/charts/matplotlib_chart
example_images: ../examples/controls/charts/matplotlib_chart/media
---

{{ class_summary(class_name, image_url=example_images + "/toolbar.png", image_width="80%") }}

## Examples

### Bar chart

Based on an official [Matplotlib example](https://matplotlib.org/stable/gallery/lines_bars_and_markers/bar_colors.html#sphx-glr-gallery-lines-bars-and-markers-bar-colors-py).

```python
--8<-- "{{ examples }}/bar_chart.py"
```

{{ image(example_images + "/bar_chart.png", width="80%") }}

### Chart with Toolbar

Based on an official [Matplotlib example](https://matplotlib.org/stable/gallery/lines_bars_and_markers/cohere.html#sphx-glr-gallery-lines-bars-and-markers-cohere-py).

```python
--8<-- "{{ examples }}/toolbar.py"
```

{{ image(example_images + "/toolbar.png", width="80%") }}

### 3D chart

```python
--8<-- "{{ examples }}/3d.py"
```

{{ image(example_images + "/3d.png", width="80%") }}

### Handle events

```python
--8<-- "{{ examples }}/handle_events.py"
```

{{ image(example_images + "/handle_events.png", width="80%") }}

### Animated chart

{{ code_and_demo(examples + "/animate.py", demo_height="420", demo_width="100%") }}


{{ class_members(class_name) }}
