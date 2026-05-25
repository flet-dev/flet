import pytest

import examples.apps.flet_animation.main as flet_animation
import flet as ft
import flet.testing as ftt


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": flet_animation.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_flet_animation(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(900, 520)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    go_button = await flet_app_function.tester.find_by_text("Go!")
    assert go_button.count == 1
    await flet_app_function.tester.tap(go_button)
    await flet_app_function.tester.pump_and_settle(
        duration=ft.Duration(milliseconds=2500)
    )

    assert (await flet_app_function.tester.find_by_text("Again!")).count == 1

    flet_app_function.assert_screenshot(
        "flet_animation",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
