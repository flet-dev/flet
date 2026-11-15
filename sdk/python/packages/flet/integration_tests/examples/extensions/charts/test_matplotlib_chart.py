import pytest

import examples.extensions.charts.matplotlib_chart.bar_chart.main as bar_chart
import examples.extensions.charts.matplotlib_chart.handle_events.main as handle_events
import examples.extensions.charts.matplotlib_chart.three_d.main as three_d
import examples.extensions.charts.matplotlib_chart.toolbar.main as toolbar
import flet.testing as ftt


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": bar_chart.main}],
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
    [{"flet_app_main": handle_events.main}],
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
    [{"flet_app_main": toolbar.main}],
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
    [{"flet_app_main": three_d.main}],
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
