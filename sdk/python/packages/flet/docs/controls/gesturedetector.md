---
class_name: flet.GestureDetector
examples: ../../examples/controls/gesture_detector
example_images: ../examples/controls/gesture_detector/media
---

{{ class_summary(class_name) }}

## Examples

[Solitaire game tutorial](https://flet.dev/docs/tutorials/python-solitaire)

### Handling events

```python
--8<-- "{{ examples }}/handling_events.py"
```

{{ demo("gesturedetector/handling_events", height="420", width="80%") }}

### Draggable containers

The following example demonstrates how a control can be freely dragged inside a Stack.

The sample also shows that GestureDetector can have a child control (blue container) as well as be nested
inside another control (yellow container) giving the same results.

```python
--8<-- "{{ examples }}/draggable_containers.py"
```

{{ demo("gesturedetector/draggable_containers", height="420", width="80%") }}

### Window drag area

```python
--8<-- "{{ examples }}/window_drag_area.py"
```

{{ demo("gesturedetector/window_drag_area", height="420", width="80%") }}

### Mouse Cursors

```python
--8<-- "{{ examples }}/mouse_cursors.py"
```

{{ demo("gesturedetector/mouse_cursors", height="420", width="80%") }}


{{ class_members(class_name) }}
