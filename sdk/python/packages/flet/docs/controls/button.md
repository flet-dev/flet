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

![Basic button]({{ example_images }}/basic.png){width="50%"}
/// caption
///

### Icons

```python
--8<-- "{{ examples }}/icons.py"
```

![Basic button]({{ example_images }}/icons.png){width="50%"}
/// caption
///

### Handling clicks

```python
--8<-- "{{ examples }}/handling_clicks.py"
```

![Handling clicks]({{ example_images }}/handling_clicks.png){width="50%"}
/// caption
///

### Custom content

```python
--8<-- "{{ examples }}/custom_content.py"
```

![Buttons with custom content]({{ example_images }}/custom_content.png){width="50%"}
/// caption
///

### Shapes

```python
--8<-- "{{ examples }}/button_shapes.py"
```

![Buttons with different shapes]({{ example_images }}/button_shapes.png){width="50%"}
/// caption
///

### Styling

```python
--8<-- "{{ examples }}/styling.py"
```

![Styled button - default state]({{ example_images }}/styled_initial.png){width="50%"}
/// caption
Default state
///

![Styled button - hovered state]({{ example_images }}/styled_hovered.png){width="50%"}
/// caption
Hovered state
///

### Animate on hover

```python
--8<-- "{{ examples }}/animate_on_hover.py"
```

![Unhovered button]({{ example_images }}/animate_on_hover_initial.png){width="50%"}
/// caption
Normal button
///

![Hovered button]({{ example_images }}/animate_on_hover_hovered.png){width="50%"}
/// caption
Hovered button
///

{{ class_members(class_name) }}
