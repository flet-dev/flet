import pytest

import flet as ft
import flet.testing as ftt
from examples.tutorials.calculator import calc1, calc2, calc3


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": calc1.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_calc1(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(350, 850)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "calc1",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": calc2.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_calc2(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(350, 350)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "calc2",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": calc3.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_calc3(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(400, 350)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "calc3",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
