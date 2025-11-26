import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.pagelet import basic


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Pagelet(
            width=350,
            height=300,
            appbar=ft.AppBar(title="Pagelet AppBar", bgcolor=ft.Colors.BLUE),
            content=ft.Text("Pagelet Content"),
            navigation_bar=ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(icon=ft.Icons.ADD, label="New"),
                    ft.NavigationBarDestination(icon=ft.Icons.INBOX, label="Inbox"),
                ],
            ),
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "basic",
        await flet_app_function.take_page_controls_screenshot(),
    )
