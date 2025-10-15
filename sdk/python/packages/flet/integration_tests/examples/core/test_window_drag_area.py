import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.window_drag_area import no_frame_window


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Row(
            controls=[
                ft.WindowDragArea(
                    expand=True,
                    content=ft.Container(
                        bgcolor=ft.Colors.BLUE_GREY_200,
                        padding=10,
                        content=ft.Text("Drag area."),
                    ),
                ),
                ft.IconButton(ft.Icons.CLOSE),
            ]
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": no_frame_window.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_no_frame_window(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "no_frame_window",
        await flet_app_function.take_page_controls_screenshot(),
    )
