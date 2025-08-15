import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_alert_dialog_basic(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    ad = ft.AlertDialog(
        key="ad",
        title=ft.Text("Hello"),
        content=ft.Text("You are notified!"),
        alignment=ft.Alignment.CENTER,
        on_dismiss=lambda e: print("Dialog dismissed!"),
        title_padding=ft.Padding.all(25),
    )
    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.show_dialog(ad)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "alert_dialog_basic",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
