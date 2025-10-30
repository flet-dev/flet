import datetime

import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_time_picker_basic(flet_app: ftt.FletTestApp, request):
    time_picker = ft.TimePicker(
        confirm_text="Confirm",
        error_invalid_text="Time out of range",
        help_text="Pick your time slot",
        value=datetime.time(hour=1, minute=30, second=30),
    )
    flet_app.page.enable_screenshots = True
    await flet_app.resize_page(400, 600)
    flet_app.page.show_dialog(time_picker)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "time_picker_basic",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
