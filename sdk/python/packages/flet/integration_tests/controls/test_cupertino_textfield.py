import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_cupertino_textfield(flet_app: ftt.FletTestApp, request):
    ct = ft.CupertinoTextField(
        placeholder_text="Cupertino text field",
        placeholder_style=ft.TextStyle(color=ft.Colors.GREY_400),
    )

    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.controls = [ct]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "empty",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    ct.value = "testing textfield 123"
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "filled",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
