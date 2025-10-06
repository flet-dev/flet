---
class_name: flet.GestureDetector
examples: ../../examples/controls/gesture_detector
example_images: ../examples/controls/gesture_detector/media
---

{{ class_summary(class_name) }}

## Examples

[Live example](https://flet-controls-gallery.fly.dev/utility/gesturedetector)

[Solitare game tutorial](https://flet.dev/docs/tutorials/python-solitaire)

### Handling events

```python
--8<-- "{{ examples }}/handling_events.py"
```

### Draggable containers

The following example demonstrates how a control can be freely dragged inside a Stack.

The sample also shows that GestureDetector can have a child control (blue container) as well as be nested
inside another control (yellow container) giving the same results.

```python
--8<-- "{{ examples }}/draggable_containers.py"
```

{{ image(example_images + "/draggable_containers.gif", alt="draggable-containers", width="80%") }}


### Window drag area

```python
--8<-- "{{ examples }}/window_drag_area.py"
```

### Mouse Cursors

```python
--8<-- "{{ examples }}/mouse_cursors.py"
```

{{ class_members(class_name) }}
