import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Image(
            src="https://picsum.photos/seed/picsum/100/100",
            width=100,
            height=100,
            fit=ft.BoxFit.CONTAIN,
        ),
        pump_times=5,
        pump_duration=1000,
    )
