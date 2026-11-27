from datetime import date

import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.date_picker.main as date_picker
import flet as ft
import flet.testing as ftt


async def _capture(app: ftt.FletTestApp, name: str):
    # The picker lists open over the page, so these are full-page screenshots.
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
            width=300,
            controls=[fluent.DatePicker(header="Birthday", value=date(1990, 4, 12))],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": date_picker.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_date_picker(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(400, 480)
    flet_app_function.page.update()
    await tester.pump_and_settle()
    await _capture(flet_app_function, "date_picker_initial")

    await tester.tap(await tester.find_by_key("birthday"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "date_picker_open")

    # Picking a year scrolls it into the highlighted row.
    await tester.tap(await tester.find_by_text("1991"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "date_picker_picked")

    # The check mark button (an internal fluent_ui icon, so found by position)
    # confirms the date.
    await tester.tap_at(ft.Offset(84, 378))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Birthday: April 12, 1991")).count == 1
    await _capture(flet_app_function, "date_picker")
    flet_app_function.create_gif(
        [
            "date_picker_initial",
            "date_picker_open",
            "date_picker_picked",
            "date_picker",
        ],
        "date_picker_flow",
        duration=1000,
    )
