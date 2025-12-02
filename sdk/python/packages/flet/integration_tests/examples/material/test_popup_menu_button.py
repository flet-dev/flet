import pytest

import flet as ft
import flet.testing as ftt

from examples.controls.popup_menu_button import basic


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(100, 200)
    flet_app_function.page.update()
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.add(
        pmb := ft.PopupMenuButton(
            key="popup",
            items=[
                ft.PopupMenuItem(content="Sm"),
                ft.PopupMenuItem(content="Med"),
                ft.PopupMenuItem(content="Lg"),
            ],
            menu_position=ft.PopupMenuPosition.UNDER,
        )
    )
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    pb = await flet_app_function.tester.find_by_key("popup")
    await flet_app_function.tester.tap(pb)
    await flet_app_function.tester.pump_and_settle()
    # for _ in range(5):
    #     await flet_app_function.tester.pump(100)
    flet_app_function.page.update()
    flet_app_function.assert_screenshot(
        request.node.name,
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio,
        ),
    )


@pytest.mark.skip(reason="Test runs asynchronously")
@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    pb = await flet_app_function.tester.find_by_key("popup")
    await flet_app_function.tester.tap(pb)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "basic",
        await flet_app_function.page.take_screenshot(delay=ft.Duration(seconds=15)),
    )
