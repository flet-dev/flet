import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.password_box.main as password_box
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Column(
            width=260,
            controls=[
                fluent.PasswordBox(placeholder="Password", value="secret"),
                fluent.PasswordBox(
                    placeholder="PIN", reveal_mode=fluent.PasswordRevealMode.HIDDEN
                ),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": password_box.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_password_box(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    scr = await flet_app_function.wrap_page_controls_in_screenshot(
        bgcolor=ft.Colors.SURFACE
    )
    flet_app_function.assert_screenshot(
        "password_box_initial",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )

    await tester.enter_text(
        await tester.find_by_key("password"), "correct horse battery"
    )
    await tester.pump_and_settle()

    assert (await tester.find_by_text("Strength: strong")).count == 1
    flet_app_function.assert_screenshot(
        "password_box",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
    flet_app_function.create_gif(
        ["password_box_initial", "password_box"], "password_box_flow", duration=1000
    )
