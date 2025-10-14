import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Container(
            padding=10,
            content=ft.FilledIconButton(
                icon=ft.Icons.PHONE,
                badge=ft.Badge(label="3"),
            ),
        ),
    )


# @pytest.mark.asyncio(loop_scope="function")
# async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
#     page = flet_app_function.page
#     page.theme_mode = ft.ThemeMode.LIGHT
#     page.add(
#         ft.Container(
#             width=160,
#             height=120,
#             alignment=ft.alignment.center,
#             bgcolor=ft.Colors.SURFACE,
#             content=ft.IconButton(
#                 icon=ft.Icons.PHONE,
#                 badge=ft.Badge(label="3"),
#             ),
#         )
#     )
#     page.update()
#     screenshot = await flet_app_function.wrap_page_controls_in_screenshot(margin=12)
#     flet_app_function.assert_screenshot(
#         request.node.name,
#         await screenshot.capture(
#             pixel_ratio=flet_app_function.screenshots_pixel_ratio
#         ),
#     )
