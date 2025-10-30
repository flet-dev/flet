import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.context_menu import manual_open


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.add(
        menu := ft.ContextMenu(
            items=[
                ft.PopupMenuItem(content="Rename"),
                ft.PopupMenuItem(content="Duplicate"),
            ],
            content=ft.IconButton(icon=ft.Icons.MENU),
        )
    )

    await menu.open()
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.assert_control_screenshot(
        request.node.name,
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": manual_open.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_manual_open(flet_app_function: ftt.FletTestApp, request):
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Open Menu")
    )
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "manual_open",
        await flet_app_function.take_page_controls_screenshot(),
    )
