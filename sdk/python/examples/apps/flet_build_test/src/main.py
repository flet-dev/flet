import sys

import numpy
import pillow
from modules.utils import greet

import flet as ft
import flet_ads  # noqa: F401
import flet_audio  # noqa: F401
import flet_audio_recorder  # noqa: F401
import flet_charts  # noqa: F401
import flet_datatable2  # noqa: F401
import flet_flashlight  # noqa: F401
import flet_geolocator  # noqa: F401
import flet_lottie  # noqa: F401
import flet_map  # noqa: F401
import flet_permission_handler  # noqa: F401
import flet_rive  # noqa: F401
import flet_secure_storage  # noqa: F401
import flet_video  # noqa: F401
import flet_webview  # noqa: F401


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.appbar = ft.AppBar(
        title=ft.Text("Flet Build Test"),
        center_title=True,
        # actions=[
        #     ft.Container(
        #         content=ft.Text(f"v{ft.__version__}", weight=ft.FontWeight.BOLD),
        #         padding=ft.Padding.only(right=15),
        #     )
        # ],
    )

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.INFO,
        bgcolor=ft.Colors.BLUE,
        on_click=lambda: page.show_dialog(
            ft.AlertDialog(
                title="Debug Info",
                content=ft.Column(
                    controls=[
                        ft.Text(f"Numpy: v{numpy.__version__}"),
                        ft.Text(f"Pillow: v{pillow.__version__}"),
                        ft.Text(f"sys.path: {sys.path}"),
                    ]
                ),
            )
        ),
    )

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Text(greet("Flet"), size=20, weight=ft.FontWeight.BOLD),
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
