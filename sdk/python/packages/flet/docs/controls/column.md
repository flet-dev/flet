---
class_name: flet.Column
examples: ../../examples/controls/column
example_images: ../examples/controls/column/media
---

{{ class_summary(class_name) }}

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/column)

### Column `spacing`

```python
--8<-- "{{ examples }}/spacing.py"
```

{{ image(example_images + "/spacing.gif", alt="spacing", width="80%") }}


### Column wrapping

```python
--8<-- "{{ examples }}/wrap.py"
```

{{ image(example_images + "/wrap.gif", alt="wrap", width="80%") }}


### Column vertical alignments

```python
--8<-- "{{ examples }}/alignment.py"
```

{{ image(example_images + "/alignment.png", alt="alignment", width="80%") }}


### Column horizontal alignments

```python
--8<-- "{{ examples }}/horizontal_alignment.py"
```

{{ image(example_images + "/horizontal_alignment.png", alt="horizontal-alignment", width="80%") }}


### Infinite scrolling

This example demonstrates adding of list items on-the-fly, as user scroll to the bottom,
creating the illusion of infinite list:

```python
--8<-- "{{ examples }}/infinite_scrolling.py"
```

### Scrolling programmatically

This example shows how to use [`scroll_to()`][flet.Column.scroll_to] to programmatically scroll a column:

```python
--8<-- "{{ examples }}/programmatic_scroll.py"
```

{{ image(example_images + "/programmatic_scroll.png", alt="programmatic-scroll", width="80%") }}


[//]: # (### Custom scrollbar)

{{ class_members(class_name) }}
