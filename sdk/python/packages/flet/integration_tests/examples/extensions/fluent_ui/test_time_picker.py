from datetime import time

import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.time_picker.main as time_picker
import flet as ft
import flet.testing as ftt


async def _capture(app: ftt.FletTestApp, name: str):
    # The picker lists open over the page, so these are full-page screenshots.
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
            width=300,
            controls=[fluent.TimePicker(header="Alarm", value=time(7, 30))],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": time_picker.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_time_picker(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(400, 480)
    flet_app_function.page.update()
    await tester.pump_and_settle()
    await _capture(flet_app_function, "time_picker_initial")

    await tester.tap(await tester.find_by_key("meeting"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "time_picker_open")

    # Picking an hour scrolls it into the highlighted row.
    await tester.tap(await tester.find_by_text("16"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "time_picker_picked")

    # The check mark button (an internal fluent_ui icon, so found by position)
    # confirms the time.
    await tester.tap_at(ft.Offset(84, 378))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Meeting at 16:30")).count == 1
    await _capture(flet_app_function, "time_picker")
    flet_app_function.create_gif(
        [
            "time_picker_initial",
            "time_picker_open",
            "time_picker_picked",
            "time_picker",
        ],
        "time_picker_flow",
        duration=1000,
    )
