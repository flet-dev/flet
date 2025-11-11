import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.skip(
    reason="temporarily disabled due to reference image generation failure"
)
@pytest.mark.asyncio(loop_scope="module")
async def test_basic(flet_app: ftt.FletTestApp, request):
    ca = ft.CircleAvatar(
        foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
        content=ft.Text("FF"),
    )
    await flet_app.assert_control_screenshot(request.node.name, ca)


@pytest.mark.asyncio(loop_scope="module")
async def test_icon_content(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.CircleAvatar(
            content=ft.Icon(ft.Icons.ABC),
        ),
    )
