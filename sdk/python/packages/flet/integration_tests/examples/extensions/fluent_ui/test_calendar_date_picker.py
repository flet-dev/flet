import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.calendar_date_picker.main as calendar_date_picker
import flet as ft
import flet.testing as ftt


async def _capture(app: ftt.FletTestApp, name: str):
    # The calendar opens over the page, so these are full-page screenshots.
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
            controls=[fluent.CalendarDatePicker(placeholder="Pick a date")],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": calendar_date_picker.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_calendar_date_picker(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(400, 480)
    flet_app_function.page.update()
    await tester.pump_and_settle()
    await _capture(flet_app_function, "calendar_date_picker_initial")

    await tester.tap(await tester.find_by_key("delivery"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "calendar_date_picker_open")

    # Picking a day closes the calendar.
    await tester.tap(await tester.find_by_text("21"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Delivery on Wednesday, May 21")).count == 1
    await _capture(flet_app_function, "calendar_date_picker")
    flet_app_function.create_gif(
        [
            "calendar_date_picker_initial",
            "calendar_date_picker_open",
            "calendar_date_picker",
        ],
        "calendar_date_picker_flow",
        duration=1000,
    )
