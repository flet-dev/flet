import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.separator.main as separator
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Column(
            width=240,
            spacing=0,
            controls=[
                ft.Text("Account"),
                shad.Separator(),
                ft.Row(
                    height=20,
                    controls=[
                        ft.Text("Blog"),
                        shad.Separator(vertical=True),
                        ft.Text("Docs"),
                    ],
                ),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": separator.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_separator(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("Docs")).count == 1
    flet_app_function.assert_screenshot(
        "separator",
        await flet_app_function.take_page_controls_screenshot(
            bgcolor=ft.Colors.SURFACE
        ),
    )
