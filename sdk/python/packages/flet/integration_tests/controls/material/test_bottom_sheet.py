import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_bottom_sheet_basic(flet_app: ftt.FletTestApp, request):
    bs = ft.BottomSheet(
        content=ft.Container(
            padding=50,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
                controls=[
                    ft.Text("Here is a bottom sheet!"),
                    ft.Button("Dismiss", on_click=lambda _: flet_app.page.pop_dialog()),
                ],
            ),
        ),
    )
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(400, 600)
    flet_app.page.show_dialog(bs)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "bottom_sheet_basic",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
