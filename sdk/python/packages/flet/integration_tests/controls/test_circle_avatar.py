import flet as ft
import flet.testing as ftt
import pytest


@pytest.mark.asyncio(loop_scope="module")
async def test_circle_avatar(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    ca = ft.CircleAvatar(
        foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
        content=ft.Text("FF"),
    )
    await flet_app.assert_control_screenshot(request.node.name, ca)


@pytest.mark.asyncio(loop_scope="module")
async def test_icon_circle_avatar(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.CircleAvatar(content=ft.Icon(ft.Icons.ABC)),
    )
