import pytest
from example_apps import load_example

import flet as ft
import flet.testing as ftt
import flet_charts as fch

speedometer = load_example("gauge_chart/speedometer")
activity_rings = load_example("gauge_chart/activity_rings")


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    """Renders a gauge with zones, a progress ring, ticks and a needle."""
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=fch.GaugeChart(
            width=240,
            height=240,
            max_value=100,
            rings_space=4,
            rings=[
                fch.GaugeProgressRing(
                    value=65,
                    width=16,
                    color=ft.Colors.INDIGO,
                    bgcolor=ft.Colors.BLACK_12,
                    stroke_cap=ft.StrokeCap.ROUND,
                ),
                fch.GaugeZonesRing(
                    width=6,
                    zones_space=4,
                    zones=[
                        fch.GaugeZone(0, 60, ft.Colors.GREEN),
                        fch.GaugeZone(60, 85, ft.Colors.AMBER),
                        fch.GaugeZone(85, 100, ft.Colors.RED),
                    ],
                ),
            ],
            ticks=fch.GaugeLineTicks(count=11, offset=4),
            pointers=[
                fch.GaugeNeedlePointer(value=65, length=80, width=8),
                fch.GaugeCirclePointer(value=0, radius=8),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": speedometer.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_speedometer(flet_app_function: ftt.FletTestApp):
    """Moving the slider updates the speed reading and the gauge."""
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    slider = await flet_app_function.tester.find_by_key("speed")
    await flet_app_function.tester.drag(slider, ft.Offset(80, 0))
    await flet_app_function.tester.pump_and_settle()
    assert (await flet_app_function.tester.find_by_text("60 km/h")).count == 0
    flet_app_function.assert_screenshot(
        "speedometer",
        await flet_app_function.take_page_controls_screenshot(
            bgcolor=ft.Colors.SURFACE
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": activity_rings.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_activity_rings(flet_app_function: ftt.FletTestApp):
    """Tapping the outer ring highlights it and shows its progress."""
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    # The 260-pixel chart sits in the top-left corner of the padded page; the
    # outer ring's stroke runs 118 pixels from its center.
    padding = flet_app_function.page.padding
    await flet_app_function.tester.tap_at(
        ft.Offset(padding.left + 130, padding.top + 130 - 118)
    )
    await flet_app_function.tester.pump_and_settle()
    assert (await flet_app_function.tester.find_by_text("Move: 85%")).count == 1
    flet_app_function.assert_screenshot(
        "activity_rings",
        await flet_app_function.take_page_controls_screenshot(
            bgcolor=ft.Colors.SURFACE
        ),
    )
