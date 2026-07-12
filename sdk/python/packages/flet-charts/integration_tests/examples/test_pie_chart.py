import pytest
from example_apps import load_example

import flet.testing as ftt

example_1 = load_example("pie_chart/pie_chart_with_hover_borders")
example_2 = load_example("pie_chart/pie_chart_with_hover_sections")
example_3 = load_example("pie_chart/pie_chart_with_icon_badges")


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
