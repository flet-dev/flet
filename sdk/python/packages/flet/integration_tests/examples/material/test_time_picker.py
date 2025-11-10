from datetime import time

import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.time_picker import basic, hour_formats


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(600, 400)

    time_picker = ft.TimePicker(
        value=time(hour=1, minute=2),
        hour_format=ft.TimePickerHourFormat.H12,
    )
    flet_app_function.page.show_dialog(time_picker)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "test_image_for_docs",
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

    # open picker
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_icon(ft.Icons.TIME_TO_LEAVE)
    )
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "basic",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": hour_formats.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_hour_formats(flet_app_function: ftt.FletTestApp):
    counter = 0
    images = []

    async def _snap():
        nonlocal counter
        counter += 1
        name = f"hour_formats_{counter}"
        images.append(name)
        flet_app_function.assert_screenshot(
            name,
            await flet_app_function.page.take_screenshot(
                pixel_ratio=flet_app_function.screenshots_pixel_ratio
            ),
        )

    async def _settle():
        await flet_app_function.tester.pump_and_settle()

    async def _open_picker():
        await flet_app_function.tester.tap(
            await flet_app_function.tester.find_by_icon(ft.Icons.SCHEDULE)
        )
        await _settle()
        await _snap()

    async def _close_picker():
        await flet_app_function.tester.tap(
            await flet_app_function.tester.find_by_text("OK")
        )
        await _settle()
        await _snap()

    async def _select_clock(label: str):
        await flet_app_function.tester.tap(
            await flet_app_function.tester.find_by_key("dd")
        )
        await _settle()
        await flet_app_function.tester.tap(
            await flet_app_function.tester.find_by_text(label)
        )
        await _settle()
        await _snap()

    flet_app_function.page.enable_screenshots = True
    await flet_app_function.resize_page(600, 450)
    flet_app_function.page.update()
    await _settle()

    # initial state
    await _snap()

    # picker open/close on default
    await _open_picker()
    await _close_picker()

    # switch to 12h, then open/close
    await _select_clock("12-hour clock")
    await _open_picker()
    await _close_picker()

    # switch to 24h, then open/close
    await _select_clock("24-hour clock")
    await _open_picker()
    await _close_picker()

    flet_app_function.create_gif(
        image_names=images, output_name="hour_formats", duration=2000
    )
