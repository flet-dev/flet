import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_rotated_box(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.RotatedBox(
            quarter_turns=1,
            content=ft.Container(
                width=220,
                height=120,
                bgcolor=ft.Colors.TEAL_300,
                border_radius=16,
                alignment=ft.Alignment.CENTER,
                content=ft.Text("RotatedBox", size=28, weight=ft.FontWeight.BOLD),
            ),
        ),
    )
