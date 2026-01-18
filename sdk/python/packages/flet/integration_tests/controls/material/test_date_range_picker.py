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
    flet_app.resize_page(400, 600)
    flet_app.page.update()

    flet_app.page.show_dialog(
        ft.DateRangePicker(
            start_value=datetime.datetime(year=2000, month=10, day=1),
            end_value=datetime.datetime(year=2000, month=10, day=15),
            first_date=datetime.datetime(year=2000, month=10, day=1),
            last_date=datetime.datetime(year=2000, month=11, day=15),
            current_date=datetime.datetime(year=2000, month=10, day=16),
        )
    )

    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        request.node.name,
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_properties1(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(400, 600)
    flet_app.page.update()

    flet_app.page.show_dialog(
        ft.DateRangePicker(
            start_value=datetime.datetime(year=2000, month=10, day=7),
            end_value=datetime.datetime(year=2000, month=10, day=15),
            first_date=datetime.datetime(year=2000, month=10, day=1),
            last_date=datetime.datetime(year=2000, month=11, day=15),
            current_date=datetime.datetime(year=2000, month=10, day=16),
            switch_to_calendar_icon=ft.Icons.BABY_CHANGING_STATION,
            switch_to_input_icon=ft.Icons.ACCESS_ALARM,
            save_text="Custom save text",
            error_invalid_range_text="Invalid range custom text",
            help_text="Custom help text",
            cancel_text="Custom cancel text",
            confirm_text="Custom confirm text",
            error_format_text="Custom error format text",
            error_invalid_text="Custom error invalid text",
            field_end_hint_text="Custom end hint text",
            field_start_hint_text="Custom start hint text",
            field_end_label_text="Custom end label text",
            field_start_label_text="Custom start label text",
            modal=False,
            barrier_color=ft.Colors.RED,
            keyboard_type=ft.KeyboardType.EMAIL,
            # entry_mode=ft.DatePickerEntryMode.CALENDAR,
        )
    )
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "properties_calendar",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # change to input mode
    input_icon = await flet_app.tester.find_by_icon(ft.Icons.ACCESS_ALARM)
    assert input_icon.count == 1
    await flet_app.tester.tap(input_icon)
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "properties_input",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_locale(flet_app: ftt.FletTestApp, request):
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(400, 600)
    flet_app.page.update()

    flet_app.page.show_dialog(
        ft.DateRangePicker(
            locale=ft.Locale("zh", "Hans"),
            start_value=datetime.datetime(year=2000, month=10, day=1),
            end_value=datetime.datetime(year=2000, month=10, day=15),
            first_date=datetime.datetime(year=2000, month=10, day=1),
            last_date=datetime.datetime(year=2000, month=11, day=15),
            current_date=datetime.datetime(year=2000, month=10, day=16),
        )
    )

    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        request.node.name,
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
