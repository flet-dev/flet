import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name, ft.ExpansionTile("ExpansionTile Title")
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_properties1(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.ExpansionTile(
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
        ),
    )
