import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_visible(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            spacing=8,
            controls=[
                ft.Container(
                    width=260,
                    height=44,
                    bgcolor=ft.Colors.GREEN_300,
                    border_radius=8,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text("Visible: True"),
                ),
                ft.Container(
                    width=260,
                    height=44,
                    bgcolor=ft.Colors.RED_300,
                    border_radius=8,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text("Visible: False"),
                    visible=False,
                ),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_parent_not_visible_child_visible(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            spacing=8,
            controls=[
                ft.Container(
                    width=260,
                    height=44,
                    bgcolor=ft.Colors.GREEN_300,
                    border_radius=8,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text("Visible sibling"),
                ),
                ft.Container(
                    visible=False,
                    content=ft.Container(
                        visible=True,
                        width=260,
                        height=44,
                        bgcolor=ft.Colors.RED_300,
                        border_radius=8,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Text("Hidden parent, visible child"),
                    ),
                ),
            ],
        ),
    )
