import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
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


async def _assert_page_screenshot(flet_app: ftt.FletTestApp, name: str):
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        name,
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )


def _page_with_docked_fab(flet_app: ftt.FletTestApp) -> ft.Page:
    # A small window keeps the bar large in the screenshot, so a misplaced
    # notch drops similarity below the threshold.
    page = flet_app.page
    page.enable_screenshots = True
    flet_app.resize_page(240, 160)
    page.bgcolor = ft.Colors.BLUE_GREY_200
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        shape=ft.CircleBorder(),
        bgcolor=ft.Colors.TEAL_700,
        foreground_color=ft.Colors.WHITE,
    )
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED
    return page


@pytest.mark.asyncio(loop_scope="function")
async def test_notch_with_margin(flet_app: ftt.FletTestApp):
    """The notch stays centered under a docked FAB when the bar has margins."""
    page = _page_with_docked_fab(flet_app)
    page.bottom_appbar = ft.BottomAppBar(
        bgcolor=ft.Colors.WHITE,
        shape=ft.CircularRectangleNotchShape(),
        border_radius=36,
        margin=ft.Margin.only(left=40, top=16, right=40, bottom=24),
        height=70,
    )
    await _assert_page_screenshot(flet_app, "notch_with_margin")


@pytest.mark.asyncio(loop_scope="function")
async def test_theme_notch_with_margin(flet_app: ftt.FletTestApp):
    """A notch shape and color from the page theme apply, centered with margins."""
    page = _page_with_docked_fab(flet_app)
    page.theme = ft.Theme(
        bottom_appbar_theme=ft.BottomAppBarTheme(
            bgcolor=ft.Colors.ORANGE_300,
            shape=ft.CircularRectangleNotchShape(),
        )
    )
    page.bottom_appbar = ft.BottomAppBar(
        border_radius=36,
        margin=ft.Margin.only(left=40, top=16, right=40, bottom=24),
        height=70,
    )
    await _assert_page_screenshot(flet_app, "theme_notch_with_margin")
