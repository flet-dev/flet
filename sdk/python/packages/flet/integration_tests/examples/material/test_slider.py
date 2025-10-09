import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.slider import (
    custom_label,
    basic,
    handling_events,
    random_values,
)


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Column(
            [
                ft.Slider(label="Defualt Slider"),
                ft.Slider(label="Disabled Slider", disabled=True),
            ]
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "basic",
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": custom_label.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_custom_label(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "custom_label",
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": handling_events.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_handling_events(flet_app_function: ftt.FletTestApp):
    scr = await flet_app_function.wrap_page_controls_in_screenshot()
    button = await flet_app_function.tester.find_by_key("slider")
    await flet_app_function.tester.tap(button)

    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "handling_events",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
