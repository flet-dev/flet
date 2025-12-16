import pytest

import flet as ft
import flet_charts as fch
import flet.testing as ftt
from examples.controls.charts.bar_chart import example_1, example_2


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        fch.BarChart(
            # expand=True,
            border=ft.Border.all(1, ft.Colors.GREY_400),
            groups=[
                fch.BarChartGroup(
                    x=0,
                    rods=[
                        fch.BarChartRod(
                            from_y=0,
                            to_y=40,
                            color=ft.Colors.BLUE_GREY_200,
                        ),
                    ],
                ),
                fch.BarChartGroup(
                    x=1,
                    rods=[
                        fch.BarChartRod(
                            from_y=0,
                            to_y=60,
                            color=ft.Colors.BLUE_GREY_600,
                        ),
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
