import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.BottomAppBar(
            bgcolor=ft.Colors.BLUE,
            shape=ft.CircularRectangleNotchShape(),
            content=ft.Row(
                controls=[
                    ft.IconButton(icon=ft.Icons.MENU, icon_color=ft.Colors.WHITE),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.SEARCH, icon_color=ft.Colors.WHITE),
                    ft.IconButton(icon=ft.Icons.FAVORITE, icon_color=ft.Colors.WHITE),
                ]
            ),
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_notch_with_margin(flet_app_function: ftt.FletTestApp):
    """The notch stays centered under a docked FAB when the bar has margins."""
    page = flet_app_function.page
    page.enable_screenshots = True
    flet_app_function.resize_page(240, 160)
    page.bgcolor = ft.Colors.BLUE_GREY_200
    page.bottom_appbar = ft.BottomAppBar(
        bgcolor=ft.Colors.WHITE,
        shape=ft.CircularRectangleNotchShape(),
        border_radius=36,
        margin=ft.Margin.only(left=40, top=16, right=40, bottom=24),
        height=70,
    )
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        shape=ft.CircleBorder(),
        bgcolor=ft.Colors.TEAL_700,
        foreground_color=ft.Colors.WHITE,
    )
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED
    page.update()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "notch_with_margin",
        await page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
