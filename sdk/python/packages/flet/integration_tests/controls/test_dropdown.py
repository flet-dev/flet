import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_dropdown_basic(flet_app: ftt.FletTestApp, request):
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
    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.controls = [dd]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    # normal state
    flet_app.assert_screenshot(
        "dropdown_0",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # open state
    await flet_app.tester.tap(await flet_app.tester.find_by_key("dd"))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "dropdown_1",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
