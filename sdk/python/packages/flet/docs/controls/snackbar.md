---
class_name: flet.SnackBar
examples: ../../examples/controls/snack_bar
example_images: ../test-images/examples/material/golden/macos/snack_bar
snack_bar_action_class_name: flet.SnackBarAction
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Opened snack bar") }}

## Examples

### Basic Example

```python
--8<-- "{{ examples }}/basic.py"
```

{{ demo("snackbar/basic", height="420", width="80%") }}

### Counter

```python
--8<-- "{{ examples }}/counter.py"
```

{{ demo("snackbar/counter", height="420", width="80%") }}

### Action

```python
--8<-- "{{ examples }}/action.py"
```

{{ demo("snackbar/action", height="420", width="80%") }}


{{ class_members(class_name) }}

{{ class_all_options(snack_bar_action_class_name) }}
