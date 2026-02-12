import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.PageView(
            height=220,
            viewport_fraction=0.85,
            controls=[
                ft.Container(
                    bgcolor=ft.Colors.PURPLE,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text("One", color=ft.Colors.WHITE),
                ),
                ft.Container(
                    bgcolor=ft.Colors.TEAL,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text("Two", color=ft.Colors.WHITE),
                ),
                ft.Container(
                    bgcolor=ft.Colors.AMBER,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text("Three", color=ft.Colors.BLACK),
                ),
            ],
        ),
    )
