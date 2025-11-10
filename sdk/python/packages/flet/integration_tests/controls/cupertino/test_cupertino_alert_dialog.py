import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_cupertino_alert_dialog_basic(flet_app: ftt.FletTestApp, request):
    cad = ft.CupertinoAlertDialog(
        title=ft.Text("Cupertino Alert Dialog"),
        content=ft.Text("Do you want to delete this file?"),
    )
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(400, 600)
    flet_app.page.show_dialog(cad)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "cupertino_alert_dialog_basic",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
