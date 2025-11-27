---
class_name: flet.Image
examples: ../../examples/controls/image
example_images: ../test-images/examples/core/golden/macos/image
example_media: ../examples/controls/image/media
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Basic Image") }}

## Examples

### Image gallery

```python
--8<-- "{{ examples }}/gallery.py"
```

{{ demo("image/gallery", height="420", width="80%") }}

### Displaying images from base64 strings and byte data

```python
--8<-- "{{ examples }}/src_base64_and_bytes.py"
```

{{ demo("image/src_base64_and_bytes", height="420", width="80%") }}

### Displaying a static SVG image

```python
--8<-- "{{ examples }}/static_svg.py"
```

{{ demo("image/static_svg", height="420", width="80%") }}

### Displaying a dynamic SVG image

```python
--8<-- "{{ examples }}/dynamic_svg.py"
```

{{ demo("image/dynamic_svg", height="420", width="80%") }}

### Displaying a Lucide icon

```python
--8<-- "{{ examples }}/lucide_icons.py"
```

{{ demo("image/lucide_icons", height="420", width="80%") }}


{{ class_members(class_name) }}
