import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_cupertino_radio(flet_app: ftt.FletTestApp, request):
    group = ft.RadioGroup(
        content=ft.Column(
            controls=[
                ft.CupertinoRadio(
                    value="red",
                    label="Red",
                    active_color=ft.Colors.RED_600,
                    inactive_color=ft.Colors.RED_200,
                    key="red",
                ),
                ft.CupertinoRadio(
                    value="green",
                    label="Green",
                    fill_color=ft.Colors.GREEN,
                    key="green",
                ),
                ft.CupertinoRadio(
                    value="blue",
                    label="Blue",
                    active_color=ft.Colors.BLUE,
                    key="blue",
                ),
            ]
        )
    )

    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.controls = [group]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    # red chosen
    await flet_app.tester.tap(await flet_app.tester.find_by_text("Red"))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "red",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # green chosen
    await flet_app.tester.tap(await flet_app.tester.find_by_text("Green"))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "green",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # blue chosen
    await flet_app.tester.tap(await flet_app.tester.find_by_text("Blue"))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "blue",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
