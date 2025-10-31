import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.segmented_button import single_multiple_selection


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.SegmentedButton(
            show_selected_icon=False,
            selected=["3"],
            segments=[
                ft.Segment(
                    value="1",
                    icon=ft.Icon(ft.Icons.SENTIMENT_VERY_SATISFIED),
                ),
                ft.Segment(
                    value="2",
                    icon=ft.Icon(ft.Icons.SENTIMENT_SATISFIED),
                ),
                ft.Segment(
                    value="3",
                    icon=ft.Icon(ft.Icons.SENTIMENT_NEUTRAL),
                ),
                ft.Segment(
                    value="4",
                    icon=ft.Icon(ft.Icons.SENTIMENT_DISSATISFIED),
                ),
                ft.Segment(
                    value="5",
                    icon=ft.Icon(ft.Icons.SENTIMENT_VERY_DISSATISFIED),
                ),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": single_multiple_selection.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_single_multiple_selection(flet_app_function: ftt.FletTestApp):
    # flet_app_function.page.enable_screenshots = True
    # flet_app_function.page.window.width = 350
    # flet_app_function.page.window.height = 300
    # flet_app_function.page.update()
    # await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "single_multiple_selection",
        await flet_app_function.take_page_controls_screenshot(),
    )
