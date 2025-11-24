import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.context_menu import programmatic_open


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(250, 200)
    flet_app_function.page.add(
        menu := ft.ContextMenu(
            content=ft.IconButton(ft.Icons.MENU),
            items=[
                ft.PopupMenuItem("Rename"),
                ft.PopupMenuItem("Duplicate"),
            ],
        )
    )
    await flet_app_function.tester.pump_and_settle()

    # open menu
    await menu.open()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        request.node.name,
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": programmatic_open.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_programmatic_open(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(300, 300)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    # click button to open menu
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Click to open menu")
    )
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        test_programmatic_open.__name__,
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
