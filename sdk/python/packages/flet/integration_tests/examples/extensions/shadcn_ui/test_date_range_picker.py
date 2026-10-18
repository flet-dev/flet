import datetime

import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.date_range_picker.main as date_range_picker
import flet as ft
import flet.testing as ftt


async def _capture(app: ftt.FletTestApp, name: str):
    app.assert_screenshot(
        name,
        await app.page.take_screenshot(pixel_ratio=app.screenshots_pixel_ratio),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    # The calendars open in an overlay, so this is a full-page screenshot.
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(600, 420)
    flet_app_function.page.add(
        shad.DateRangePicker(
            key="picker",
            start_value=datetime.date(2025, 6, 9),
            end_value=datetime.date(2025, 6, 13),
        )
    )
    await flet_app_function.tester.pump_and_settle()
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_key("picker")
    )
    await flet_app_function.tester.pump_and_settle()
    await _capture(flet_app_function, request.node.name)


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": date_range_picker.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_date_range_picker(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(600, 440)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    await _capture(flet_app_function, "date_range_picker_closed")

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_key("trip")
    )
    await flet_app_function.tester.pump_and_settle()
    await _capture(flet_app_function, "date_range_picker_open")

    # The range is complete, so the first click starts a new range...
    await flet_app_function.tester.tap(
        (await flet_app_function.tester.find_by_text("16")).first
    )
    await flet_app_function.tester.pump_and_settle()
    assert (
        await flet_app_function.tester.find_by_text("Trip: 2025-06-16 to ...")
    ).count == 1
    await _capture(flet_app_function, "date_range_picker_start")

    # ...and the second click sets its end.
    await flet_app_function.tester.tap(
        (await flet_app_function.tester.find_by_text("20")).first
    )
    await flet_app_function.tester.pump_and_settle()
    assert (
        await flet_app_function.tester.find_by_text("Trip: 2025-06-16 to 2025-06-20")
    ).count == 1
    await _capture(flet_app_function, "date_range_picker")
    flet_app_function.create_gif(
        [
            "date_range_picker_closed",
            "date_range_picker_open",
            "date_range_picker_start",
            "date_range_picker",
        ],
        "date_range_picker_flow",
        duration=1000,
    )
