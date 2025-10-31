import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.alert_dialog import modal_and_non_modal


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    dialog = ft.AlertDialog(
        title=ft.Text("Session expired"),
        content=ft.Text("Please sign in again to continue."),
        actions=[ft.TextButton("Dismiss")],
        open=True,
    )
    flet_app_function.page.enable_screenshots = True
    await flet_app_function.resize_page(350, 300)
    flet_app_function.page.add(dialog)
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
    [{"flet_app_main": modal_and_non_modal.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    await flet_app_function.resize_page(350, 300)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "before_click",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    button = await flet_app_function.tester.find_by_text_containing("Open dialog")
    await flet_app_function.tester.tap(button)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "non_modal_dialog",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    flet_app_function.page.pop_dialog()
    await flet_app_function.tester.pump_and_settle()
    modal_button = await flet_app_function.tester.find_by_text_containing(
        "Open modal dialog"
    )
    await flet_app_function.tester.tap(modal_button)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "modal_dialog",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    flet_app_function.create_gif(
        ["before_click", "non_modal_dialog", "before_click", "modal_dialog"],
        "alert_dialog_flow",
        duration=2000,
    )
