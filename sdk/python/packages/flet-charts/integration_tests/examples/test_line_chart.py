import pytest

import flet as ft
import flet_charts as fch
import flet.testing as ftt
from examples.controls.charts.line_chart import example_1, example_2


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        fch.LineChart(
            data_series=[
                fch.LineChartData(
                    color=ft.Colors.BLUE_GREY_500,
                    curved=True,
                    points=[
                        fch.LineChartDataPoint(1, 0.5),
                        fch.LineChartDataPoint(2, 1.5),
                        fch.LineChartDataPoint(3, 1),
                    ],
                ),
                fch.LineChartData(
                    color=ft.Colors.AMBER_400,
                    curved=True,
                    points=[
                        fch.LineChartDataPoint(1, 2),
                        fch.LineChartDataPoint(2, 0.5),
                        fch.LineChartDataPoint(3, 1.5),
                    ],
                ),
            ],
            min_y=0,
            max_y=3,
            min_x=0,
            max_x=5,
        ),
    )


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
