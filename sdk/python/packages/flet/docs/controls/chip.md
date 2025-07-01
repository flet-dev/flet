::: flet.Chip

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/chip)

### Assist chips

Assist chips are chips with `leading` icon and `on_click` event specified. They represent smart or automated actions that appear dynamically and contextually in a UI.

An alternative to assist chips are buttons, which should appear persistently and consistently.



```python
import flet as ft


def main(page: ft.Page):
    def save_to_favorites_clicked(e):
        e.control.label.value = "Saved to favorites"
        e.control.leading = ft.Icon(ft.Icons.FAVORITE_OUTLINED)
        e.control.disabled = True
        page.update()

    def open_google_maps(e):
        page.launch_url("https://maps.google.com")
        page.update()

    save_to_favourites = ft.Chip(
        label=ft.Text("Save to favourites"),
        leading=ft.Icon(ft.Icons.FAVORITE_BORDER_OUTLINED),
        bgcolor=ft.Colors.GREEN_200,
        disabled_color=ft.Colors.GREEN_100,
        autofocus=True,
        on_click=save_to_favorites_clicked,
    )

    open_in_maps = ft.Chip(
        label=ft.Text("9 min walk"),
        leading=ft.Icon(ft.Icons.MAP_SHARP),
        bgcolor=ft.Colors.GREEN_200,
        on_click=open_google_maps,
    )

    page.add(ft.Row([save_to_favourites, open_in_maps]))

ft.run(main)
```


<img src="/img/docs/controls/chip/assist-chips.png" className="screenshot-40"/>

### Filter chips

Filter chips are chips with `on_select` event specified. They use tags or descriptive words provided in the `label` to filter content. They can be a good alternative to switches or checkboxes.



```python
import flet as ft

def main(page: ft.Page):
    def amenity_selected(e):
        page.update()

    title = ft.Row([ft.Icon(ft.Icons.HOTEL_CLASS), ft.Text("Amenities")])
    amenities = ["Washer / Dryer", "Ramp access", "Dogs OK", "Cats OK", "Smoke-free"]
    amenity_chips = []

    for amenity in amenities:
        amenity_chips.append(
            ft.Chip(
                label=ft.Text(amenity),
                bgcolor=ft.Colors.GREEN_200,
                disabled_color=ft.Colors.GREEN_100,
                autofocus=True,
                on_select=amenity_selected,
            )
        )

    page.add(title, ft.Row(amenity_chips))

ft.run(main)
```


<img src="/img/docs/controls/chip/filter-chips.png" className="screenshot-60"/>

