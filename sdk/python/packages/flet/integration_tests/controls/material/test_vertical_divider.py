import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_vertical_divider_basic(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app.page.enable_screenshots = True
    await flet_app.resize_page(400, 600)
    flet_app.page.add(ft.VerticalDivider(expand=True))
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "vertical_divider_basic",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_vertical_divider_properties(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app.page.enable_screenshots = True
    await flet_app.resize_page(400, 600)
    flet_app.page.add(
        ft.VerticalDivider(
            expand=True,
            thickness=20,
            color=ft.Colors.RED,
            width=100,
            leading_indent=100,
            trailing_indent=100,
            radius=10,
        )
    )
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "vertical_divider_properties",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
