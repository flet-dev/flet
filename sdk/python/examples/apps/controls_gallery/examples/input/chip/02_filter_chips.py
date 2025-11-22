import flet as ft

name = "Filter chips"


def example():
    def amenity_selected(e):
        amenity_chips.update()

    title = ft.Row([ft.Icon(ft.Icons.HOTEL_CLASS), ft.Text("Amenities")])
    amenities = ["Washer / Dryer", "Ramp access", "Dogs OK", "Cats OK", "Smoke-free"]
    amenity_chips = ft.Row()

    for amenity in amenities:
        amenity_chips.controls.append(
            ft.Chip(
                label=ft.Text(amenity),
                on_select=amenity_selected,
            )
        )

    return ft.Column(controls=[title, amenity_chips])
