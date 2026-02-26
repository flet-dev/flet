import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_visible(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            spacing=8,
            controls=[
                ft.Container(
                    width=260,
                    height=44,
                    bgcolor=ft.Colors.GREEN_300,
                    border_radius=8,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text("Visible: True"),
                ),
                ft.Container(
                    width=260,
                    height=44,
                    bgcolor=ft.Colors.RED_300,
                    border_radius=8,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text("Visible: False"),
                    visible=False,
                ),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_parent_not_visible_child_visible(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            spacing=8,
            controls=[
                ft.Container(
                    width=260,
                    height=44,
                    bgcolor=ft.Colors.GREEN_300,
                    border_radius=8,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text("Visible sibling"),
                ),
                ft.Container(
                    visible=False,
                    content=ft.Container(
                        visible=True,
                        width=260,
                        height=44,
                        bgcolor=ft.Colors.RED_300,
                        border_radius=8,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Text("Hidden parent, visible child"),
                    ),
                ),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_expand_row_remaining_space(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Container(
            width=480,
            padding=10,
            border=ft.Border.all(2, ft.Colors.BLUE_GREY_200),
            border_radius=10,
            content=ft.Row(
                controls=[
                    ft.TextField(hint_text="Enter your name", expand=True),
                    ft.Button("Join chat"),
                ]
            ),
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_expand_row_proportions_1_3_1(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Container(
            width=500,
            padding=10,
            border=ft.Border.all(2, ft.Colors.BLUE_GREY_200),
            border_radius=10,
            content=ft.Row(
                spacing=8,
                controls=[
                    ft.Container(
                        expand=1,
                        height=60,
                        bgcolor=ft.Colors.CYAN_300,
                        alignment=ft.Alignment.CENTER,
                        border_radius=8,
                        content=ft.Text("1"),
                    ),
                    ft.Container(
                        expand=3,
                        height=60,
                        bgcolor=ft.Colors.AMBER_300,
                        alignment=ft.Alignment.CENTER,
                        border_radius=8,
                        content=ft.Text("3"),
                    ),
                    ft.Container(
                        expand=1,
                        height=60,
                        bgcolor=ft.Colors.PINK_200,
                        alignment=ft.Alignment.CENTER,
                        border_radius=8,
                        content=ft.Text("1"),
                    ),
                ],
            ),
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_expand_row_equal_split(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Container(
            width=500,
            height=180,
            padding=10,
            border=ft.Border.all(2, ft.Colors.BLUE_GREY_200),
            border_radius=10,
            content=ft.Row(
                spacing=8,
                controls=[
                    ft.Container(
                        expand=True,
                        bgcolor=ft.Colors.ORANGE_300,
                        border_radius=8,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Text("Card 1"),
                    ),
                    ft.Container(
                        expand=True,
                        bgcolor=ft.Colors.GREEN_200,
                        border_radius=8,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Text("Card 2"),
                    ),
                ],
            ),
        ),
    )
