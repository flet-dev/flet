::: flet.WebRenderer
    options:
        separate_signature: false


## Usage Example

You can explicitly set what renderer to use when running a Flet program
in web mode using the `web_renderer` parameter of the `ft.run`.

```python
import flet as ft

def main(page: ft.Page):
    ...

ft.run(main, view=ft.AppView.WEB_BROWSER, web_renderer=ft.WebRenderer.CANVAS_KIT)
```
