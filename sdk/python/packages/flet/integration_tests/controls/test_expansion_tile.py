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
        request.node.name, ft.ExpansionTile("ExpansionTile Title")
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_expanded(flet_app: ftt.FletTestApp, request):
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
    flet_app.page.controls = [et]
    flet_app.page.update()
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
