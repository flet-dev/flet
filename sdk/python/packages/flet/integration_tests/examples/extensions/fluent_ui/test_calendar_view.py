from datetime import date

import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.calendar_view.main as calendar_view
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Column(
            intrinsic_width=True,
            controls=[fluent.CalendarView(value=date(2025, 5, 14), width=300)],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": calendar_view.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_calendar_view(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    await tester.pump_and_settle()
    scr = await flet_app_function.wrap_page_controls_in_screenshot(
        bgcolor=ft.Colors.SURFACE
    )
    flet_app_function.assert_screenshot(
        "calendar_view_initial",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )

    # With a range selected, a click starts a new range...
    await tester.tap(await tester.find_by_text("20"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Now pick the last day")).count == 1
    flet_app_function.assert_screenshot(
        "calendar_view_start",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )

    # ...and the next click ends it.
    await tester.tap(await tester.find_by_text("23"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Your trip is 4 days long")).count == 1
    flet_app_function.assert_screenshot(
        "calendar_view",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
    flet_app_function.create_gif(
        ["calendar_view_initial", "calendar_view_start", "calendar_view"],
        "calendar_view_flow",
        duration=1000,
    )
