import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_align_inside_stack(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Stack(
            [
                ft.Button("A", align=ft.Alignment(0, 0)),
                ft.Button("B", align=ft.Alignment(0.9, 0.9)),
                ft.Button("C", align=ft.Alignment.BOTTOM_LEFT),
            ],
            width=200,
            height=200,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_align_inside_container(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Container(
            ft.Button("B", align=ft.Alignment(0.9, 0.9)),
            width=200,
            height=200,
        ),
    )
