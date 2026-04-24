import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.ExpansionPanelList(
            width=400,
            controls=[
                ft.ExpansionPanel(
                    header=ft.Text("Shipping address"),
                    content=ft.Text("123 Market Street, Springfield"),
                    expanded=True,
                ),
                ft.ExpansionPanel(
                    header=ft.Text("Billing address"),
                    content=ft.Text("Same as shipping"),
                ),
            ],
        ),
    )
