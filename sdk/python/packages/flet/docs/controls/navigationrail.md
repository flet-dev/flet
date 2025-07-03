::: flet.NavigationRail

## Examples

[Live example](https://flet-controls-gallery.fly.dev/navigation/navigationrail)



```python
import flet as ft

def main(page: ft.Page):

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        # extended=True,
        min_width=100,
        min_extended_width=400,
        leading=ft.FloatingActionButton(icon=ft.Icons.CREATE, text="Add"),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.FAVORITE_BORDER, selected_icon=ft.Icons.FAVORITE, label="First"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.BOOKMARK_BORDER),
                selected_icon=ft.Icon(ft.Icons.BOOKMARK),
                label="Second",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icon(ft.Icons.SETTINGS),
                label_content=ft.Text("Settings"),
            ),
        ],
        on_change=lambda e: print("Selected destination:", e.control.selected_index),
    )

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                ft.Column([ ft.Text("Body!")], alignment=ft.MainAxisAlignment.START, expand=True),
            ],
            expand=True,
        )
    )

ft.run(main)
```


<img src="/img/docs/controls/navigation-rail/custom-navrail.png" className="screenshot-50" />
