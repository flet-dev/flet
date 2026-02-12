---
class_name: flet.DataTable
examples: ../../examples/controls/data_table
example_images: ../../test-images/examples/material/golden/macos/datatable
---

# DataTable

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Basic DataTable") }}

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/datatable)

### Basic Example

```python
--8<-- "{{ examples }}/basic.py"
```

{{ image(example_images + "/basic.png", width="80%") }}


### Sortable columns and selectable rows

This example demonstrates row selection (including select-all),
sortable string and numeric columns, and stable selection across sorts and refreshes.

```python
--8<-- "{{ examples }}/sortable_and_selectable.py"
```

{{ image(example_images + "/sortable_and_selectable.png", width="80%") }}


### Handling events

```python
--8<-- "{{ examples }}/handling_events.py"
```

{{ class_members(class_name) }}
