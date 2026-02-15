import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.hero import basic


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(380, 500)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    # Initial home view
    flet_app_function.assert_screenshot(
        "basic_1",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    # Navigate to details view
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Open details")
    )
    await flet_app_function.tester.pump_and_settle(
        duration=ft.Duration(milliseconds=700)
    )
    flet_app_function.assert_screenshot(
        "basic_2",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    # Navigate back to home view
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Back")
    )
    await flet_app_function.tester.pump_and_settle(
        duration=ft.Duration(milliseconds=700)
    )
    flet_app_function.assert_screenshot(
        "basic_1",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    # Create GIF
    flet_app_function.create_gif(
        ["basic_1", "basic_2"],
        "basic",
        duration=1400,
    )
