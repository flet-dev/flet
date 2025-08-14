import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_cupertino_app_bar(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.CupertinoAppBar(
            leading=ft.Icon(ft.Icons.PALETTE, color=ft.Colors.ON_SECONDARY),
            title=ft.Text("CupertinoAppBar Example"),
            trailing=ft.Icon(ft.Icons.WB_SUNNY_OUTLINED, color=ft.Colors.ON_SECONDARY),
            automatic_background_visibility=False,
            bgcolor=ft.Colors.SECONDARY,
            brightness=ft.Brightness.LIGHT,
        ),
    )
