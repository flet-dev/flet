import flet as ft
import flet_map as ftm


def main(page: ft.Page):
    page.add(
        ft.SafeArea(
            content=ftm.Map(
                expand=True,
                layers=[
                    ftm.TileLayer(
                        url_template="https://tile.memomaps.de/tilegen/{z}/{x}/{y}.png",
                        on_image_error=lambda e: print(f"TileLayer Error: {e.data}"),
                    ),
                ],
            ),
        )
    )


ft.run(main)
