import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.CupertinoActivityIndicator(
            radius=30,
            color=ft.CupertinoColors.DARK_BACKGROUND_GRAY,
            animating=False,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_progress(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.CupertinoActivityIndicator(
            radius=30,
            color=ft.CupertinoColors.DARK_BACKGROUND_GRAY,
            progress=0.5,
        ),
    )
