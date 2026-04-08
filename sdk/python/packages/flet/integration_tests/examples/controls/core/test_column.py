import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Column(
            width=220,
            height=120,
            spacing=12,
            controls=[
                ft.Text("Daily planning", size=20, weight=ft.FontWeight.W_600),
                ft.Text("Review pull requests"),
                ft.Text("Ship release"),
            ],
        ),
    )
