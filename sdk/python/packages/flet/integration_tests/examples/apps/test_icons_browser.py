import pytest

import examples.apps.icons_browser.main as icons_browser
import flet as ft
import flet.testing as ftt


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": icons_browser.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_icons_browser(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(800, 800 * 0.625)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("Material")).count == 1
    assert (await flet_app_function.tester.find_by_text("Cupertino")).count == 1

    search_input = await flet_app_function.tester.find_by_key(
        "material_icons_search_input"
    )
    assert search_input.count == 1
    await flet_app_function.tester.enter_text(search_input, "add")
    await flet_app_function.tester.pump_and_settle()

    search_button = await flet_app_function.tester.find_by_key(
        "material_icons_search_button"
    )
    assert search_button.count == 1
    await flet_app_function.tester.tap(search_button)
    await flet_app_function.tester.pump_and_settle()

    add_icon = await flet_app_function.tester.find_by_text("ADD")
    assert add_icon.count == 1
    await flet_app_function.tester.mouse_hover(add_icon)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "icons_browser",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
