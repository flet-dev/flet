import datetime

import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.date_picker.main as date_picker
import flet as ft
import flet.testing as ftt


async def _capture(app: ftt.FletTestApp, name: str):
    app.assert_screenshot(
        name,
        await app.page.take_screenshot(pixel_ratio=app.screenshots_pixel_ratio),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    # The calendar opens in an overlay, so this is a full-page screenshot.
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(320, 420)
    flet_app_function.page.add(
        shad.DatePicker(key="picker", value=datetime.date(2025, 6, 12))
    )
    await flet_app_function.tester.pump_and_settle()
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_key("picker")
    )
    await flet_app_function.tester.pump_and_settle()
    await _capture(flet_app_function, request.node.name)


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": date_picker.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_date_picker(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(320, 440)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    await _capture(flet_app_function, "date_picker_closed")

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_key("due_date")
    )
    await flet_app_function.tester.pump_and_settle()
    await _capture(flet_app_function, "date_picker_open")

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("20")
    )
    await flet_app_function.tester.pump_and_settle()

    assert (
        await flet_app_function.tester.find_by_text("Due date: 2025-06-20")
    ).count == 1
    await _capture(flet_app_function, "date_picker")
    flet_app_function.create_gif(
        ["date_picker_closed", "date_picker_open", "date_picker"],
        "date_picker_flow",
        duration=1000,
    )
