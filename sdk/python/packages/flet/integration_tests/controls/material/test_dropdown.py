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
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(350, 300)

    colors = ["red", "blue", "green"]
    flet_app.page.add(
        dd := ft.Dropdown(
            key="dd",
            label="Color",
            text="Select a color",
            options=[
                ft.DropdownOption(key=color, content=ft.Text(value=color, color=color))
                for color in colors
            ],
        )
    )
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

    # select red option
    red_options = await flet_app.tester.find_by_text("red")
    assert red_options.count == 2  # Flutter Finder bug - should be 1
    await flet_app.tester.tap(red_options.last)
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "basic_2",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # clear value
    dd.value = None
    dd.update()
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "basic_0",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_theme(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(350, 300)
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
    flet_app.page.add(
        ft.Dropdown(
            key="dd",
            label="Color",
            text="Select a color",
            options=[
                ft.DropdownOption(key=color.value, content=ft.Text(value=color.value))
                for color in colors
            ],
        )
    )
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
