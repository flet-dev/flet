---
class_name: flet.DropdownM2
examples: ../../examples/controls/dropdown_m2
example_images: ../test-images/examples/material/golden/macos/dropdown_m2
example_media: ../examples/controls/dropdown_m2/media
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Basic DropdownM2") }}

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/dropdown)

### Basic Example

```python
--8<-- "{{ examples }}/basic.py"
```

{{ image(example_media + "/basic.gif", alt="basic", width="80%") }}


### Dropdown with label and hint

```python
--8<-- "{{ examples }}/label_and_hint.py"
```

{{ image(example_media + "/label_and_hint.gif", alt="label-and-hint", width="80%") }}


### Handling events

```python
--8<-- "{{ examples }}/handling_events.py"
```

{{ image(example_media + "/handling_events.gif", alt="handling-events", width="80%") }}



### Add and delete options

```python
--8<-- "{{ examples }}/add_and_delete_options.py"
```

{{ image(example_media + "/add_and_delete_options.gif", alt="add-and-delete-options", width="80%") }}


{{ class_members(class_name) }}
