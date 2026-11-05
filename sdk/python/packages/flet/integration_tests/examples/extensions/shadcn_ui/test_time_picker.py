import datetime

import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.time_picker.main as time_picker
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=shad.TimePicker(value=datetime.time(14, 30)),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": time_picker.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_time_picker(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    scr = await flet_app_function.wrap_page_controls_in_screenshot(
        bgcolor=ft.Colors.SURFACE
    )
    flet_app_function.assert_screenshot(
        "time_picker_initial",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
    assert (await flet_app_function.tester.find_by_text("Meeting at 14:30")).count == 1
    assert (
        await flet_app_function.tester.find_by_text("Alarm at 07:00 (07:00 AM)")
    ).count == 1

    # 24-hour picker: set from code with the button.
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Set to noon")
    )
    await flet_app_function.tester.pump_and_settle()
    assert (await flet_app_function.tester.find_by_text("Meeting at 12:00")).count == 1
    flet_app_function.assert_screenshot(
        "time_picker_noon",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )

    # 12-hour picker: switch the alarm from AM to PM; value stays 24-hour.
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("AM")
    )
    await flet_app_function.tester.pump_and_settle()
    await flet_app_function.tester.tap(
        (await flet_app_function.tester.find_by_text("PM")).last
    )
    await flet_app_function.tester.pump_and_settle()
    assert (
        await flet_app_function.tester.find_by_text("Alarm at 19:00 (07:00 PM)")
    ).count == 1
    flet_app_function.assert_screenshot(
        "time_picker",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
    flet_app_function.create_gif(
        ["time_picker_initial", "time_picker_noon", "time_picker"],
        "time_picker_flow",
        duration=1000,
    )
