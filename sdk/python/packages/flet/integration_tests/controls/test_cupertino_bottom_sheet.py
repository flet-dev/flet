import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_cupertino_bottom_sheet_basic(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    action_sheet = ft.CupertinoActionSheet(
        title=ft.Row(
            controls=[ft.Text("Title"), ft.Icon(ft.Icons.BEDTIME)],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        message=ft.Row(
            controls=[ft.Text("Description"), ft.Icon(ft.Icons.AUTO_AWESOME)],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        cancel=ft.CupertinoActionSheetAction(
            content=ft.Text("Cancel"),
        ),
        actions=[
            ft.CupertinoActionSheetAction(
                content=ft.Text("Default Action"),
                default=True,
            ),
            ft.CupertinoActionSheetAction(
                content=ft.Text("Normal Action"),
            ),
            ft.CupertinoActionSheetAction(
                content=ft.Text("Destructive Action"),
                destructive=True,
            ),
        ],
    )

    cupertino_bottom_sheet = ft.CupertinoBottomSheet(action_sheet)
    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.show_dialog(cupertino_bottom_sheet)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "cupertino_bottom_sheet_basic",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
