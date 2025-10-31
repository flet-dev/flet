import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_programmatic_open(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    await flet_app.resize_page(250, 250)
    flet_app.page.add(
        menu := ft.ContextMenu(
            content=ft.IconButton(ft.Icons.MENU),
            items=[
                ft.PopupMenuItem("Item 1"),
                ft.PopupMenuItem("Item 2"),
                ft.PopupMenuItem("Item 3"),
            ],
        )
    )
    await flet_app.tester.pump_and_settle()

    await menu.open()
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "programmatic_open_1",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "programmatic_open_2",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
