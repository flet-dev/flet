import pytest

import flet as ft
import flet.testing as ftt

from examples.controls.radio import basic, handling_selection_changes, styled


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.RadioGroup(
            content=ft.Row(
                controls=[ft.Radio(label=f"{i}") for i in range(1, 4)],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            ),
            expand=True,
        ),
    )


# @pytest.mark.parametrize(
#     "flet_app_function",
#     [{"flet_app_main": basic.main}],
#     indirect=True,
# )
# @pytest.mark.asyncio(loop_scope="function")
# async def test_basic(flet_app_function: ftt.FletTestApp):
#     flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
#     flet_app_function.page.enable_screenshots = True
#     flet_app_function.page.update()
#     red = await flet_app_function.tester.find_by_text("Red")
#     await flet_app_function.tester.tap(red)
#     await flet_app_function.tester.pump_and_settle()
#     submit = await flet_app_function.tester.find_by_text("Submit")
#     await flet_app_function.tester.tap(submit)
#     await flet_app_function.tester.pump_and_settle()
#     flet_app_function.assert_screenshot(
#         "basic",
#         await flet_app_function.take_page_controls_screenshot(),
#     )


# @pytest.mark.parametrize(
#     "flet_app_function",
#     [{"flet_app_main": handling_selection_changes.main}],
#     indirect=True,
# )
# @pytest.mark.asyncio(loop_scope="function")
# async def test_handling_selection_changes(flet_app_function: ftt.FletTestApp):
#     flet_app_function.page.enable_screenshots = True
#     flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
#     flet_app_function.page.update()
#     blue = await flet_app_function.tester.find_by_text("Blue")
#     await flet_app_function.tester.tap(blue)
#     await flet_app_function.tester.pump_and_settle()
#     flet_app_function.assert_screenshot(
#         "handling_selection_changes",
#         await flet_app_function.take_page_controls_screenshot(
#             pixel_ratio=flet_app_function.screenshots_pixel_ratio
#         ),
#     )
