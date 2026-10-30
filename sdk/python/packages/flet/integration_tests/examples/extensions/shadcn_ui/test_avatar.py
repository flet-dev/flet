import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.avatar.main as avatar
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
                        shad.Avatar(placeholder="CN"),
                        shad.Avatar(placeholder="JD", size=48),
                        shad.Avatar(
                            placeholder=ft.Icon(shad.LucideIcons.USER, size=20)
                        ),
                    ]
                )
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": avatar.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_avatar(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    # Let the network image load before the screenshot.
    for _ in range(10):
        await flet_app_function.tester.pump(duration=ft.Duration(milliseconds=300))
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("JD")).count == 1
    flet_app_function.assert_screenshot(
        "avatar",
        await flet_app_function.take_page_controls_screenshot(
            bgcolor=ft.Colors.SURFACE
        ),
    )
