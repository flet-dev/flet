import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_radio(flet_app: ftt.FletTestApp, request):
    group = ft.RadioGroup(
        content=ft.Column(
            controls=[
                ft.Radio(value="one", label="One"),
                ft.Radio(value="two", label="Two"),
                ft.Radio(value="three", label="Three"),
            ]
        )
    )

    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.controls = [group]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    # one chosen
    await flet_app.tester.tap(await flet_app.tester.find_by_text("One"))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "one",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # green chosen
    await flet_app.tester.tap(await flet_app.tester.find_by_text("Two"))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "two",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # blue chosen
    await flet_app.tester.tap(await flet_app.tester.find_by_text("Three"))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "three",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
