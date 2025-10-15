import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    page = flet_app_function.page
    page.theme_mode = ft.ThemeMode.LIGHT
    page.enable_screenshots = True
    page.window.width = 400
    page.window.height = 400
    sheet = ft.CupertinoActionSheet(
        title=ft.Text("Choose an option"),
        message=ft.Text("Select what you would like to do."),
        actions=[
            ft.CupertinoActionSheetAction(content=ft.Text("Save")),
            ft.CupertinoActionSheetAction(content=ft.Text("Delete"), destructive=True),
        ],
        cancel=ft.CupertinoActionSheetAction(content=ft.Text("Cancel")),
    )
    page.add(sheet)
    page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "test_image_for_docs",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    page.update()
