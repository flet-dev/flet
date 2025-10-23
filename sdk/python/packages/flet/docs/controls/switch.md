---
class_name: flet.Switch
examples: ../../examples/controls/switch
example_images: ../test-images/examples/material/golden/macos/switch
example_media: ../../examples/controls/switch/media
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Basic switch and disabled switch") }}

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/switch)

### Basic Example

```python
--8<-- "{{ examples }}/basic.py"
```

{{ image(example_images + "/basic.png", alt="basic", width="80%") }}


### Handling change events

```python
--8<-- "{{ examples }}/handling_events.py"
```

{{ image(example_media + "/handling_events.gif", alt="handling-events", width="80%") }}


{{ class_members(class_name) }}
