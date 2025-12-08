import pytest

import flet as ft
import flet.testing as ftt

from examples.controls.navigation_bar import basic


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    nvb = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.CIRCLE, label="Item 1"),
            ft.NavigationBarDestination(icon=ft.Icons.SQUARE, label="Item 2"),
            ft.NavigationBarDestination(icon=ft.Icons.HEXAGON, label="Item 3"),
        ],
    )
    flet_app_function.resize_page(400, 100)
    flet_app_function.page.navigation_bar = nvb
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle(
        duration=ft.Duration(milliseconds=800)
    )
    flet_app_function.assert_screenshot(
        "image_for_docs",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(300, 300)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "basic",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
