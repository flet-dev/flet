import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.resize_page(100, 300)
    flet_app_function.page.update()
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.ListView(
            controls=[ft.Text(f"Item {i}") for i in range(1, 6)],
            divider_thickness=1,
        ),
    )
