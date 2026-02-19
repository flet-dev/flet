import pytest

import flet as ft
import flet_charts as fch
import flet.testing as ftt
from examples.controls.charts.candlestick_chart import example_1


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        fch.CandlestickChart(
            min_x=-1,
            max_x=2,
            min_y=20,
            max_y=30,
            bgcolor=ft.Colors.AMBER_200,
            spots=[
                fch.CandlestickChartSpot(
                    x=0,
                    open=22.6,
                    high=28.3,
                    low=21.4,
                    close=24.1,
                ),
                fch.CandlestickChartSpot(
                    x=1,
                    open=25.4,
                    high=27.6,
                    low=22.3,
                    close=23.9,
                ),
            ],
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
