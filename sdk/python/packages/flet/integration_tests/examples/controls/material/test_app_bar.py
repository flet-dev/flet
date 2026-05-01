import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.material.app_bar.actions_and_popup_menu import (
    main as actions_and_popup_menu,
)
from examples.controls.material.app_bar.theme_mode_toggle import (
    main as theme_mode_toggle,
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
async def test_actions_and_popup_menu(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(450, 300)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "before_click",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    button = await flet_app_function.tester.find_by_key("popup")
    await flet_app_function.tester.mouse_hover(button)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "hover_popup",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    await flet_app_function.tester.tap(button)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "popup_open",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    checked_item = await flet_app_function.tester.find_by_text("Checked item")
    await flet_app_function.tester.mouse_hover(checked_item)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "hover_checked_item",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    await flet_app_function.tester.tap(checked_item)
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.tester.tap(button)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "checked_item_reopened",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    flet_app_function.create_gif(
        [
            "before_click",
            "hover_popup",
            "popup_open",
            "hover_checked_item",
            "checked_item_reopened",
        ],
        "app_bar_flow",
        duration=1000,
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": theme_mode_toggle.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_theme_mode_toggle(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(450, 450)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "theme_mode_before_click",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    toggle_button = await flet_app_function.tester.find_by_key("theme_mode_toggle")
    await flet_app_function.tester.mouse_hover(toggle_button)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "theme_mode_hover",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    await flet_app_function.tester.tap(toggle_button)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "theme_mode_after_click",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    flet_app_function.create_gif(
        [
            "theme_mode_before_click",
            "theme_mode_hover",
            "theme_mode_after_click",
        ],
        "theme_mode_toggle_flow",
        duration=1000,
    )
