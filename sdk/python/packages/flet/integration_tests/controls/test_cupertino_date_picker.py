import datetime

import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_cupertino_date_picker_basic(flet_app: ftt.FletTestApp, request):
    date_picker = ft.CupertinoDatePicker(
        value=datetime.datetime(year=2024, month=8, day=15),
        date_picker_mode=ft.CupertinoDatePickerMode.DATE_AND_TIME,
    )

    cupertino_bottom_sheet = ft.CupertinoBottomSheet(date_picker)
    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.show_dialog(cupertino_bottom_sheet)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "cupertino_date_picker_basic",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
