from dataclasses import dataclass, field
from typing import Any

import flet as ft


def main(page: ft.Page):
    @ft.control
    class MyButton(ft.Button):
        expand: int = field(default_factory=lambda: 1)
        style: ft.ButtonStyle = field(
            default_factory=lambda: ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)
            )
        )
        bgcolor: ft.Colors = ft.Colors.BLUE_ACCENT
        icon: Any = ft.Icons.HEADPHONES

    @dataclass
    class MyButton2(ft.Button):
        expand: Any = 1
        bgcolor: ft.Colors = ft.Colors.GREEN_ACCENT
        style: ft.ButtonStyle = field(
            default_factory=lambda: ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20)
            )
        )
        icon: ft.IconDataOrControl = ft.Icons.HEADPHONES

    @ft.control
    class MyButton3(ft.Button):
        def init(self):
            self.expand = 1
            self.bgcolor = ft.Colors.RED_ACCENT
            self.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30))
            self.icon = ft.Icons.HEADPHONES

    page.add(
        ft.Row([MyButton(content="1")]),
        ft.Row([MyButton2(content="2")]),
        ft.Row([MyButton3(content="3")]),
    )


ft.run(main)
