import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_cupertino_slider(flet_app: ftt.FletTestApp, request):
    sl = ft.CupertinoSlider(
        divisions=20,
        min=0,
        max=100,
        active_color=ft.Colors.PURPLE,
        thumb_color=ft.Colors.PURPLE,
    )

    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.controls = [sl]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "slider start",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    sl.value = 50.0
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "slider middle",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
