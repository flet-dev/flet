---
class_name: flet.Column
examples: ../../examples/controls/column
example_images: ../test-images/examples/core/golden/macos/column
example_media: ../examples/controls/column/media
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Basic Column with Text controls") }}

## Examples

### Column `spacing`

```python
--8<-- "{{ examples }}/spacing.py"
```

{{ demo("column/spacing", height="420", width="80%") }}

### Column wrapping

```python
--8<-- "{{ examples }}/wrap.py"
```

{{ demo("column/wrap", height="420", width="80%") }}

### Column vertical alignments

```python
--8<-- "{{ examples }}/alignment.py"
```

{{ demo("column/alignment", height="420", width="80%") }}

### Column horizontal alignments

```python
--8<-- "{{ examples }}/horizontal_alignment.py"
```

{{ demo("column/horizontal_alignment", height="420", width="80%") }}

### Infinite scrolling

This example demonstrates adding of list items on-the-fly, as user scroll to the bottom,
creating the illusion of infinite list:

```python
--8<-- "{{ examples }}/infinite_scrolling.py"
```

{{ demo("column/infinite_scrolling", height="420", width="80%") }}

### Scrolling programmatically

This example shows how to use [`scroll_to()`][flet.Column.scroll_to] to programmatically scroll a column:

```python
--8<-- "{{ examples }}/programmatic_scroll.py"
```

{{ demo("column/programmatic_scroll", height="420", width="80%") }}


[//]: # (### Custom scrollbar)

{{ class_members(class_name) }}
