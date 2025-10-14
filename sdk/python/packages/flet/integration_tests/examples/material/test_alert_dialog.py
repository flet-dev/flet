import pytest

import flet as ft
import flet.testing as ftt


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
    flet_app_function.page.window.width = 350
    flet_app_function.page.window.height = 300
    flet_app_function.page.add(dialog)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "test_image_for_docs",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
