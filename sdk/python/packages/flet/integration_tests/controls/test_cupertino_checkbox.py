import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_styled_cupertino_checkboxes(flet_app: ftt.FletTestApp, request):
    cbs = ft.Column(
        controls=[
            ft.CupertinoCheckbox(
                label="Cupertino Checkbox tristate",
                value=True,
                tristate=True,
                check_color=ft.Colors.GREY_900,
                fill_color={
                    ft.ControlState.HOVERED: ft.Colors.PINK_200,
                    ft.ControlState.PRESSED: ft.Colors.LIME_ACCENT_200,
                    ft.ControlState.SELECTED: ft.Colors.DEEP_ORANGE_200,
                    ft.ControlState.DEFAULT: ft.Colors.TEAL_200,
                },
                key="tristate",
            ),
            ft.CupertinoCheckbox(
                label="Cupertino Checkbox circle border",
                value=True,
                shape=ft.CircleBorder(),
                key="circleborder",
            ),
            ft.CupertinoCheckbox(
                label="Cupertino Checkbox label position",
                value=True,
                label_position=ft.LabelPosition.LEFT,
                key="labelposition",
            ),
        ]
    )
    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.controls = [cbs]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    # normal state
    flet_app.assert_screenshot(
        "checkboxes_0",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # checked state
    await flet_app.tester.tap(await flet_app.tester.find_by_key("tristate"))
    await flet_app.tester.tap(await flet_app.tester.find_by_key("circleborder"))
    await flet_app.tester.tap(await flet_app.tester.find_by_key("labelposition"))

    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "checkboxes_1",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
