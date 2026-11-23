import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.rating_bar.main as rating_bar
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
            controls=[
                fluent.RatingBar(value=3),
                fluent.RatingBar(value=4.5, read_only=True),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": rating_bar.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_rating_bar(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    scr = await flet_app_function.wrap_page_controls_in_screenshot(
        bgcolor=ft.Colors.SURFACE
    )
    flet_app_function.assert_screenshot(
        "rating_bar_initial",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )

    # A tap in the middle of five stars rates three.
    await tester.tap(await tester.find_by_key("rating"))
    await tester.pump_and_settle()

    assert (await tester.find_by_text("You rated it 3 stars")).count == 1
    flet_app_function.assert_screenshot(
        "rating_bar",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
    flet_app_function.create_gif(
        ["rating_bar_initial", "rating_bar"], "rating_bar_flow", duration=1000
    )
