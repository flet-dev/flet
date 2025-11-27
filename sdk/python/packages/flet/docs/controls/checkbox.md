---
class_name: flet.Checkbox
examples: ../../examples/controls/checkbox
example_images: ../test-images/examples/material/golden/macos/checkbox
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Basic checkboxes") }}

## Examples

### Basic Example

```python
--8<-- "{{ examples }}/basic.py"
```

{{ image(example_images + "/basic.png", alt="basic", width="50%", caption="After clicking Submit") }}

{{ iframe(route="checkbox/basic", height="400") }}

### Handling events

```python
--8<-- "{{ examples }}/handling_events.py"
```

{{ image(example_images + "/handling_events.png", alt="handling-events", width="50%", caption="After three clicks") }}

{{ iframe(route="checkbox/handling_events", height="520") }}

### Styled checkboxes

```python
--8<-- "{{ examples }}/styled.py"
```

{{ image(example_images + "/styled_checkboxes.png", alt="Styled checkboxes", width="50%") }}

{{ iframe(route="checkbox/styled", height="520") }}

{{ class_members(class_name) }}
