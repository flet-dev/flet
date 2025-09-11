import datetime

import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_basic(flet_app: ftt.FletTestApp, request):
    dp = ft.DateRangePicker(
        start_value=datetime.datetime(year=2000, month=10, day=1),
        end_value=datetime.datetime(year=2000, month=10, day=15),
    )
    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.show_dialog(dp)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "basic",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
