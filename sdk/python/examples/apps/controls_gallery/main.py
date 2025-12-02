import logging

from components.gallery_view import GalleryView
from gallerydata import GalleryData

import flet as ft
import flet.version

gallery = GalleryData()

logging.basicConfig(level=logging.DEBUG)

ft.context.disable_auto_update()


def main(page: ft.Page):
    page.title = "Flet controls gallery"

    page.fonts = {
        "Roboto Mono": "RobotoMono-VariableFont_wght.ttf",
        "RobotoSlab": "RobotoSlab[wght].ttf",
    }

    def get_route_list(route):
        route_list = [item for item in route.split("/") if item != ""]
        return route_list

    def route_change(e):
        route_list = get_route_list(page.route)

        if len(route_list) == 0:
            page.go("/layout")
        else:
            # gallery.selected_control_group = gallery.get_control_group(route_list[0])
            if len(route_list) == 1:
                gallery_view.display_controls_grid(route_list[0])
            elif len(route_list) == 2:
                gallery_view.display_control_examples(route_list[0], route_list[1])
            else:
                print("Invalid route")

    gallery_view = GalleryView(gallery)

    page.appbar = ft.AppBar(
        leading=ft.Container(padding=5, content=ft.Image(src="logo.svg")),
        leading_width=40,
        title=ft.Text("Flet Controls Gallery"),
        center_title=True,
        bgcolor=ft.Colors.INVERSE_PRIMARY,
        actions=[
            ft.Container(
                padding=10, content=ft.Text(f"Flet version: {flet.version.version}")
            )
        ],
    )

    page.theme_mode = ft.ThemeMode.LIGHT
    # page.on_error = lambda e: print("Page error:", e.data)

    page.add(gallery_view)
    page.on_route_change = route_change
    print(f"Initial route: {page.route}")
    page.go(page.route)


# os.environ["FLET_PLATFORM"] = "macos"
# ft.run(main, view=ft.AppView.FLET_APP, port=8550)

ft.run(main)
