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
    await flet_app.resize_page(400, 600)
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.ExpansionTile(
            title="ExpansionTile Title",
            subtitle="ExpansionTile Subtitle",
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_expanded(flet_app: ftt.FletTestApp, request):
    await flet_app.resize_page(400, 600)
    flet_app.page.add(
        tile := ft.ExpansionTile(
            key="tile",
            expanded=False,
            title="ExpansionTile Title",
            subtitle="ExpansionTile Subtitle",
            trailing=ft.Icons.SUNNY,
            controls_padding=ft.Padding.all(10),
            tile_padding=ft.Padding.all(20),
            affinity=ft.TileAffinity.LEADING,
            controls=[
                ft.Text("ExpansionTile Content"),
                ft.Text("More Content"),
            ],
        )
    )
    await flet_app.tester.pump_and_settle()

    # collapsed state
    assert tile.expanded is False
    await flet_app.assert_control_screenshot("collapsed", tile)

    # tap/click on the tile to expand
    await flet_app.tester.tap(await flet_app.tester.find_by_key("tile"))
    await flet_app.tester.pump_and_settle()

    # expanded state
    assert tile.expanded is True
    await flet_app.assert_control_screenshot("expanded", tile)

    # collapse programatically
    tile.expanded = False
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    # collapsed state
    await flet_app.assert_control_screenshot("collapsed", tile)
