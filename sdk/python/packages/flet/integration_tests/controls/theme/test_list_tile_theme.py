import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_theme(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme = ft.Theme(
        list_tile_theme=ft.ListTileTheme(
            icon_color=ft.Colors.PURPLE,
            text_color=ft.Colors.PINK,
            bgcolor=ft.Colors.LIGHT_GREEN_ACCENT_100,
            selected_tile_color=ft.Colors.LIGHT_GREEN_ACCENT_400,
            selected_color=ft.Colors.GREEN_700,
            is_three_line=True,
            enable_feedback=False,
            dense=True,
            shape=ft.RoundedRectangleBorder(
                radius=10, side=ft.BorderSide(color=ft.Colors.RED, width=2.0)
            ),
            visual_density=ft.VisualDensity.COMFORTABLE,
            content_padding=ft.Padding.symmetric(horizontal=20, vertical=10),
            min_vertical_padding=50,
            horizontal_spacing=30,
            min_leading_width=80,
            title_text_style=ft.TextStyle(
                color=ft.Colors.GREEN, italic=True, weight=ft.FontWeight.BOLD
            ),
            subtitle_text_style=ft.TextStyle(
                color=ft.Colors.GREEN, italic=True, weight=ft.FontWeight.W_200
            ),
            leading_and_trailing_text_style=ft.TextStyle(
                color=ft.Colors.BLUE,
                bgcolor=ft.Colors.GREEN_200,
                italic=True,
                weight=ft.FontWeight.W_200,
            ),
            mouse_cursor=ft.MouseCursor.FORBIDDEN,
            min_height=100,
        )
    )

    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600

    lt1 = ft.ListTile(
        "ListTile with is_three_line = False",
        subtitle="List",
        leading=ft.Icon(ft.Icons.STAR),
        is_three_line=False,
        trailing=ft.Checkbox(),
        # bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
        style=ft.ListTileStyle.LIST,
        toggle_inputs=True,
        visual_density=ft.VisualDensity.COMPACT,
    )
    lt2 = ft.ListTile(
        "ListTile default is_three_line",
        subtitle="List",
        leading=ft.Icon(ft.Icons.STAR),
        # is_three_line=True,
        trailing=ft.Checkbox(),
        selected=True,
        # bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
        style=ft.ListTileStyle.LIST,
        toggle_inputs=False,
    )
    lt3 = ft.ListTile(
        title="ListTile is_three_line = True",
        subtitle="Subtitle",
        is_three_line=True,
        leading=ft.Text("Leading"),
        trailing=ft.Text("Trailing"),
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
        hover_color=ft.Colors.YELLOW_200,
        style=ft.ListTileStyle.DRAWER,
        shape=ft.RoundedRectangleBorder(radius=10),
    )

    flet_app.page.add(lt1, lt2, lt3)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "theme1",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
