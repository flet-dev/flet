import pytest

import examples.apps.declarative.sunflower.main as sunflower
import flet as ft
import flet.testing as ftt


def sunflower_main(page: ft.Page):
    page.render_views(sunflower.Sunflower)


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": sunflower_main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_declarative_sunflower(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(500, 630)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("Sunflower")).count == 1
    assert (await flet_app_function.tester.find_by_text("Showing 125 seeds")).count == 1

    flet_app_function.assert_screenshot(
        "declarative_sunflower",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
