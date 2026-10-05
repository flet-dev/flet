import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.form.main as form
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Column(
            width=300,
            spacing=16,
            controls=[
                shad.Input(
                    label="Username",
                    value="flet_fan",
                    description="This is your public display name.",
                ),
                shad.Input(
                    label="Email",
                    value="flet.dev",
                    error_text="Enter a valid email address.",
                ),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": form.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_form(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    tester = flet_app_function.tester
    await tester.pump_and_settle()
    scr = await flet_app_function.wrap_page_controls_in_screenshot(
        bgcolor=ft.Colors.SURFACE
    )
    await tester.pump_and_settle()

    async def capture(name: str):
        flet_app_function.assert_screenshot(
            name,
            await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
        )

    await capture("form_initial")

    # Submitting the empty form shows an error under every field.
    await tester.tap(await tester.find_by_key("submit"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Enter a valid email address.")).count == 1
    assert (await tester.find_by_text("You must accept the terms.")).count == 1
    await capture("form_errors")

    # After a submit, each field re-checks as it changes.
    await tester.enter_text(await tester.find_by_key("username"), "flet_fan")
    await tester.enter_text(await tester.find_by_key("email"), "fan@flet.dev")
    await tester.enter_text(await tester.find_by_key("password"), "secret")
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Enter a valid email address.")).count == 0
    assert (
        await tester.find_by_text("Password must be at least 8 characters.")
    ).count == 1
    await capture("form_partial")

    await tester.enter_text(await tester.find_by_key("password"), "secret123")
    await tester.tap(await tester.find_by_text("Select a role"))
    await tester.pump_and_settle()
    await tester.tap(await tester.find_by_text("Developer"))
    await tester.pump_and_settle()
    await tester.tap(await tester.find_by_text("I accept the terms and conditions"))
    await tester.pump_and_settle()
    await tester.tap(await tester.find_by_key("submit"))
    await tester.pump_and_settle()

    assert (await tester.find_by_text("Account created for flet_fan!")).count == 1
    await capture("form")
    flet_app_function.create_gif(
        ["form_initial", "form_errors", "form_partial", "form"],
        "form_flow",
        duration=1200,
    )
