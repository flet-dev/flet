import pytest

import flet as ft
import flet_charts as fch
import flet.testing as ftt
from examples.controls.charts.plotly_chart import (
    example_1,
    example_2,
    example_3,
    example_4,
)


@pytest.mark.skip(reason="poltly control temporarily out of service")
@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": example_1.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_example_1(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "example_1",
        await flet_app_function.page.take_screenshot(),
    )


@pytest.mark.skip(reason="poltly control temporarily out of service")
@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": example_2.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_example_2(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "example_2",
        await flet_app_function.page.take_screenshot(),
    )


@pytest.mark.skip(reason="poltly control temporarily out of service")
@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": example_3.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_example_3(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "example_3",
        await flet_app_function.page.take_screenshot(),
    )


@pytest.mark.skip(reason="poltly control temporarily out of service")
@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": example_4.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_example_4(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "example_4",
        await flet_app_function.page.take_screenshot(),
    )
