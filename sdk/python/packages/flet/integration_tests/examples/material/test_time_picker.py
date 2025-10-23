import pytest
from datetime import time

import flet as ft
import flet.testing as ftt
from examples.controls.time_picker import basic


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    tp = ft.TimePicker(
        value=time(1, 2),
        time_picker_entry_mode=ft.TimePickerEntryMode.INPUT_ONLY,
        open=True,
    )
    flet_app_function.page.enable_screenshots = True
    flet_app_function.page.window.width = 400
    flet_app_function.page.window.height = 300
    flet_app_function.page.add(tp)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "test_image_for_docs",
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
    flet_app_function.page.enable_screenshots = True
    flet_app_function.page.window.width = 350
    flet_app_function.page.window.height = 300
    button = await flet_app_function.tester.find_by_icon(ft.Icons.TIME_TO_LEAVE)
    await flet_app_function.tester.tap(button)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "basic",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
