::: flet.WebRenderer


## Usage Example

You can explicitly set what renderer to use when running a Flet program in web mode using the `web_renderer` parameter of the `ft.app`.

```python
import flet as ft

def main(page: ft.Page):
    ...

ft.app(main, view=ft.AppView.WEB_BROWSER, web_renderer=ft.WebRenderer.HTML)
```
    options:
        separate_signature: false
