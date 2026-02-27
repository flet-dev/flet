from __future__ import annotations

import flet as ft

from models import TrolliState
from .dialogs import show_login_dialog


@ft.component
def TrolliAppBar(app: TrolliState):
    profile_label = "Log in" if not app.user else f"{app.user}'s Profile"

    return ft.AppBar(
        leading=ft.Icon(ft.Icons.GRID_GOLDENRATIO_ROUNDED),
        leading_width=100,
        title=ft.Text(
            "Trolli",
            font_family="Pacifico",
            size=32,
            text_align=ft.TextAlign.START,
        ),
        center_title=False,
        toolbar_height=60,
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_700,
        actions=[
            ft.Container(
                margin=ft.margin.only(left=50, right=25),
                content=ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            content=profile_label,
                            on_click=(
                                (lambda _: show_login_dialog(app))
                                if not app.user
                                else None
                            ),
                        ),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(content="Settings"),
                    ]
                ),
            )
        ],
    )
