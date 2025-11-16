import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.snack_bar import action, basic, counter


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    sb = ft.SnackBar(ft.Text("Opened snack bar"))
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(250, 200)
    flet_app_function.page.show_dialog(sb)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "test_image_for_docs",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(250, 200)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    button = await flet_app_function.tester.find_by_text_containing("Open SnackBar")
    await flet_app_function.tester.tap(button)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "basic",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": counter.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_counter(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(250, 200)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "before_click",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    button = await flet_app_function.tester.find_by_text_containing("Open SnackBar")
    await flet_app_function.tester.tap(button)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "click_1",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    await flet_app_function.tester.tap(button)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "click_2",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    flet_app_function.create_gif(
        ["before_click", "click_1", "click_2"],
        "snack_bar_flow",
        duration=2000,
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": action.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_action(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(450, 300)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    button = await flet_app_function.tester.find_by_text_containing(
        "Open SnackBar with a Simple action"
    )
    await flet_app_function.tester.tap(button)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "action_simple",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    button = await flet_app_function.tester.find_by_text_containing(
        "Open SnackBar with a Custom action"
    )
    await flet_app_function.tester.tap(button)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "action_custom",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
