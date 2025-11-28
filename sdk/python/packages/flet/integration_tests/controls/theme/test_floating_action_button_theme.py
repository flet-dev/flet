import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_theme_1(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme = ft.Theme(
        floating_action_button_theme=ft.FloatingActionButtonTheme(
            bgcolor=ft.Colors.ORANGE,
            hover_color=ft.Colors.GREEN,
            focus_color=ft.Colors.RED,
            foreground_color=ft.Colors.PINK,
            splash_color=ft.Colors.YELLOW,
            shape=ft.RoundedRectangleBorder(
                radius=4, side=ft.BorderSide(color=ft.Colors.BLUE, width=2.0)
            ),
            elevation=20,
            hover_elevation=30,
            focus_elevation=40,
            disabled_elevation=50,
            highlight_elevation=60,
            enable_feedback=True,
            extended_padding=ft.Padding.all(5),
            text_style=ft.TextStyle(italic=True),
            icon_label_spacing=20,
            extended_size_constraints=ft.BoxConstraints(
                min_width=200,
                max_width=200,
                min_height=200,
                max_height=200,
            ),
            size_constraints=ft.BoxConstraints(
                min_width=100,
                max_width=100,
                min_height=100,
                max_height=100,
            ),
        )
    )

    flet_app.page.enable_screenshots = True
    flet_app.resize_page(400, 600)

    fab1 = ft.FloatingActionButton(
        key="fab1",
        content="Add",
        icon=ft.Icons.ADD,
    )
    fab2 = ft.FloatingActionButton(ft.Text("Text", color=ft.Colors.GREEN), mini=True)
    fab3 = ft.FloatingActionButton("Text", disabled=True)
    fab4 = ft.FloatingActionButton("Long Long Long Long Text", disabled=True)
    flet_app.page.add(fab1, fab2, fab3, fab4)
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "theme_1_normal",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # test focus and disabled
    fab2.autofocus = True
    fab3.disabled = True
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "theme_1_focus_disabled",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # test hover
    button = await flet_app.tester.find_by_key("fab1")
    assert button.count == 1
    await flet_app.tester.mouse_hover(button)
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "theme_1_hover",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
