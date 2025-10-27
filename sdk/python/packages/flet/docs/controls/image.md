---
class_name: flet.Image
examples: ../../examples/controls/image
example_images: ../test-images/examples/core/golden/macos/image
example_media: ../examples/controls/image/media
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Basic Image") }}

## Examples

[Live example](https://flet-controls-gallery.fly.dev/displays/image)

### Image gallery

```python
--8<-- "{{ examples }}/gallery.py"
```

{{ image(example_media + "/gallery.gif", width="80%") }}

### Displaying a base64 image

```python
--8<-- "{{ examples }}/base64.py"
```

### Displaying a static SVG image

```python
--8<-- "{{ examples }}/static_svg.py"
```

### Displaying a dynamic SVG image

```python
--8<-- "{{ examples }}/dynamic_svg.py"
```

### Displaying a Lucide icon

```python
--8<-- "{{ examples }}/lucide_icons.py"
```

{{ class_members(class_name) }}
