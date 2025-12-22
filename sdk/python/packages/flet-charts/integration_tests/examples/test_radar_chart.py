import pytest

import flet as ft
import flet_charts as fch
import flet.testing as ftt
from examples.controls.charts.radar_chart import example_1


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.padding = 20
    flet_app_function.page.update()
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        fch.RadarChart(
            # expand=True,
            titles=[
                fch.RadarChartTitle(text="winter", position_percentage_offset=0.1),
                fch.RadarChartTitle(text="spring", position_percentage_offset=0.1),
                fch.RadarChartTitle(text="summer", position_percentage_offset=0.1),
                fch.RadarChartTitle(text="autumn", position_percentage_offset=0.1),
            ],
            radar_shape=fch.RadarShape.CIRCLE,
            data_sets=[
                fch.RadarDataSet(
                    fill_color=ft.Colors.with_opacity(0.2, ft.Colors.BLUE_GREY_700),
                    entries=[
                        fch.RadarDataSetEntry(130),
                        fch.RadarDataSetEntry(95),
                        fch.RadarDataSetEntry(190),
                        fch.RadarDataSetEntry(60),
                    ],
                ),
                fch.RadarDataSet(
                    fill_color=ft.Colors.with_opacity(0.2, ft.Colors.CYAN_400),
                    entries=[
                        fch.RadarDataSetEntry(90),
                        fch.RadarDataSetEntry(45),
                        fch.RadarDataSetEntry(265),
                        fch.RadarDataSetEntry(150),
                    ],
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
