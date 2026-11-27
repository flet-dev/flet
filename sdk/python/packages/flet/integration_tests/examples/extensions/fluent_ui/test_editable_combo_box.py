import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.editable_combo_box.main as editable_combo_box
import flet as ft
import flet.testing as ftt


async def _capture(app: ftt.FletTestApp, name: str):
    # The list opens over the page, so these are full-page screenshots.
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
        control=ft.Row(
            tight=True,
            controls=[
                fluent.EditableComboBox(
                    width=200,
                    value="12",
                    items=[
                        fluent.ComboBoxItem(value=str(size)) for size in [8, 10, 12, 14]
                    ],
                )
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": editable_combo_box.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_editable_combo_box(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(340, 320)
    flet_app_function.page.update()
    await tester.pump_and_settle()
    await _capture(flet_app_function, "editable_combo_box_initial")

    # Typed text is applied when the box loses focus, here to the other box.
    await tester.enter_text(await tester.find_by_key("size"), "30")
    await tester.pump_and_settle()
    await tester.tap(await tester.find_by_key("font"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "editable_combo_box_typed")

    # The test driver types into the focused box, so focus Size first.
    await tester.tap(await tester.find_by_key("size"))
    await tester.pump_and_settle()
    await tester.enter_text(await tester.find_by_key("size"), "100")
    await tester.pump_and_settle()
    await tester.tap(await tester.find_by_key("font"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Enter 1 to 72")).count == 1
    await _capture(flet_app_function, "editable_combo_box_error")

    # Picking an option clears the error.
    # The chevron has no text or Flet icon to find it by.
    await tester.tap_at(ft.Offset(286, 26))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "editable_combo_box_open")
    await tester.tap(await tester.find_by_text("24"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Enter 1 to 72")).count == 0
    await _capture(flet_app_function, "editable_combo_box")
    flet_app_function.create_gif(
        [
            "editable_combo_box_initial",
            "editable_combo_box_typed",
            "editable_combo_box_error",
            "editable_combo_box_open",
            "editable_combo_box",
        ],
        "editable_combo_box_flow",
        duration=1000,
    )
