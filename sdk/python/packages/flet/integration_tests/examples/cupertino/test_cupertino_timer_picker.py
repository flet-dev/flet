import pytest

import flet as ft
import flet.testing as ftt

from examples.controls.cupertino_timer_picker import basic


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.CupertinoTimerPicker(value=1000),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(400, 400)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    btn = await flet_app_function.tester.find_by_text("00:01:10")
    await flet_app_function.tester.tap(btn)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "basic",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
