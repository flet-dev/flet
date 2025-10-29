import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_range_slider(flet_app: ftt.FletTestApp, request):
    rs = ft.RangeSlider(
        min=0,
        max=50,
        start_value=0,
        divisions=10,
        end_value=50,
        inactive_color=ft.Colors.GREEN_300,
        active_color=ft.Colors.GREEN_700,
        overlay_color=ft.Colors.GREEN_100,
        label="{value}%",
        key="rs",
    )
    c = ft.Container(content=rs, padding=ft.Padding.only(top=40))

    flet_app.page.enable_screenshots = True
    await flet_app.resize_page(400, 600)
    flet_app.page.controls = [c]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    # default
    flet_app.assert_screenshot(
        "default",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # move slider
    rs.end_value = 20
    rs.start_value = 10
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "slider_move",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # tap
    await flet_app.tester.tap(await flet_app.tester.find_by_key("rs"))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "tap",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
