import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_chip(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Chip(
            label=ft.Text("Save to favourites"),
            leading=ft.Icon(ft.Icons.FAVORITE_BORDER_OUTLINED),
            bgcolor=ft.Colors.GREEN_200,
            disabled_color=ft.Colors.GREEN_100,
            autofocus=True,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_chip_clicked(flet_app: ftt.FletTestApp, request):
    flet_app.page.clean()
    await flet_app.tester.pump_and_settle()

    def handle_chip_click(e: ft.Event[ft.Chip]):
        e.control.label.value = "Saved to favorites"
        e.control.leading = ft.Icon(ft.Icons.FAVORITE_OUTLINED)
        e.control.disabled = True

    chip = ft.Chip(
        label=ft.Text("Save to favourites"),
        leading=ft.Icon(ft.Icons.FAVORITE_BORDER_OUTLINED),
        bgcolor=ft.Colors.GREEN_200,
        disabled_color=ft.Colors.GREEN_100,
        autofocus=True,
        on_click=handle_chip_click,
        key="chip",
    )

    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.add(chip)
    await flet_app.tester.pump_and_settle()
    await flet_app.tester.tap(await flet_app.tester.find_by_key("chip"))
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "chip_clicked",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
