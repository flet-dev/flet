import pytest

import flet as ft
import flet.testing as ftt


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
