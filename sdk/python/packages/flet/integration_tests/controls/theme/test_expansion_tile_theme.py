import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_expansion_tile_theme(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme = ft.Theme(
        expansion_tile_theme=ft.ExpansionTileTheme(
            bgcolor=ft.Colors.GREEN_200,
            icon_color=ft.Colors.PINK,
            text_color=ft.Colors.ORANGE,
            collapsed_bgcolor=ft.Colors.YELLOW,
            collapsed_icon_color=ft.Colors.BLUE,
            collapsed_text_color=ft.Colors.PURPLE,
            tile_padding=ft.Padding.all(10),
            controls_padding=ft.Padding(bottom=100),
            expanded_alignment=ft.Alignment.BOTTOM_RIGHT,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )
    )

    et = ft.ExpansionTile(
        key="et",
        title="ExpansionTile Title",
        subtitle="ExpansionTile Subtitle",
        # leading=ft.Icons.UMBRELLA,
        trailing=ft.Icons.SUNNY,
        controls=[
            ft.Text("ExpansionTile Content"),
            ft.Text("More Content"),
        ],
        controls_padding=ft.Padding.all(10),
        tile_padding=ft.Padding.all(20),
        affinity=ft.TileAffinity.LEADING,
    )

    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.add(et)
    await flet_app.tester.pump_and_settle()

    # normal state
    flet_app.assert_screenshot(
        "collapsed",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # open state
    await flet_app.tester.tap(await flet_app.tester.find_by_key("et"))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "expanded",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
