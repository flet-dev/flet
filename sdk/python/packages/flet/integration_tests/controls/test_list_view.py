import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_list_view_basic(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.ListView(
            controls=[
                ft.ListTile("List Tile"),
            ]
        ),
    )


# @pytest.mark.asyncio(loop_scope="module")
# async def test_list_view_horizontal(flet_app: ftt.FletTestApp, request):
#     flet_app.page.theme_mode = ft.ThemeMode.LIGHT
#     await flet_app.assert_control_screenshot(
#         request.node.name,
#         ft.ListView(
#             horizontal=True,
#             controls=[
#                 ft.ListTile("List Tile"),
#             ],
#         ),
#     )
