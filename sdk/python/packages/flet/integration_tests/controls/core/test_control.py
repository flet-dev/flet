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
async def test_disabled_propagates_to_children(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            spacing=12,
            controls=[
                ft.Column(
                    spacing=8,
                    controls=[
                        ft.Text("Enabled parent"),
                        ft.TextField(label="Name", value="John"),
                        ft.Button("Save"),
                    ],
                ),
                ft.Column(
                    disabled=True,
                    spacing=8,
                    controls=[
                        ft.Text("Disabled parent"),
                        ft.TextField(label="Name", value="John"),
                        ft.Button("Save"),
                    ],
                ),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_badge(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Container(
            padding=10,
            content=ft.Row(
                spacing=20,
                controls=[
                    ft.Container(
                        padding=10,
                        content=ft.FilledIconButton(
                            icon=ft.Icons.NOTIFICATIONS_OUTLINED,
                            badge="3",
                        ),
                    ),
                    ft.Container(
                        padding=10,
                        content=ft.FilledIconButton(
                            icon=ft.Icons.MAIL_OUTLINED,
                            badge=ft.Badge(
                                label="99+",
                                bgcolor=ft.Colors.RED_400,
                                text_color=ft.Colors.WHITE,
                                alignment=ft.Alignment(1, -1),
                                offset=ft.Offset(-2, 2),
                            ),
                        ),
                    ),
                ],
            ),
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_opacity(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            spacing=10,
            controls=[
                ft.Container(
                    width=260,
                    height=46,
                    bgcolor=ft.Colors.BLUE_300,
                    alignment=ft.Alignment.CENTER,
                    border_radius=8,
                    content=ft.Text("opacity=1.0"),
                    opacity=1.0,
                ),
                ft.Container(
                    width=260,
                    height=46,
                    bgcolor=ft.Colors.BLUE_300,
                    alignment=ft.Alignment.CENTER,
                    border_radius=8,
                    content=ft.Text("opacity=0.6"),
                    opacity=0.6,
                ),
                ft.Container(
                    width=260,
                    height=46,
                    bgcolor=ft.Colors.BLUE_300,
                    alignment=ft.Alignment.CENTER,
                    border_radius=8,
                    content=ft.Text("opacity=0.25"),
                    opacity=0.25,
                ),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_rtl(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            spacing=12,
            controls=[
                ft.Container(
                    width=320,
                    border=ft.Border.all(1, ft.Colors.BLUE_GREY_200),
                    padding=10,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        controls=[
                            ft.Container(
                                width=44, height=30, bgcolor=ft.Colors.RED_300
                            ),
                            ft.Container(
                                width=44, height=30, bgcolor=ft.Colors.GREEN_300
                            ),
                            ft.Container(
                                width=44, height=30, bgcolor=ft.Colors.BLUE_300
                            ),
                        ],
                    ),
                ),
                ft.Container(
                    width=320,
                    border=ft.Border.all(1, ft.Colors.BLUE_GREY_200),
                    padding=10,
                    content=ft.Row(
                        rtl=True,
                        alignment=ft.MainAxisAlignment.START,
                        controls=[
                            ft.Container(
                                width=44, height=30, bgcolor=ft.Colors.RED_300
                            ),
                            ft.Container(
                                width=44, height=30, bgcolor=ft.Colors.GREEN_300
                            ),
                            ft.Container(
                                width=44, height=30, bgcolor=ft.Colors.BLUE_300
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_col(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Container(
            width=520,
            padding=10,
            border=ft.Border.all(1, ft.Colors.BLUE_GREY_200),
            border_radius=8,
            content=ft.ResponsiveRow(
                run_spacing=8,
                spacing=8,
                controls=[
                    ft.Container(
                        col=6,
                        height=52,
                        bgcolor=ft.Colors.CYAN_300,
                        border_radius=8,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Text("col=6"),
                    ),
                    ft.Container(
                        col=6,
                        height=52,
                        bgcolor=ft.Colors.AMBER_300,
                        border_radius=8,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Text("col=6"),
                    ),
                    ft.Container(
                        col={"sm": 4, "md": 3},
                        height=52,
                        bgcolor=ft.Colors.PINK_200,
                        border_radius=8,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Text('col={"sm":4,"md":3}'),
                    ),
                    ft.Container(
                        col={"sm": 8, "md": 9},
                        height=52,
                        bgcolor=ft.Colors.GREEN_200,
                        border_radius=8,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Text('col={"sm":8,"md":9}'),
                    ),
                ],
            ),
        ),
    )
