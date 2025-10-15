import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.vertical_divider import basic


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Row(
            width=120,
            height=60,
            expand=True,
            spacing=0,
            controls=[
                ft.Container(
                    bgcolor=ft.Colors.BLUE_GREY_200,
                    alignment=ft.Alignment.CENTER,
                    expand=True,
                ),
                ft.VerticalDivider(),
                ft.Container(
                    bgcolor=ft.Colors.GREY_500,
                    alignment=ft.Alignment.CENTER,
                    expand=True,
                ),
            ],
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
