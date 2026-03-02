from __future__ import annotations

import flet as ft

from models import TrolliState


@ft.component
def Sidebar(app: TrolliState):
    board_id = app.current_board_id
    active_board_index = (
        next((i for i, b in enumerate(app.boards) if b.board_id == board_id), None)
        if board_id is not None
        else None
    )
    top_index = (
        0
        if app.active_screen == "boards"
        else 1 if app.active_screen == "members" else None
    )

    def top_nav_change(e: ft.Event[ft.NavigationRail]):
        if e.control.selected_index == 0:
            ft.context.page.go("/boards")
        elif e.control.selected_index == 1:
            ft.context.page.go("/members")

    def bottom_nav_change(e: ft.Event[ft.NavigationRail]):
        idx = e.control.selected_index
        if idx is None:
            return
        ft.context.page.go(f"/board/{app.boards[idx].board_id}")

    return ft.Container(
        width=200,
        bgcolor=ft.Colors.BLUE_GREY,
        padding=ft.Padding.all(15),
        visible=app.nav_visible,
        content=ft.Column(
            tight=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[ft.Text("Workspace")],
                ),
                ft.Divider(height=1, thickness=1, color=ft.Colors.BLACK_26),
                ft.NavigationRail(
                    selected_index=top_index,
                    label_type=ft.NavigationRailLabelType.ALL,
                    bgcolor=ft.Colors.BLUE_GREY,
                    extended=True,
                    height=110,
                    on_change=top_nav_change,
                    destinations=[
                        ft.NavigationRailDestination(
                            label="Boards",
                            icon=ft.Icons.BOOK_OUTLINED,
                            selected_icon=ft.Icons.BOOK_OUTLINED,
                        ),
                        ft.NavigationRailDestination(
                            label="Members",
                            icon=ft.Icons.PERSON,
                            selected_icon=ft.Icons.PERSON,
                        ),
                    ],
                ),
                ft.Divider(height=1, thickness=1, color=ft.Colors.BLACK_26),
                ft.NavigationRail(
                    selected_index=active_board_index,
                    label_type=ft.NavigationRailLabelType.ALL,
                    bgcolor=ft.Colors.BLUE_GREY,
                    extended=True,
                    expand=True,
                    on_change=bottom_nav_change,
                    destinations=[
                        ft.NavigationRailDestination(
                            label=b.name,
                            icon=ft.Icons.CHEVRON_RIGHT_OUTLINED,
                            selected_icon=ft.Icons.CHEVRON_RIGHT_ROUNDED,
                        )
                        for b in app.boards
                    ],
                ),
            ],
        ),
    )
