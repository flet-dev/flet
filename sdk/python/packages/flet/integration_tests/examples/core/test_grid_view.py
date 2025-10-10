import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.GridView(
            width=180,
            runs_count=2,
            spacing=8,
            controls=[
                ft.Container(
                    width=50, height=50, bgcolor=ft.Colors.PRIMARY, border_radius=8
                ),
                ft.Container(
                    width=50, height=50, bgcolor=ft.Colors.SECONDARY, border_radius=8
                ),
                ft.Container(
                    width=50, height=50, bgcolor=ft.Colors.TERTIARY, border_radius=8
                ),
                ft.Container(
                    width=50, height=50, bgcolor=ft.Colors.ERROR, border_radius=8
                ),
            ],
        ),
    )
