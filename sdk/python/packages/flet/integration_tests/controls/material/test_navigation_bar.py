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
        ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Explore"),
                ft.NavigationBarDestination(icon=ft.Icons.COMMUTE, label="Commute"),
                ft.NavigationBarDestination(
                    icon=ft.Icons.BOOKMARK_BORDER,
                    selected_icon=ft.Icons.BOOKMARK,
                    label="Favorites",
                ),
            ]
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_theme(flet_app: ftt.FletTestApp):
    flet_app.page.theme = ft.Theme(
        navigation_bar_theme=ft.NavigationBarTheme(
            bgcolor=ft.Colors.GREEN_200,
            shadow_color=ft.Colors.ORANGE_500,  # not shows in the screenshot
            elevation=50,  # not shows in the screenshot
            indicator_color=ft.Colors.GREEN,
            overlay_color=ft.Colors.YELLOW_300,
            height=200,
            label_text_style=ft.TextStyle(color=ft.Colors.ORANGE_900, size=20),
            indicator_shape=ft.RoundedRectangleBorder(
                radius=ft.BorderRadius.all(10),
                side=ft.BorderSide(color=ft.Colors.PURPLE, width=3),
            ),
            label_behavior=ft.NavigationBarLabelBehavior.ONLY_SHOW_SELECTED,
            label_padding=ft.Padding.all(20),
        )
    )

    flet_app.page.enable_screenshots = True
    await flet_app.resize_page(400, 600)

    scr_1 = ft.Screenshot(
        ft.NavigationBar(
            key="nb",
            elevation=100,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Explore"),
                ft.NavigationBarDestination(key="add", icon=ft.Icon(ft.Icons.ADD)),
                ft.NavigationBarDestination(
                    icon=ft.Icons.PHONE_ENABLED,
                    label="Explore",
                ),
            ],
        )
    )
    flet_app.page.add(scr_1)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "theme_1",
        await scr_1.capture(pixel_ratio=flet_app.screenshots_pixel_ratio),
    )

    # hover to check overlay color
    add = await flet_app.tester.find_by_key("add")
    assert add.count == 1
    await flet_app.tester.mouse_hover(add)
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "theme_2",
        await scr_1.capture(pixel_ratio=flet_app.screenshots_pixel_ratio),
    )

    # click to check label behaviour
    await flet_app.tester.tap(add)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "theme_3",
        await scr_1.capture(pixel_ratio=flet_app.screenshots_pixel_ratio),
    )
