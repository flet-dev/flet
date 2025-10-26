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
    colors = [ft.Colors.RED, ft.Colors.BLUE, ft.Colors.GREEN]
    dd = ft.Dropdown(
        label="Color",
        text="Select a color",
        options=[
            ft.DropdownOption(
                key=color.value, content=ft.Text(value=color.value, color=color)
            )
            for color in colors
        ],
        key="dd",
    )
    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.add(dd)
    await flet_app.tester.pump_and_settle()

    # normal state
    flet_app.assert_screenshot(
        "basic_0",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # open state
    await flet_app.tester.tap(await flet_app.tester.find_by_key("dd"))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "basic_1",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_theme(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme = ft.Theme(
        dropdown_theme=ft.DropdownTheme(
            text_style=ft.TextStyle(color=ft.Colors.PURPLE, size=20),
            menu_style=ft.MenuStyle(
                alignment=ft.Alignment.BOTTOM_CENTER,
                elevation=10,
                bgcolor=ft.Colors.GREEN_300,
            ),
        )
    )
    colors = [ft.Colors.RED, ft.Colors.BLUE, ft.Colors.GREEN]
    dd = ft.Dropdown(
        label="Color",
        text="Select a color",
        options=[
            ft.DropdownOption(key=color.value, content=ft.Text(value=color.value))
            for color in colors
        ],
        key="dd",
    )
    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600

    flet_app.page.add(dd)
    await flet_app.tester.pump_and_settle()

    # normal state
    flet_app.assert_screenshot(
        "theme_0",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # open state
    await flet_app.tester.tap(await flet_app.tester.find_by_key("dd"))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "theme_1",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
