import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_dismissible_basic(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Dismissible(ft.Text("Dismissible Item")),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_dismissible_properties(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Dismissible(
            content=ft.ListTile(title="Item 1"),
            dismiss_direction=ft.DismissDirection.HORIZONTAL,
            background=ft.Container(bgcolor=ft.Colors.GREEN),
            secondary_background=ft.Container(bgcolor=ft.Colors.RED),
            dismiss_thresholds={
                ft.DismissDirection.END_TO_START: 0.2,
                ft.DismissDirection.START_TO_END: 0.2,
            },
        ),
    )
