::: flet.Dropdown

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/dropdown)

### Dropdown with colors

```python
import flet as ft

def main(page: ft.Page):
    colors = [
        ft.Colors.RED,
        ft.colors.BLUE,
        ft.Colors.YELLOW,
        ft.Colors.PURPLE,
        ft.Colors.LIME,
    ]

    def get_options():
        options = []
        for color in colors:
            options.append(
                ft.DropdownOption(
                    key=color.value,
                    content=ft.Text(
                        value=color.value,
                        color=color,
                    ),
                )
            )
        return options

    def dropdown_changed(e):
        e.control.color = e.control.value
        page.update()

    dd = ft.Dropdown(
        editable=True,
        label="Color",
        options=get_options(),
        on_change=dropdown_changed,
    )

    page.add(dd)


ft.run(main)
```


<img src="/img/docs/controls/dropdown/dropdown-with-colors.png" className="screenshot-20"/>

### Dropdown with icons



```python
import flet as ft

def main(page: ft.Page):

    icons = [
        {"name": "Smile", "icon_name": ft.Icons.SENTIMENT_SATISFIED_OUTLINED},
        {"name": "Cloud", "icon_name": ft.Icons.CLOUD_OUTLINED},
        {"name": "Brush", "icon_name": ft.Icons.BRUSH_OUTLINED},
        {"name": "Heart", "icon_name": ft.Icons.FAVORITE},
    ]

    def get_options():
        options = []
        for icon in icons:
            options.append(
                ft.DropdownOption(key=icon["name"], leading_icon=icon["icon_name"])
            )
        return options

    dd = ft.Dropdown(
        border=ft.InputBorder.UNDERLINE,
        enable_filter=True,
        editable=True,
        leading_icon=ft.Icons.SEARCH,
        label="Icon",
        options=get_options(),
    )

    page.add(dd)


ft.run(main)
```


<img src="/img/docs/controls/dropdown/dropdown-with-icons.png" className="screenshot-20"/>
