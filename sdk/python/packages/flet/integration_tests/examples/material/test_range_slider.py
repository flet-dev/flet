import pytest

import flet as ft
import flet.testing as ftt

from examples.controls.range_slider import basic, handling_change_events


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.RangeSlider(
            min=0,
            max=10,
            start_value=2,
            divisions=10,
            end_value=7,
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(800, 200)
    flet_app_function.page.update()
    await flet_app_function.tester.tap_at(ft.Offset(200, 100))
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "basic1",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    await flet_app_function.tester.tap_at(ft.Offset(700, 100))
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "basic2",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    await flet_app_function.tester.tap_at(ft.Offset(400, 100))
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "basic3",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    flet_app_function.create_gif(
        ["basic1", "basic2", "basic3"],
        "basic",
        duration=1600,
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": handling_change_events.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_handling_change_events(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(800, 200)
    flet_app_function.page.update()
    await flet_app_function.tester.tap_at(ft.Offset(200, 100))
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "handling_events1",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    await flet_app_function.tester.tap_at(ft.Offset(700, 100))
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "handling_events2",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    await flet_app_function.tester.tap_at(ft.Offset(400, 100))
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "handling_events3",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    flet_app_function.create_gif(
        ["handling_events1", "handling_events2", "handling_events3"],
        "handling_events",
        duration=1600,
    )
