import pytest

import examples.apps.calculator.main as calculator
import flet as ft
import flet.testing as ftt


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": calculator.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_calculator(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(430, 520)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("AC")).count == 1
    assert (await flet_app_function.tester.find_by_text("=")).count == 1

    flet_app_function.assert_screenshot(
        "calculator",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
