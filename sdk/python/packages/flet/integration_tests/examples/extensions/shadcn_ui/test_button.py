import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.button.main as button
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
                ft.Row(
                    [
                        shad.Button("Primary"),
                        shad.Button("Outline", variant=shad.ButtonVariant.OUTLINE),
                        shad.Button("Mail", leading=shad.LucideIcons.MAIL),
                    ]
                )
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": button.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_button(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Login with Email")
    )
    await flet_app_function.tester.pump_and_settle()

    assert (
        await flet_app_function.tester.find_by_text("Clicked: Login with Email")
    ).count == 1
    flet_app_function.assert_screenshot(
        "button",
        await flet_app_function.take_page_controls_screenshot(
            bgcolor=ft.Colors.SURFACE
        ),
    )
