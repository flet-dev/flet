---
class_name: flet.ProgressRing
examples: ../../examples/controls/progress_ring
example_images: ../test-images/examples/material/golden/macos/progress_ring
example_media: ../examples/controls/progress_ring/media
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Fixed progress ring") }}

## Examples

[Live example](https://flet-controls-gallery.fly.dev/displays/progressring)

### Determinate and indeterminate progress rings

```python
--8<-- "{{ examples }}/determinate_and_indeterminate.py"
```

{{ image(example_media + "/determinate_and_indeterminate.gif", alt="determinate-and-indeterminate", width="80%") }}


### Gauge with progress

```python
--8<-- "{{ examples }}/gauge_with_progress.py"
```

{{ image(example_images + "/gauge_with_progress.png", alt="determinate-and-indeterminate", width="80%") }}

{{ class_members(class_name) }}
