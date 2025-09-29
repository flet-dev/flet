import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_basic(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.IconButton(icon=ft.Icons.PHONE, badge=ft.Badge()),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_properties1(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.IconButton(
            icon=ft.Icons.PHONE,
            badge=ft.Badge(
                label="1",
                offset=ft.Offset(5, 5),
                alignment=ft.Alignment(-1, -1),
                bgcolor=ft.Colors.GREEN,
                # label_visible=False,
                large_size=20,
                small_size=10,
                padding=ft.Padding.all(5),
                text_color=ft.Colors.YELLOW,
                text_style=ft.TextStyle(
                    size=10,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK,
                    italic=True,
                ),
            ),
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_small_size(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.IconButton(
            icon=ft.Icons.PHONE,
            badge=ft.Badge(
                # label="1",
                offset=ft.Offset(5, 5),
                alignment=ft.Alignment(-1, -1),
                bgcolor=ft.Colors.GREEN,
                # label_visible=False,
                large_size=20,
                small_size=10,
                # padding=ft.Padding.all(5),
                # text_color=ft.Colors.YELLOW,
                # text_style=ft.TextStyle(
                #     size=10,
                #     weight=ft.FontWeight.BOLD,
                #     color=ft.Colors.BLACK,
                #     italic=True,
                # ),
            ),
        ),
    )
