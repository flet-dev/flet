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

![spacing]({{ example_images }}/spacing.gif){width="80%"}
/// caption
///

### Column wrapping

```python
--8<-- "{{ examples }}/wrap.py"
```

![wrap]({{ example_images }}/wrap.gif){width="80%"}
/// caption
///

### Column vertical alignments

```python
--8<-- "{{ examples }}/alignment.py"
```

![alignment]({{ example_images }}/alignment.png){width="80%"}
/// caption
///

### Column horizontal alignments

```python
--8<-- "{{ examples }}/horizontal_alignment.py"
```

![horizontal-alignment]({{ example_images }}/horizontal_alignment.png){width="80%"}
/// caption
///

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

![programmatic-scroll]({{ example_images }}/programmatic_scroll.png){width="80%"}
/// caption
///

[//]: # (### Custom scrollbar)

{{ class_members(class_name) }}
