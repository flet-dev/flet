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
        title="List Tile without three line",
        subtitle="Long Long Long Long Long Long Long Long Long Long Long "
        "Long Long Long Long Long Long Long Long Long Long Long"
        "Long Subtitle with is_three_line = False",
        # is_three_line=True,
        leading=ft.Icon(ft.Icons.STAR),
        trailing=ft.Icon(ft.Icons.ARROW_FORWARD),
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
        splash_color=ft.Colors.GREEN_200,  # is not shown on screenshot
        hover_color=ft.Colors.YELLOW_200,
    )

    lt1 = ft.ListTile(
        title="List Tile with three line",
        subtitle="Long Long Long Long Long Long Long Long Long Long Long "
        "Long Long Long Long Long Long Long Long Long Long Long"
        "Long Subtitle with is_three_line = True",
        is_three_line=True,  # not sure if this behaviour is correct or not.
        # Tested it in flutter, it also shows more than 3 lines
        leading=ft.Icon(ft.Icons.STAR),
        trailing=ft.Icon(ft.Icons.ARROW_FORWARD),
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
        splash_color=ft.Colors.GREEN_200,  # is not shown on screenshot
        hover_color=ft.Colors.YELLOW_200,
    )

    lt2 = ft.ListTile(
        title="List Tile with Compact visual density",
        subtitle="Long Long Long Long Long Long Long Long Long Long Long "
        "Long Long Long Long Long Long Long Long Long Long Long"
        "Long Subtitle with is_three_line = False",
        leading=ft.Icon(ft.Icons.STAR),
        trailing=ft.Icon(ft.Icons.ARROW_FORWARD),
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
        visual_density=ft.VisualDensity.COMPACT,
    )

    lt3 = ft.ListTile(
        title="List Tile with horizontal spacing",
        subtitle="Subtitle",
        leading=ft.Icon(ft.Icons.STAR),
        trailing=ft.Icon(ft.Icons.ARROW_FORWARD),
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
        splash_color=ft.Colors.GREEN_200,  # is not shown on screenshot
        hover_color=ft.Colors.YELLOW_200,
        horizontal_spacing=50,
        title_alignment=ft.ListTileTitleAlignment.THREE_LINE,  # default value
    )

    lt4 = ft.ListTile(
        title="List Tile with minimum leading width",
        subtitle="Top Title Alignment",
        is_three_line=True,
        leading=ft.Icon(ft.Icons.STAR),
        trailing=ft.Icon(ft.Icons.ARROW_FORWARD),
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
        splash_color=ft.Colors.GREEN_200,  # is not shown on screenshot
        hover_color=ft.Colors.YELLOW_200,
        min_leading_width=100,
        title_alignment=ft.ListTileTitleAlignment.TOP,  # default value
    )

    lt5 = ft.ListTile(
        title="List Tile with minimum vertical padding",
        subtitle="Center Title Alignment",
        leading=ft.Icon(ft.Icons.STAR),
        trailing=ft.Icon(ft.Icons.ARROW_FORWARD),
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
        splash_color=ft.Colors.GREEN_200,  # is not shown on screenshot
        hover_color=ft.Colors.YELLOW_200,
        min_vertical_padding=30,
        title_alignment=ft.ListTileTitleAlignment.CENTER,
    )

    lt6 = ft.ListTile(
        title="List Tile with icon color and text color and styles",
        subtitle="Bottom Title Alignment",
        icon_color=ft.Colors.RED,
        text_color=ft.Colors.PURPLE,
        title_text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD),
        subtitle_text_style=ft.TextStyle(size=10, italic=True),
        leading=ft.Icon(ft.Icons.STAR),
        trailing=ft.Icon(ft.Icons.ARROW_FORWARD),
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
        title_alignment=ft.ListTileTitleAlignment.BOTTOM,
    )

    lt7 = ft.ListTile(
        title="List Tile with leading and trailing text style",
        subtitle="Title Height Title Alignment",
        icon_color=ft.Colors.RED,
        leading=ft.Text("Leading"),
        trailing=ft.Text("Trailing"),
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
        title_alignment=ft.ListTileTitleAlignment.TITLE_HEIGHT,
    )

    lt8 = ft.ListTile(
        title="List Tile with minimum height",
        subtitle="Title Height Title Alignment",
        icon_color=ft.Colors.RED,
        leading=ft.Text("Leading"),
        trailing=ft.Text("Trailing"),
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
        min_height=150,
    )

    flet_app.page.add(lt, lt1, lt2, lt3, lt4, lt5, lt6, lt7, lt8)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "properties_2_normal",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # test hover
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


@pytest.mark.asyncio(loop_scope="function")
async def test_toggle_inputs(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600

    lt = ft.ListTile(
        key="lt",
        title="ListTileStyle with toggle inputs",
        subtitle="List",
        leading=ft.Icon(ft.Icons.STAR),
        trailing=ft.Checkbox(),
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
        style=ft.ListTileStyle.LIST,
        toggle_inputs=True,
    )

    flet_app.page.add(lt)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "toggle_initial",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # test click1
    tile = await flet_app.tester.find_by_key("lt")
    assert tile.count == 1
    await flet_app.tester.tap(tile)
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "toggle_click1",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # test click2 - issue #5627
    # await flet_app.tester.tap(tile)
    # await flet_app.tester.pump_and_settle()

    # flet_app.assert_screenshot(
    #     "toggle_click2",
    #     await flet_app.page.take_screenshot(
    #         pixel_ratio=flet_app.screenshots_pixel_ratio
    #     ),
    # )
