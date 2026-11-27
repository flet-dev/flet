"""Screen states.

A screen that shows data renders one of these instead of a blank area.
"""

from collections.abc import Callable

import theme

import flet as ft


@ft.component
def EmptyState(
    icon: ft.IconData, title: str, message: str, action: ft.Control | None = None
):
    return _Centered(
        [
            ft.Icon(icon, size=56, color=ft.Colors.OUTLINE),
            ft.Text(
                title, theme_style=theme.Text.TITLE, text_align=ft.TextAlign.CENTER
            ),
            ft.Text(
                message,
                theme_style=theme.Text.BODY,
                color=ft.Colors.ON_SURFACE_VARIANT,
                text_align=ft.TextAlign.CENTER,
            ),
            *([action] if action else []),
        ]
    )


@ft.component
def LoadingState(message: str = "Loading…"):
    return _Centered(
        [ft.ProgressRing(), ft.Text(message, color=ft.Colors.ON_SURFACE_VARIANT)]
    )


@ft.component
def ErrorState(message: str, on_retry: Callable | None = None):
    return _Centered(
        [
            ft.Icon(ft.Icons.ERROR_OUTLINE, size=56, color=ft.Colors.ERROR),
            ft.Text("Something went wrong", theme_style=theme.Text.TITLE),
            ft.Text(
                message,
                color=ft.Colors.ON_SURFACE_VARIANT,
                text_align=ft.TextAlign.CENTER,
            ),
            *([ft.OutlinedButton("Try again", on_click=on_retry)] if on_retry else []),
        ]
    )


def _Centered(controls: list[ft.Control]) -> ft.Control:
    return ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        padding=theme.Space.XL,
        content=ft.Column(
            controls,
            tight=True,
            spacing=theme.Space.M,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
