import flet as ft
import flet.testing as ftt
import pytest


@pytest.mark.asyncio(loop_scope="module")
async def test_cupertino_action_sheet_action_basic(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.CupertinoActionSheetAction("Click me"),
    )