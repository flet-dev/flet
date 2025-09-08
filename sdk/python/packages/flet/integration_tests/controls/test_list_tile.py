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
        ft.ListTile(
            "List Tile",
            subtitle="Subtitle",
            leading=ft.Icon(ft.Icons.STAR),
            trailing=ft.Icon(ft.Icons.ARROW_FORWARD),
            bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_selected(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.ListTile(
            "List Tile",
            subtitle="Subtitle",
            leading=ft.Icon(ft.Icons.STAR),
            trailing=ft.Icon(ft.Icons.ARROW_FORWARD),
            bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
            selected=True,
            selected_color=ft.Colors.PINK_200,
            selected_tile_color=ft.Colors.PURPLE_200,
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
        selected=True,
        dense=True,
        toggle_inputs=True,
        style=ft.ListTileStyle.DRAWER,
        shape=ft.RoundedRectangleBorder(radius=10),
    )

    flet_app.page.add(lt)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "theme1",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # test focus color
    lt.autofocus = True
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "focus",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # test disabled
    lt.autofocus = False
    lt.disabled = True
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "disabled",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # test hover
    lt.disabled = False
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    tile = await flet_app.tester.find_by_key("lt")
    assert tile.count == 1
    await flet_app.tester.mouse_hover(tile)
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "hover",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
