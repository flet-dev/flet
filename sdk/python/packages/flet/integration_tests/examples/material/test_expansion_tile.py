import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.expansion_tile import basic


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.ExpansionTile(
            width=400,
            title="Account",
            subtitle="Manage profile and security",
            expanded=True,
            controls=[
                ft.ListTile(title=ft.Text("Profile")),
                ft.ListTile(title=ft.Text("Security")),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        test_basic.__name__,
        await flet_app_function.take_page_controls_screenshot(),
    )
