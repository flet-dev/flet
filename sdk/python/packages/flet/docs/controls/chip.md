---
class_name: flet.Chip
examples: ../../examples/controls/chip
example_images: ../test-images/examples/material/golden/macos/chip
example_media: ../examples/controls/chip/media
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Basic Chip") }}

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/chip)

### Assist chips

Assist chips are chips with [`leading`][flet.Chip.leading] icon and [`on_click`][flet.Chip.on_click] event specified.

They represent smart or automated actions that appear dynamically and contextually in a UI.

An alternative to assist chips are [buttons](buttons/index.md), which should appear persistently and consistently.

```python
--8<-- "{{ examples }}/assist_chips.py"
```

{{ image(example_media + "/assist_chips.png", alt="assist-chips", width="80%") }}


### Filter chips

Filter chips are chips with [`on_select`][flet.Chip.on_select] event specified.

They use tags or descriptive words provided in the [`label`][flet.Chip.label] to filter content.
They can be a good alternative to switches or checkboxes.

```python
--8<-- "{{ examples }}/filter_chips.py"
```

{{ image(example_media + "/filter_chips.png", alt="filter-chips", width="80%") }}


{{ class_members(class_name) }}
