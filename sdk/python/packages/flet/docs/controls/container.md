---
class_name: flet.Container
examples: ../../examples/controls/container
example_images: ../examples/controls/container/media
golden_example_images: ../test-images/examples/material/golden/macos/container
---

{{ class_summary(class_name) }}

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/container)

### Clickable container

```python
--8<-- "{{ examples }}/clickable.py"
```

{{ image(example_images + "/clickable.gif", width="80%") }}

### Handling clicks

```python
--8<-- "{{ examples }}/handling_clicks.py"
```

{{ image(example_images + "/handling_clicks.gif", width="80%") }}


### Handling hovers

```python
--8<-- "{{ examples }}/handling_hovers.py"
```

{{ image(example_images + "/handling_hovers.gif", width="80%") }}


### Animate 1

```python
--8<-- "{{ examples }}/animate_1.py"
```

{{ image(example_images + "/animate_1.gif", width="80%") }}


### Animate 2

```python
--8<-- "{{ examples }}/animate_2.py"
```

### Animate 3

```python
--8<-- "{{ examples }}/animate_3.py"
```

### Animate 4

```python
--8<-- "{{ examples }}/animate_4.py"
```

### Nested themes 1

```python
--8<-- "{{ examples }}/nested_themes_1.py"
```

{{ image(golden_example_images + "/nested_themes_1.png", width="80%") }}

### Nested themes 2

```python
--8<-- "{{ examples }}/nested_themes_2.py"
```

{{ image(golden_example_images + "/nested_themes_2.png", width="80%") }}

### Nested themes 3

```python
--8<-- "{{ examples }}/nested_themes_3.py"
```

{{ image(example_images + "/nested_themes_3.gif", width="80%") }}


### Size aware

```python
--8<-- "{{ examples }}/size_aware.py"
```

{{ image(golden_example_images + "/size_aware.png", width="80%") }}

{{ class_members(class_name) }}
