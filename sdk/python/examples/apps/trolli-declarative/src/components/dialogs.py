from __future__ import annotations

import asyncio
from typing import Sequence
from dataclasses import dataclass

import flet as ft

from models import Board, TrolliState


@dataclass(frozen=True)
class _ColorOption:
    value: str


LIST_COLORS: list[_ColorOption] = [
    _ColorOption(ft.Colors.LIGHT_GREEN),
    _ColorOption(ft.Colors.RED_200),
    _ColorOption(ft.Colors.AMBER_500),
    _ColorOption(ft.Colors.PINK_300),
    _ColorOption(ft.Colors.ORANGE_300),
    _ColorOption(ft.Colors.LIGHT_BLUE),
    _ColorOption(ft.Colors.DEEP_ORANGE_300),
    _ColorOption(ft.Colors.PURPLE_100),
    _ColorOption(ft.Colors.RED_700),
    _ColorOption(ft.Colors.TEAL_500),
    _ColorOption(ft.Colors.YELLOW_400),
    _ColorOption(ft.Colors.PURPLE_400),
    _ColorOption(ft.Colors.BROWN_300),
    _ColorOption(ft.Colors.CYAN_500),
    _ColorOption(ft.Colors.BLUE_GREY_500),
]


def show_login_dialog(app: TrolliState) -> None:
    user_field = ft.TextField(label="User name")
    password_field = ft.TextField(label="Password", password=True)
    error_text = ft.Text(value="", color=ft.Colors.RED)

    async def do_login(_: ft.Event):
        user = user_field.value.strip()
        pwd = password_field.value.strip()
        if not user or not pwd:
            error_text.value = "Please provide username and password"
            ft.context.page.update()
            return
        await ft.context.page.shared_preferences.set("current_user", user)
        app.user = user
        ft.context.page.pop_dialog()

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Log in"),
        content=ft.Column(
            tight=True,
            controls=[
                user_field,
                password_field,
                error_text,
                ft.FilledButton("Login", on_click=do_login),
            ],
        ),
        actions=[
            ft.TextButton("Cancel", on_click=lambda _: ft.context.page.pop_dialog())
        ],
    )
    ft.context.page.show_dialog(dlg)
    ft.context.page.update()


def show_new_board_dialog(app: TrolliState) -> None:
    name_field = ft.TextField(label="New board name")
    error_text = ft.Text(value="", color=ft.Colors.RED)

    def on_submit(_: ft.Event):
        name = name_field.value.strip()
        if not name:
            error_text.value = "Please enter a name"
            ft.context.page.update()
            return
        board = app.create_board(name)
        ft.context.page.pop_dialog()
        ft.context.page.go(f"/board/{board.board_id}")

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Create board"),
        content=ft.Column(tight=True, controls=[name_field, error_text]),
        actions=[
            ft.TextButton("Cancel", on_click=lambda _: ft.context.page.pop_dialog()),
            ft.FilledButton("Create", on_click=on_submit),
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
    ft.context.page.show_dialog(dlg)
    ft.context.page.update()


def show_new_list_dialog(board: Board) -> None:
    title_field = ft.TextField(label="New list name")
    error_text = ft.Text(value="", color=ft.Colors.RED)
    color_grid = ft.GridView(
        runs_count=3,
        max_extent=40,
        height=150,
        spacing=8,
        run_spacing=8,
    )

    def set_selected_color(e: ft.Event[ft.Container]):
        color_grid.data = e.control.data
        for option in color_grid.controls:
            option.border = (
                ft.Border.all(3, ft.Colors.BLACK_26)
                if option.data == color_grid.data
                else None
            )
        ft.context.page.update()

    def create(_: ft.Event[ft.Button]):
        title = title_field.value.strip()
        if not title:
            error_text.value = "Please enter a list name"
            ft.context.page.update()
            return
        board.add_list(title=title, color=color_grid.data)
        ft.context.page.pop_dialog()

    for option in LIST_COLORS:
        color_grid.controls.append(
            ft.Container(
                bgcolor=option.value,
                width=36,
                height=36,
                border_radius=ft.BorderRadius.all(999),
                data=option.value,
                on_click=set_selected_color,
            )
        )

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Create list"),
        content=ft.Column(
            tight=True,
            controls=[
                title_field,
                color_grid,
                error_text,
            ],
        ),
        actions=[
            ft.TextButton("Cancel", on_click=lambda _: ft.context.page.pop_dialog()),
            ft.FilledButton("Create", on_click=create),
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
    ft.context.page.show_dialog(dlg)
    ft.context.page.update()
