import inspect
import os

import pytest

import examples.extensions.charts.matplotlib_chart.bar_chart.main as bar_chart
import examples.extensions.charts.matplotlib_chart.handle_events.main as handle_events
import examples.extensions.charts.matplotlib_chart.three_d.main as three_d
import examples.extensions.charts.matplotlib_chart.toolbar.main as toolbar
import flet as ft
import flet.testing as ftt

PIXEL_RATIO = float(os.getenv("FLET_TEST_SCREENSHOTS_PIXEL_RATIO", "2.0"))


def at_screenshot_pixel_ratio(main):
    """
    Wraps an example's `main` so its chart draws at the screenshot pixel ratio.

    `MatplotlibChart` renders its figure at the device pixel ratio of the
    display, so on a 1x display the figure has half the resolution of the
    goldens.
    """

    async def wrapper(page: ft.Page):
        page.media.device_pixel_ratio = PIXEL_RATIO
        if inspect.iscoroutinefunction(main):
            await main(page)
        else:
            main(page)

    return wrapper


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": at_screenshot_pixel_ratio(bar_chart.main)}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_bar_chart(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "bar_chart",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": at_screenshot_pixel_ratio(handle_events.main)}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_handle_events(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "handle_events",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": at_screenshot_pixel_ratio(toolbar.main)}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_toolbar(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "toolbar",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": at_screenshot_pixel_ratio(three_d.main)}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_three_d(flet_app_function: ftt.FletTestApp):
    # Full-page screenshot, like the sibling tests: the controls-capture
    # path measures intrinsic dimensions, which the LayoutBuilder-based
    # matplotlib canvas cannot provide.
    flet_app_function.page.enable_screenshots = True
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "three_d",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
