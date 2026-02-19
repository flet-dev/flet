import pytest

import flet as ft
import flet_charts as fch
import flet.testing as ftt
from examples.controls.charts.matplotlib_chart import (
    bar_chart,
    handle_events,
    toolbar,
    three_d,
)


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
        await flet_app_function.page.take_screenshot(),
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
        await flet_app_function.page.take_screenshot(),
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
        await flet_app_function.page.take_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": three_d.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_three_d(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "three_d",
        await flet_app_function.take_page_controls_screenshot(),
    )
