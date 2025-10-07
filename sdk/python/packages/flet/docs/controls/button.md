---
class_name: flet.Button
examples: ../../examples/controls/button
example_images: ../test-images/examples/material/golden/macos/button
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Enabled and disabled buttons") }}

## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/elevatedbutton)

### Button

```python
--8<-- "{{ examples }}/basic.py"
```

{{ image(example_images + "/basic.png", alt="Basic button", width="50%") }}


### Icons

```python
--8<-- "{{ examples }}/icons.py"
```

{{ image(example_images + "/icons.png", alt="Basic button", width="50%") }}


### Handling clicks

```python
--8<-- "{{ examples }}/handling_clicks.py"
```

{{ image(example_images + "/handling_clicks.png", alt="Handling clicks", width="50%") }}


### Custom content

```python
--8<-- "{{ examples }}/custom_content.py"
```

{{ image(example_images + "/custom_content.png", alt="Buttons with custom content", width="50%") }}


### Shapes

```python
--8<-- "{{ examples }}/button_shapes.py"
```

{{ image(example_images + "/button_shapes.png", alt="Buttons with different shapes", width="50%") }}


### Styling

```python
--8<-- "{{ examples }}/styling.py"
```

{{ image(example_images + "/styled_initial.png", alt="Styled button - default state", width="50%", caption="Default state") }}


{{ image(example_images + "/styled_hovered.png", alt="Styled button - hovered state", width="50%", caption="Hovered state") }}


### Animate on hover

```python
--8<-- "{{ examples }}/animate_on_hover.py"
```

{{ image(example_images + "/animate_on_hover_initial.png", alt="Unhovered button", width="50%", caption="Normal button") }}


{{ image(example_images + "/animate_on_hover_hovered.png", alt="Hovered button", width="50%", caption="Hovered button") }}


{{ class_members(class_name) }}
