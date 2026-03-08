---
class_name: flet.ExpansionPanelList
examples: ../../examples/controls/expansion_panel_list
example_images: ../test-images/examples/material/golden/macos/expansion_panel_list
example_media: ../examples/controls/expansion_panel_list/media
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Basic ExpansionPanelList") }}

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/expansionpanellist)

### Basic Example

```python
--8<-- "{{ examples }}/basic.py"
```

{{ image(example_media + "/basic.gif", alt="basic", width="80%") }}

### Scrollable list with many panels

`ExpansionPanelList` supports scrolling. For long lists, enable [`scroll`][flet.].
If you want it to fill available space, also set [`expand`][flet.Control.expand].

```python
--8<-- "{{ examples }}/scrollable.py"
```

### Change event with expanded state

[`on_change`][flet.ExpansionPanelList.on_change] includes both panel index and
resulting expanded/collapsed state.


{{ class_members(class_name) }}
