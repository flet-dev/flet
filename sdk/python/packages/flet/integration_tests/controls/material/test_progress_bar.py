import pytest
import asyncio
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_determinate(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.ProgressBar(
            width=400, color=ft.Colors.GREEN_400, bgcolor=ft.Colors.GREY_400, value=0.5
        ),
    )
