import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.number_box.main as number_box
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Column(
            width=200,
            controls=[
                fluent.NumberBox(value=3, min=0, max=10),
                fluent.NumberBox(value=2.5, small_change=0.5, precision=1),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": number_box.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_number_box(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    scr = await flet_app_function.wrap_page_controls_in_screenshot(
        bgcolor=ft.Colors.SURFACE
    )
    flet_app_function.assert_screenshot(
        "number_box_initial",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )

    await tester.enter_text(await tester.find_by_key("quantity"), "3")
    # The number box applies typed text when the user clicks outside it.
    await tester.tap(await tester.find_by_text("Coffee beans, $4.50 per bag"))
    await tester.pump_and_settle()

    assert (await tester.find_by_text("Total: $13.50")).count == 1
    flet_app_function.assert_screenshot(
        "number_box",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
    flet_app_function.create_gif(
        ["number_box_initial", "number_box"], "number_box_flow", duration=1000
    )
