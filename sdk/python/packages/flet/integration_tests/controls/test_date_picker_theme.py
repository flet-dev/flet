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
async def test_date_picker_theme(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme = ft.Theme(
        date_picker_theme=ft.DatePickerTheme(
            bgcolor=ft.Colors.GREEN_200,
        )
    )

    dp = ft.DatePicker(
        current_date=datetime.datetime(year=2025, month=8, day=15),
        first_date=datetime.datetime(year=2000, month=10, day=1),
        last_date=datetime.datetime(year=2025, month=10, day=1),
    )
    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.show_dialog(dp)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "theme1",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
