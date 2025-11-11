import datetime

import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(600, 450)

    time_picker = ft.TimePicker(
        confirm_text="Confirm",
        error_invalid_text="Time out of range",
        help_text="Pick your time slot",
        value=datetime.time(hour=1, minute=30),
    )
    flet_app.page.show_dialog(time_picker)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        request.node.name,
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_hour_format_12(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(600, 450)

    time_picker = ft.TimePicker(
        value=datetime.time(hour=1, minute=30),
        hour_format=ft.TimePickerHourFormat.H12,
    )
    flet_app.page.show_dialog(time_picker)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        request.node.name,
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_hour_format_24(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(600, 450)

    time_picker = ft.TimePicker(
        value=datetime.time(hour=1, minute=30),
        hour_format=ft.TimePickerHourFormat.H24,
    )
    flet_app.page.show_dialog(time_picker)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        request.node.name,
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
