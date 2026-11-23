import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.combo_box.main as combo_box
import flet as ft
import flet.testing as ftt


async def _capture(app: ftt.FletTestApp, name: str):
    # The open list is drawn in an overlay, so these are full-page screenshots.
    app.assert_screenshot(
        name,
        await app.page.take_screenshot(pixel_ratio=app.screenshots_pixel_ratio),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Column(
            intrinsic_width=True,
            controls=[
                fluent.ComboBox(
                    placeholder="Placeholder",
                    items=[fluent.ComboBoxItem(value="a", text="Option A")],
                ),
                fluent.ComboBox(
                    value="a",
                    items=[fluent.ComboBoxItem(value="a", text="Option A")],
                ),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": combo_box.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_combo_box(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(320, 260)
    flet_app_function.page.update()
    await tester.pump_and_settle()
    await _capture(flet_app_function, "combo_box_initial")

    await tester.tap(await tester.find_by_text("Pick a color"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "combo_box_open")

    await tester.tap(await tester.find_by_text("Green"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Color: green")).count == 1
    await _capture(flet_app_function, "combo_box")
    flet_app_function.create_gif(
        ["combo_box_initial", "combo_box_open", "combo_box"],
        "combo_box_flow",
        duration=1000,
    )
