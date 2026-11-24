import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.input.main as input
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=shad.Input(
            width=280, placeholder="Email", leading=shad.LucideIcons.MAIL
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": input.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_input(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    scr = await flet_app_function.wrap_page_controls_in_screenshot(
        bgcolor=ft.Colors.SURFACE
    )
    flet_app_function.assert_screenshot(
        "input_initial",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )

    await flet_app_function.tester.enter_text(
        await flet_app_function.tester.find_by_key("email"), "hello@flet.dev"
    )
    await flet_app_function.tester.pump_and_settle()

    assert (
        await flet_app_function.tester.find_by_text("Email: hello@flet.dev")
    ).count == 1
    flet_app_function.assert_screenshot(
        "input",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
    flet_app_function.create_gif(
        ["input_initial", "input"], "input_flow", duration=1000
    )
