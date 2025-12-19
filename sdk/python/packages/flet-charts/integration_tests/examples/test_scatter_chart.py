import pytest


import flet as ft
import flet_charts as fch
import flet.testing as ftt
from examples.controls.charts.scatter_chart import example_1


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    chart_spots = [
        fch.ScatterChartSpot(
            x=i * 2,
            y=i * 3,
        )
        for i in range(10)
    ]
    chart_spots += [
        fch.ScatterChartSpot(
            x=i,
            y=i,
        )
        for i in range(10)
    ]

    chart_spots += [
        fch.ScatterChartSpot(
            x=i + 2,
            y=i + 10,
        )
        for i in range(10)
    ]

    await flet_app_function.assert_control_screenshot(
        request.node.name,
        fch.ScatterChart(
            # expand=True,
            aspect_ratio=1.0,
            # min_x=0.0,
            # max_x=50.0,
            # min_y=0.0,
            # max_y=50.0,
            # left_axis=fch.ChartAxis(show_labels=False),
            # right_axis=fch.ChartAxis(show_labels=False),
            # top_axis=fch.ChartAxis(show_labels=False),
            # bottom_axis=fch.ChartAxis(show_labels=False),
            # show_tooltips_for_selected_spots_only=False,
            spots=chart_spots,
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
