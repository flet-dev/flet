import math

import flet as ft
import flet.canvas as fc
import flet.testing as ftt
import pytest


@pytest.mark.asyncio(loop_scope="module")
async def test_drop(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    colors = [ft.Colors.RED, ft.Colors.BLUE, ft.Colors.GREEN]
    dd = ft.Dropdown(
        label="Color",
        options=[
            ft.DropdownOption(
                key=color.value, content=ft.Text(value=color.value, color=color)
            )
            for color in colors
        ],
        key="dd",
    )
    flet_app.page.add(dd)
    await flet_app.tester.pump_and_settle()
    await flet_app.tester.tap(await flet_app.tester.find_by_key("dd"))
    await flet_app.tester.pump_and_settle()
    await flet_app.assert_control_screenshot(request.node.name, dd)
