import flet as ft


def main(page: ft.Page):
    def handle_amenity_selection(e: ft.Event[ft.Chip]):
        page.update()

    amenities = ["Washer / Dryer", "Ramp access", "Dogs OK", "Cats OK", "Smoke-free"]

    page.add(
        ft.Row(controls=[ft.Icon(ft.Icons.HOTEL_CLASS), ft.Text("Amenities")]),
        ft.Row(
            controls=[
                ft.Chip(
                    label=ft.Text(amenity),
                    bgcolor=ft.Colors.GREEN_200,
                    disabled_color=ft.Colors.GREEN_100,
                    autofocus=True,
                    on_select=handle_amenity_selection,
                )
                for amenity in amenities
            ]
        ),
    )


ft.run(main)
