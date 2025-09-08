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
        ft.ListTile("List Tile"),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_properties1(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            [
                ft.ListTile(
                    "List Tile with custom shape",
                    subtitle="Subtitle",
                    leading=ft.Icon(ft.Icons.STAR),
                    trailing=ft.Icon(ft.Icons.ARROW_FORWARD),
                    bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
                    shape=ft.RoundedRectangleBorder(
                        radius=10, side=ft.BorderSide(color=ft.Colors.RED, width=2.0)
                    ),
                ),
                ft.ListTile(
                    "Dense List Tile",
                    subtitle="Subtitle",
                    leading=ft.Icon(ft.Icons.STAR),
                    trailing=ft.Icon(ft.Icons.ARROW_FORWARD),
                    bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
                    dense=True,
                ),
                ft.ListTile(
                    "List Tile with Content Padding",
                    subtitle="Subtitle",
                    leading=ft.Icon(ft.Icons.STAR),
                    trailing=ft.Icon(ft.Icons.ARROW_FORWARD),
                    bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
                    content_padding=ft.Padding.all(20),
                ),
                ft.ListTile(
                    "List Tile with autofocus",
                    subtitle="Subtitle",
                    leading=ft.Icon(ft.Icons.STAR),
                    trailing=ft.Icon(ft.Icons.ARROW_FORWARD),
                    bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
                    autofocus=True,
                ),
                ft.ListTile(
                    "Disabled List Tile",
                    subtitle="Subtitle",
                    leading=ft.Icon(ft.Icons.STAR),
                    trailing=ft.Icon(ft.Icons.ARROW_FORWARD),
                    bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
                    disabled=True,
                ),
                ft.ListTile(
                    "Selected List Tile",
                    subtitle="Subtitle",
                    leading=ft.Icon(ft.Icons.STAR),
                    trailing=ft.Icon(ft.Icons.ARROW_FORWARD),
                    bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
                    selected=True,
                    selected_color=ft.Colors.PINK_200,
                    selected_tile_color=ft.Colors.PURPLE_200,
                ),
                ft.ListTile(
                    "Drawer style List Tile",
                    subtitle="Subtitle",
                    leading=ft.Icon(ft.Icons.STAR),
                    trailing=ft.Icon(ft.Icons.ARROW_FORWARD),
                    bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
                    style=ft.ListTileStyle.DRAWER,
                ),
            ]
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_properties2(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600

    lt = ft.ListTile(
        key="lt",
        title="List Tile",
        subtitle="Subtitle",
        is_three_line=True,
        leading=ft.Icon(ft.Icons.STAR),
        trailing=ft.Icon(ft.Icons.ARROW_FORWARD),
        content_padding=ft.Padding.all(20),
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
        bgcolor_activated=ft.Colors.GREEN_200,
        hover_color=ft.Colors.YELLOW_200,
        selected_color=ft.Colors.PINK_200,
        selected_tile_color=ft.Colors.PURPLE_200,
        selected=False,
        toggle_inputs=True,
        style=ft.ListTileStyle.DRAWER,
        shape=ft.RoundedRectangleBorder(radius=10),
    )

    flet_app.page.add(lt)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "properties_2_normal",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # test hover
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    tile = await flet_app.tester.find_by_key("lt")
    assert tile.count == 1
    await flet_app.tester.mouse_hover(tile)
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "properties_2_hover",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
