import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.card import music_info


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Card(
            shadow_color=ft.Colors.ON_SURFACE_VARIANT,
            content=ft.Container(
                width=400,
                padding=10,
                content=ft.ListTile(
                    bgcolor=ft.Colors.GREY_400,
                    leading=ft.Icon(ft.Icons.FOREST),
                    title=ft.Text("Card Name"),
                ),
            ),
        ),
        similarity_threshold=98.4,
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": music_info.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_music_info(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "music_info",
        await flet_app_function.take_page_controls_screenshot(),
        similarity_threshold=98.4,
    )
