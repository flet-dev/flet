from datetime import time

import pytest

import examples.controls.material.time_picker.basic.main as basic
import examples.controls.material.time_picker.custom_locale.main as custom_locale
import examples.controls.material.time_picker.hour_formats.main as hour_formats
import flet as ft
import flet.testing as ftt

# Note: CI macOS runner uses a 12-hour (AM / PM) time format by default.


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(600, 400)
    flet_app_function.page.update()

    flet_app_function.page.show_dialog(
        ft.TimePicker(
            value=time(hour=19, minute=30),
            hour_format=ft.TimePickerHourFormat.H12,
        )
    )
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        request.node.name,
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(600, 400)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    pick_time = await flet_app_function.tester.find_by_key("pick_time_button")
    frames = [
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    ]

    await flet_app_function.tester.mouse_hover(pick_time)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(pick_time)
    await flet_app_function.tester.pump_and_settle()
    opened_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot("basic_opened", opened_frame)
    frames.append(opened_frame)

    switch_to_text_input = await flet_app_function.tester.find_by_tooltip(
        "Switch to text input mode"
    )
    await flet_app_function.tester.mouse_hover(switch_to_text_input.first)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(switch_to_text_input.first)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    am = await flet_app_function.tester.find_by_text("AM")
    await flet_app_function.tester.mouse_hover(am.first)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(am.first)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    hour_field = await flet_app_function.tester.find_by_text("7")
    await flet_app_function.tester.enter_text(hour_field.first, "11")
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    minute_field = await flet_app_function.tester.find_by_text("30")
    await flet_app_function.tester.enter_text(minute_field.first, "45")
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    confirm = await flet_app_function.tester.find_by_text("Confirm")
    await flet_app_function.tester.mouse_hover(confirm.first)
    await flet_app_function.tester.pump_and_settle()
    confirm_hover_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot("basic_confirm_hover", confirm_hover_frame)
    frames.append(confirm_hover_frame)

    await flet_app_function.tester.tap(confirm.first)
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    flet_app_function.create_gif(frames=frames, output_name="basic", duration=1000)


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": hour_formats.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_hour_formats(flet_app_function: ftt.FletTestApp):
    async def _settle():
        await flet_app_function.tester.pump_and_settle(ft.Duration(milliseconds=500))

    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(600, 450)
    flet_app_function.page.update()
    await _settle()

    open_picker = await flet_app_function.tester.find_by_text("Open TimePicker")
    dropdown = await flet_app_function.tester.find_by_key("dd")

    frames = [
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    ]

    await flet_app_function.tester.mouse_hover(open_picker.first)
    await _settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(dropdown)
    await _settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    clock_12h = await flet_app_function.tester.find_by_text("12-hour clock")
    await flet_app_function.tester.mouse_hover(clock_12h.last)
    await _settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(clock_12h.last)
    await _settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.mouse_hover(open_picker.first)
    await _settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(open_picker.first)
    await _settle()
    opened_12h_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot("hour_formats_opened_12h", opened_12h_frame)
    frames.append(opened_12h_frame)

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Cancel")
    )
    await _settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(dropdown)
    await _settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    clock_24h = await flet_app_function.tester.find_by_text("24-hour clock")
    await flet_app_function.tester.mouse_hover(clock_24h.last)
    await _settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(clock_24h.last)
    await _settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.mouse_hover(open_picker.first)
    await _settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    await flet_app_function.tester.tap(open_picker.first)
    await _settle()
    opened_24h_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot("hour_formats_opened_24h", opened_24h_frame)
    frames.append(opened_24h_frame)

    flet_app_function.create_gif(
        frames=frames, output_name="hour_formats", duration=1000
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": custom_locale.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_custom_locale(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(600, 400)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_key("custom_locale_button")
    )
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "custom_locale",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
