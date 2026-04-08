import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.material.app_bar.actions_and_popup_menu import (
    main as actions_and_popup_menu,
)


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.AppBar(
            leading=ft.Icon(ft.Icons.MENU),
            title=ft.Text("Dashboard"),
            actions=[
                ft.IconButton(ft.Icons.SEARCH),
                ft.IconButton(ft.Icons.MORE_VERT),
            ],
            bgcolor=ft.Colors.SURFACE_CONTAINER,
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": actions_and_popup_menu.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(350, 300)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "before_click",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    button = await flet_app_function.tester.find_by_key("popup")
    await flet_app_function.tester.tap(button)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "after_click",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    flet_app_function.create_gif(
        ["before_click", "after_click"],
        "app_bar_flow",
        duration=2000,
    )
