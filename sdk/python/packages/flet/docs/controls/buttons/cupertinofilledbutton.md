::: flet.CupertinoFilledButton

## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/cupertinofilledbutton)

### Basic Example



```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.CupertinoFilledButton(
            content=ft.Text("CupertinoFilled"),
            opacity_on_click=0.3,
            on_click=lambda e: print("CupertinoFilledButton clicked!"),
        ),
    )

ft.run(main)
```

<img src="/img/docs/controls/cupertino-filled-button/cupertino-filled-button.png" className="screenshot-20" />
