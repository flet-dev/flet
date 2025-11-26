import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_theme_1(flet_app: ftt.FletTestApp, request):
    flet_app.resize_page(400, 600)
    flet_app.page.theme = ft.Theme(
        outlined_button_theme=ft.OutlinedButtonTheme(
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN,
                shape=ft.BeveledRectangleBorder(
                    radius=5,
                ),
                side=ft.BorderSide(width=5, color=ft.Colors.GREEN_900),
                padding=ft.Padding.all(10),
            ),
        )
    )

    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.OutlinedButton(content="Button"),
    )
