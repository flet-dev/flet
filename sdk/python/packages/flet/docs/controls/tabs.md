::: flet.Tabs
::: flet.Tab

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/tabs)

### Tabs

<img src="/img/docs/controls/tabs/tabs-simple.gif" className="screenshot-60"/>



```python
import flet as ft

def main(page: ft.Page):

    t = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Tab 1",
                content=ft.Container(
                    content=ft.Text("This is Tab 1"), alignment=ft.alignment.center
                ),
            ),
            ft.Tab(
                tab_content=ft.Icon(ft.Icons.SEARCH),
                content=ft.Text("This is Tab 2"),
            ),
            ft.Tab(
                text="Tab 3",
                icon=ft.Icons.SETTINGS,
                content=ft.Text("This is Tab 3"),
            ),
        ],
        expand=1,
    )

    page.add(t)

ft.run(main)
```
