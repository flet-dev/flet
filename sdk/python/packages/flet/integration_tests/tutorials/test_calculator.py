import pytest

import flet.testing as ftt

# from examples.controls.checkbox import basic, handling_events, styled
from examples.tutorials.calculator import calc1

# @pytest.mark.asyncio(loop_scope="function")
# async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
#     flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
#     await flet_app_function.assert_control_screenshot(
#         request.node.name,
#         ft.Column(
#             intrinsic_width=True,
#             controls=[
#                 ft.Checkbox(),
#                 ft.Checkbox(label="Checked", value=True),
#                 ft.Checkbox(label="Disabled", disabled=True),
#             ],
#         ),
#     )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": calc1.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    # button = await flet_app_function.tester.find_by_text("Submit")
    # await flet_app_function.tester.tap(button)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "calc1",
        await flet_app_function.take_page_controls_screenshot(),
    )


# @pytest.mark.parametrize(
#     "flet_app_function",
#     [{"flet_app_main": handling_events.main}],
#     indirect=True,
# )
# @pytest.mark.asyncio(loop_scope="function")
# async def test_handling_events(flet_app_function: ftt.FletTestApp):
#     checkbox = await flet_app_function.tester.find_by_text(
#         "Checkbox with 'change' event"
#     )
#     await flet_app_function.tester.tap(checkbox)
#     await flet_app_function.tester.pump_and_settle()
#     await flet_app_function.tester.tap(checkbox)
#     await flet_app_function.tester.pump_and_settle()
#     await flet_app_function.tester.tap(checkbox)
#     await flet_app_function.tester.pump_and_settle()
#     scr = await flet_app_function.wrap_page_controls_in_screenshot()
#     flet_app_function.assert_screenshot(
#         "handling_events",
#         await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
#     )


# @pytest.mark.parametrize(
#     "flet_app_function",
#     [{"flet_app_main": styled.main}],
#     indirect=True,
# )
# @pytest.mark.asyncio(loop_scope="function")
# async def test_styled(flet_app_function: ftt.FletTestApp):
#     flet_app_function.assert_screenshot(
#         "styled_checkboxes",
#         await flet_app_function.take_page_controls_screenshot(),
#     )
