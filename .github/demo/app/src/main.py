"""Demo app for the Linux app icon work in flet-dev/flet#2269.

The window content is only a reading aid: the thing under test is what the
desktop shows *around* the window -- the dock icon, the app-grid entry and the
name in the window list. So the app just restates the identity it was built
with, next to the icon it should be wearing.
"""

import os
from pathlib import Path

import flet as ft

BUNDLE_ID = "com.flet.flet_icon_demo"
ARTIFACT = "flet-icon-demo"

# `flet build` points FLET_ASSETS_DIR at the bundled assets; the fallback is
# for running this from a checkout. Read as bytes rather than handed to Image
# as an asset path, because that path resolves differently per run mode and a
# broken image is the one thing this demo cannot afford to show.
ASSETS = Path(os.getenv("FLET_ASSETS_DIR") or Path(__file__).parent / "assets")
try:
    ICON = (ASSETS / "icon_linux.png").read_bytes()
except OSError:
    ICON = None

CHECKS = [
    ("Window icon", "The icon in the title bar / window list, on X11."),
    ("Dock icon", "The icon in the dock or taskbar, once the app is running."),
    ("App grid", "The launcher entry, named 'Flet Icon Demo'."),
    ("File manager", "The icon on the launcher, not on the executable file."),
]


def labelled(label: str, value: str) -> ft.Row:
    """One `label   value` line, with the values left-aligned as a column."""
    return ft.Row(
        controls=[
            ft.Text(label, width=110, color=ft.Colors.ON_SURFACE_VARIANT),
            ft.Text(value, selectable=True, font_family="monospace"),
        ],
        spacing=8,
    )


def main(page: ft.Page):
    page.title = "Flet Icon Demo"
    page.window.width = 620
    page.window.height = 560
    page.padding = 28

    page.add(
        ft.Row(
            controls=[
                # The very file `flet build` used as the Linux icon, so the
                # window shows exactly what the dock is meant to show.
                ft.Image(src=ICON, width=96, height=96)
                if ICON
                else ft.Container(width=96, height=96),
                ft.Column(
                    controls=[
                        ft.Text("Flet Icon Demo", size=26, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            "The icon on the left is the one this app was built "
                            "with. Look for it everywhere the desktop shows "
                            "this app.",
                            color=ft.Colors.ON_SURFACE_VARIANT,
                        ),
                    ],
                    spacing=4,
                    expand=True,
                ),
            ],
            spacing=20,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        ft.Divider(height=32),
        ft.Text("Built with", weight=ft.FontWeight.BOLD),
        labelled("Bundle ID", BUNDLE_ID),
        labelled("Artifact", ARTIFACT),
        labelled("Categories", "Graphics;Viewer;"),
        ft.Divider(height=32),
        ft.Text("Where the icon should appear", weight=ft.FontWeight.BOLD),
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(name, width=110, weight=ft.FontWeight.W_500),
                        ft.Text(detail, expand=True, color=ft.Colors.ON_SURFACE_VARIANT),
                    ],
                    spacing=8,
                )
                for name, detail in CHECKS
            ],
            spacing=6,
        ),
    )


ft.run(main)
