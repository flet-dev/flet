import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.search_bar import basic


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.SearchBar(bar_hint_text="Search..."),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(450, 300)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    # scr = await flet_app_function.wrap_page_controls_in_screenshot()
    button = await flet_app_function.tester.find_by_text_containing("Search")
    await flet_app_function.tester.tap(button)

    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "basic",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
