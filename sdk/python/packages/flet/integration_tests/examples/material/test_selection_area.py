import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.selection_area import basic


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    selectable = ft.SelectionArea(
        content=ft.Text("Selectable text", color=ft.Colors.GREEN),
    )
    non_selectable = ft.Text("Not selectable", color=ft.Colors.RED)
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Column(controls=[selectable, non_selectable]),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "basic",
        await flet_app_function.take_page_controls_screenshot(),
    )


# @pytest.mark.parametrize(
#     "flet_app_function",
#     [{"flet_app_main": basic.main}],
#     indirect=True,
# )
# @pytest.mark.asyncio(loop_scope="function")
# async def test_basic(flet_app_function: ftt.FletTestApp):
#     flet_app_function.page.enable_screenshots = True
#     flet_app_function.page.window.width = 250
#     flet_app_function.page.window.height = 200
#     flet_app_function.page.update()
#     selectable_text = await flet_app_function.tester.find_by_key("selectable")
#     await flet_app_function.tester.tap(selectable_text)
#     await flet_app_function.tester.pump_and_settle(duration=ft.Duration(seconds=1))
#     flet_app_function.assert_screenshot(
#         "selectable",
#         await flet_app_function.page.take_screenshot(
#             pixel_ratio=flet_app_function.screenshots_pixel_ratio
#         ),
#     )
#     unselectable_text = await flet_app_function.tester.find_by_key("non-selectable")
#     await flet_app_function.tester.tap(unselectable_text)
#     await flet_app_function.tester.pump_and_settle(duration=ft.Duration(seconds=1))
#     flet_app_function.assert_screenshot(
#         "non_selectable",
#         await flet_app_function.page.take_screenshot(
#             pixel_ratio=flet_app_function.screenshots_pixel_ratio
#         ),
#     )

#     flet_app_function.create_gif(
#         ["selectable", "non_selectable"],
#         "selection_area",
#         duration=2000,
#     )
