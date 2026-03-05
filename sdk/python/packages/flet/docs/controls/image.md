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

### Fade-in images with a placeholder

```python
--8<-- "{{ examples }}/fade_in.py"
```

### Displaying images from base64 strings and byte data

```python
--8<-- "{{ examples }}/src_base64_and_bytes.py"
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

### Gapless playback when changing image sources

This example updates both images to a new network URL on each click. With
[`gapless_playback`][flet.Image.gapless_playback] set to `True`, the previous frame remains visible while the next
image loads. With [`gapless_playback`][flet.Image.gapless_playback] set to `False`, the image area can
briefly be empty, causing a flicker/blink effect.

```python
--8<-- "{{ examples }}/gapless_playback.py"
```

{{ class_members(class_name) }}
