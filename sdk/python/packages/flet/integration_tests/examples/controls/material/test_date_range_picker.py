import datetime

import pytest

import examples.controls.material.date_range_picker.basic.main as basic
import examples.controls.material.date_range_picker.custom_locale.main as custom_locale
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(620, 480)
    flet_app_function.page.update()

    flet_app_function.page.show_dialog(
        ft.DateRangePicker(
            start_value=datetime.datetime(2025, 4, 10),
            end_value=datetime.datetime(2025, 4, 20),
            first_date=datetime.datetime(2024, 1, 1),
            last_date=datetime.datetime(2026, 12, 31),
            current_date=datetime.datetime(2025, 4, 15),
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
    flet_app_function.resize_page(620, 480)
    flet_app_function.page.update()

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Pick date range")
    )
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "basic",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": custom_locale.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_custom_locale(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(620, 480)
    flet_app_function.page.update()

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Pick dates (zh_Hans locale)")
    )
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "custom_locale",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
