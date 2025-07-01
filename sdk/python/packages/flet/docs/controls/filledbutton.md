::: flet.FilledButton

## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/filledbutton)

### Filled button



```python
import flet as ft


def main(page: ft.Page):
    page.title = "Basic filled buttons"
    page.add(
        ft.FilledButton(text="Filled button"),
        ft.FilledButton("Disabled button", disabled=True),
        ft.FilledButton("Button with icon", icon="add"),
    )

ft.run(main)
```

