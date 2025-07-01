::: flet.FilledTonalButton

## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/filledtonalbutton)

### Filled tonal button



```python
import flet as ft


def main(page: ft.Page):
    page.title = "Basic filled tonal buttons"
    page.add(
        ft.FilledTonalButton(text="Filled tonal button"),
        ft.FilledTonalButton("Disabled button", disabled=True),
        ft.FilledTonalButton("Button with icon", icon="add"),
    )

ft.run(main)
```
