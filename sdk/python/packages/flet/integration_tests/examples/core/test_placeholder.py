import pytest

import flet as ft
import flet.testing as ftt

from examples.controls.placeholder import basic


# @pytest.mark.asyncio(loop_scope="function")
# async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
#     flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
#     await flet_app_function.assert_control_screenshot(
#         request.node.name,
#         ft.Placeholder(
#             expand=True,
#             color=ft.Colors.RED_500,
#         ),
#     )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(200, 200)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "basic",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
