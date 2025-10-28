import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.bottom_app_bar import border_radius, notched_fab


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.window.width = 400

    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.BottomAppBar(
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    ft.IconButton(ft.Icons.MENU),
                    ft.IconButton(ft.Icons.SEARCH),
                    ft.IconButton(ft.Icons.SETTINGS),
                ],
            ),
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": border_radius.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_border_radius(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.window.width = 500
    flet_app_function.page.window.height = 400
    flet_app_function.page.update()

    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "border_radius",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": notched_fab.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_notched_fab(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.window.width = 500
    flet_app_function.page.window.height = 400
    flet_app_function.page.update()

    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "notched_fab",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
