import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_cupertino_timer_picker_basic(flet_app: ftt.FletTestApp, request):
    timer_picker = ft.CupertinoTimerPicker(
        value=300,
        second_interval=10,
        minute_interval=1,
        mode=ft.CupertinoTimerPickerMode.HOUR_MINUTE_SECONDS,
    )

    cupertino_bottom_sheet = ft.CupertinoBottomSheet(timer_picker)
    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.show_dialog(cupertino_bottom_sheet)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "cupertino_timer_picker_basic",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
