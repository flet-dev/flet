---
class_name: flet.SnackBar
examples: ../../examples/controls/snack_bar
example_images: ../test-images/examples/material/golden/macos/snack_bar
snack_bar_action_class_name: flet.SnackBarAction
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Opened snack bar") }}

## Examples

[Live example](https://flet-controls-gallery.fly.dev/dialogs/snackbar)

### Basic Example

```python
--8<-- "{{ examples }}/basic.py"
```

{{ image(example_images + "/basic.png", alt="basic", width="80%") }}


### Counter

```python
--8<-- "{{ examples }}/counter.py"
```
{{ image(example_images + "/snack_bar_flow.gif", alt="Snack bar with counter", caption="Snack bar with counter",width="50%") }}


{{ class_members(class_name) }}

{{ class_all_options(snack_bar_action_class_name) }}
