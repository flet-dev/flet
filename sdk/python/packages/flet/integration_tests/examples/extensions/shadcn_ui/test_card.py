import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.card.main as card
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=shad.Card(
            width=300,
            title="Notifications",
            description="You have 3 unread messages.",
            content=ft.Container(
                padding=ft.Padding.symmetric(vertical=16),
                content=ft.Text("Your call has been confirmed."),
            ),
            footer=shad.Button("Mark all as read", width=252),
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": card.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_card(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    await flet_app_function.tester.enter_text(
        await flet_app_function.tester.find_by_key("name"), "my-app"
    )
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Deploy")
    )
    await flet_app_function.tester.pump_and_settle()

    assert (
        await flet_app_function.tester.find_by_text("Created project 'my-app'")
    ).count == 1
    flet_app_function.assert_screenshot(
        "card",
        await flet_app_function.take_page_controls_screenshot(
            bgcolor=ft.Colors.SURFACE
        ),
    )
