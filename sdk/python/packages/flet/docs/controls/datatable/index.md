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
--8<-- "{{ examples }}/basic/main.py"
```

{{ image(example_images + "/basic.png", width="80%") }}


### Horizontal margin and column spacing

Use [`horizontal_margin`][flet.DataTable.horizontal_margin] to control the left and right
edge spacing of the first and last columns.
Use [`column_spacing`][flet.DataTable.column_spacing] to control spacing between columns.

```python
--8<-- "{{ examples }}/spacing/main.py"
```

### Adaptive row heights

Setting [`data_row_max_height`][flet.DataTable.data_row_max_height] to `float('inf')`
(infinity) will cause the `DataTable` to let each individual row adapt its height to its
respective content, instead of all rows having the same height.

```python
--8<-- "{{ examples }}/adaptive_row_heights/main.py"
```

### Sortable columns and selectable rows

This example demonstrates row selection (including select-all),
sortable string and numeric columns, and stable selection across sorts and refreshes.

```python
--8<-- "{{ examples }}/sortable_and_selectable/main.py"
```

{{ image(example_images + "/sortable_and_selectable.png", width="80%") }}


### Handling events

```python
--8<-- "{{ examples }}/handling_events/main.py"
```

{{ class_members(class_name) }}
