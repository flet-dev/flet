import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_popup_menu_basic(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT

    pb = ft.PopupMenuButton(
        key="pb",
        items=[
            ft.PopupMenuItem("Item 1"),
            ft.PopupMenuItem(icon=ft.Icons.POWER_INPUT, content="Check power"),
            ft.PopupMenuItem(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.HOURGLASS_TOP_OUTLINED),
                        ft.Text("Item with a custom content"),
                    ]
                ),
            ),
            ft.PopupMenuItem(),  # divider
            ft.PopupMenuItem(
                content="Checked item",
                checked=False,
            ),
        ],
    )

    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.controls = [pb]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    # normal state
    flet_app.assert_screenshot(
        "popup_menu_button_0",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # open state
    await flet_app.tester.tap(await flet_app.tester.find_by_key("pb"))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "popup_menu_button_1",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
