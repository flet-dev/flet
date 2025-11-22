import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_end_position(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(400, 500)
    flet_app.page.end_drawer = ft.NavigationDrawer(
        controls=[
            ft.NavigationDrawerDestination(
                icon=ft.Icons.ADD_TO_HOME_SCREEN_SHARP,
                label="Item 1",
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.ADD_COMMENT),
                label="Item 2",
            ),
        ],
    )
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    await flet_app.page.show_end_drawer()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        request.node.name,
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_start_position(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(400, 500)
    flet_app.page.drawer = ft.NavigationDrawer(
        controls=[
            ft.NavigationDrawerDestination(
                icon=ft.Icons.ADD_TO_HOME_SCREEN_SHARP,
                label="Item 1",
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.ADD_COMMENT),
                label="Item 2",
            ),
        ],
    )
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    await flet_app.page.show_drawer()
    await flet_app.tester.pump_and_settle()

    # normal state
    flet_app.assert_screenshot(
        request.node.name,
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_theme(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(400, 500)
    flet_app.page.theme = ft.Theme(
        navigation_drawer_theme=ft.NavigationDrawerTheme(
            bgcolor=ft.Colors.BLUE_GREY_200,
            elevation=20,
            shadow_color=ft.Colors.RED,
            indicator_color=ft.Colors.ORANGE,
            indicator_shape=ft.RoundedRectangleBorder(
                radius=ft.BorderRadius.all(10),
            ),
            indicator_size=ft.Size(200, 50),
            label_text_style=ft.TextStyle(color=ft.Colors.GREEN),
            tile_height=100,
        )
    )
    flet_app.page.drawer = ft.NavigationDrawer(
        controls=[
            ft.NavigationDrawerDestination(
                icon=ft.Icons.ADD_TO_HOME_SCREEN_SHARP,
                label="Item 1",
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.ADD_COMMENT),
                label="Item 2",
            ),
        ],
    )
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    await flet_app.page.show_drawer()
    await flet_app.tester.pump_and_settle()

    # normal state
    flet_app.assert_screenshot(
        request.node.name,
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_with_appbar(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(400, 500)

    flet_app.page.appbar = ft.AppBar(title="AppBar")
    flet_app.page.drawer = ft.NavigationDrawer(
        controls=[
            ft.NavigationDrawerDestination(
                icon=ft.Icons.ADD_TO_HOME_SCREEN_SHARP,
                label="Item 1",
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.ADD_COMMENT),
                label="Item 2",
            ),
        ],
    )
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    await flet_app.page.show_drawer()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        request.node.name,
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_with_cupertino_appbar(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(400, 500)

    flet_app.page.appbar = ft.CupertinoAppBar(title="CupertinoAppBar")
    flet_app.page.drawer = ft.NavigationDrawer(
        controls=[
            ft.NavigationDrawerDestination(
                icon=ft.Icons.ADD_TO_HOME_SCREEN_SHARP,
                label="Item 1",
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.Icons.ADD_COMMENT),
                label="Item 2",
            ),
        ],
    )
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    await flet_app.page.show_drawer()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        request.node.name,
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
