import flet as ft
import flet_map as ftm


def main(page: ft.Page):
    page.add(
        ft.SafeArea(
            expand=True,
            content=ftm.Map(
                expand=True,
                layers=[
                    ftm.TileLayer(
                        url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                        user_agent_package_name="flet-map-examples/1.0",
                        on_image_error=lambda e: print(f"TileLayer Error: {e.data}"),
                    ),
                    ftm.SimpleAttribution(text="OpenStreetMap contributors"),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
