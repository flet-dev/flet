import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.color_picker.main as color_picker
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Column(
            intrinsic_width=True,
            controls=[fluent.ColorPicker(value="#0078d4", show_more_button=False)],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": color_picker.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_color_picker(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(480, 760)
    flet_app_function.page.update()
    await tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "color_picker_initial",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    # A tap on the right edge of the spectrum picks a saturated red, at the
    # brightness of the previous color.
    await tester.tap_at(ft.Offset(255, 138))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("#ffd41212")).count == 1
    flet_app_function.assert_screenshot(
        "color_picker",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    flet_app_function.create_gif(
        ["color_picker_initial", "color_picker"],
        "color_picker_flow",
        duration=1200,
    )
