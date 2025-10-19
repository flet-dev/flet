import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.BottomAppBar(
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            content=ft.Row(
                controls=[
                    ft.IconButton(ft.Icons.MENU),
                    ft.IconButton(ft.Icons.SEARCH),
                    ft.IconButton(ft.Icons.SETTINGS),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
        ),
    )
