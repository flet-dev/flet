---
class_name: flet.Row
examples: ../../examples/controls/row
example_images: ../test-images/examples/core/golden/macos/row
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Basic row of controls") }}

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/row)

### Spacing children

```python
--8<-- "{{ examples }}/spacing.py"
```

{{ image(example_images + "/row_spacing_adjustment.gif", alt="spacing", width="80%") }}


### Wrapping children

```python
--8<-- "{{ examples }}/wrap.py"
```

{{ image(example_images + "/wrap_adjustment.gif", alt="wrap", width="80%") }}


### Setting horizontal alignment

```python
--8<-- "{{ examples }}/alignment.py"
```

{{ image(example_images + "/alignment.png", alt="alignment", width="60%") }}


### Setting vertical alignment

```python
--8<-- "{{ examples }}/vertical_alignment.py"
```

{{ image(example_images + "/vertical_alignment.png", alt="vertical-alignment", width="60%") }}


{{ class_members(class_name) }}
