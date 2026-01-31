import pytest

import flet as ft
import flet.testing as ftt
from flet_color_picker import ColorPicker


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Column(
            intrinsic_width=True,
            controls=[ColorPicker()],
        ),
    )


# @pytest.mark.parametrize(
#     "flet_app_function",
#     [{"flet_app_main": basic.main}],
#     indirect=True,
# )
# @pytest.mark.asyncio(loop_scope="function")
# async def test_basic(flet_app_function: ftt.FletTestApp):
#     button = await flet_app_function.tester.find_by_text("Submit")
#     await flet_app_function.tester.tap(button)
#     await flet_app_function.tester.pump_and_settle()
#     flet_app_function.assert_screenshot(
#         "basic",
#         await flet_app_function.take_page_controls_screenshot(),
#     )
