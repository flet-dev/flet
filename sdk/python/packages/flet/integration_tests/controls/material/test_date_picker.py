import datetime

import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_basic(flet_app: ftt.FletTestApp, request):
    dp = ft.DatePicker(
        current_date=datetime.datetime(year=2025, month=8, day=15),
        first_date=datetime.datetime(year=2000, month=10, day=1),
        last_date=datetime.datetime(year=2025, month=10, day=1),
    )
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(400, 600)
    flet_app.page.show_dialog(dp)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        request.node.name,
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
