import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_explicitly_sized(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Pagelet(
            width=400,
            height=400,
            appbar=ft.AppBar(
                title=ft.Text("Pagelet AppBar Title"),
                bgcolor=ft.Colors.AMBER_ACCENT,
            ),
            bottom_appbar=ft.BottomAppBar(
                content=ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.Icons.MENU, icon_color=ft.Colors.WHITE),
                        ft.Container(expand=True),
                        ft.IconButton(icon=ft.Icons.SEARCH, icon_color=ft.Colors.WHITE),
                        ft.IconButton(
                            icon=ft.Icons.FAVORITE, icon_color=ft.Colors.WHITE
                        ),
                    ]
                ),
            ),
            content=ft.Container(
                bgcolor=ft.Colors.AMBER, content=ft.Text("Pagelet Content")
            ),
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_auto_size(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(500, 500)
    flet_app.page.add(
        ft.Pagelet(
            content=ft.Container(
                bgcolor=ft.Colors.AMBER, content=ft.Text("Pagelet Content")
            ),
        ),
    )
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        f"{request.node.name}_1",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    flet_app.page.controls = [
        ft.Pagelet(
            height=400,
            appbar=ft.AppBar(
                title=ft.Text("Pagelet AppBar Title"),
                bgcolor=ft.Colors.AMBER_ACCENT,
            ),
            bottom_appbar=ft.BottomAppBar(
                content=ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.Icons.MENU, icon_color=ft.Colors.WHITE),
                        ft.Container(expand=True),
                        ft.IconButton(icon=ft.Icons.SEARCH, icon_color=ft.Colors.WHITE),
                        ft.IconButton(
                            icon=ft.Icons.FAVORITE, icon_color=ft.Colors.WHITE
                        ),
                    ]
                ),
            ),
            content=ft.Container(
                bgcolor=ft.Colors.AMBER, content=ft.Text("Pagelet Content")
            ),
        ),
    ]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        f"{request.node.name}_2",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
