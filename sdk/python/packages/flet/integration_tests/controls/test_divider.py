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
        ft.Divider(),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_properties(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Divider(
            color=ft.Colors.RED,
            height=50,
            thickness=2,
            leading_indent=20,
            trailing_indent=20,
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_theme(flet_app: ftt.FletTestApp):
    flet_app.page.theme = ft.Theme(
        divider_theme=ft.DividerTheme(
            color=ft.Colors.GREEN,
            thickness=5,
            space=100,
            leading_indent=20,
            trailing_indent=20,
        ),
    )
    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600

    scr_1 = ft.Screenshot(ft.Divider())
    flet_app.page.add(scr_1)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "theme_1",
        await scr_1.capture(pixel_ratio=flet_app.screenshots_pixel_ratio),
    )
