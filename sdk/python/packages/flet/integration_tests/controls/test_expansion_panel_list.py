import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_expansion_panel_list_basic(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.ExpansionPanelList(
            controls=[ft.ExpansionPanel(ft.Text("Expansion Panel"))],
        ),
    )
