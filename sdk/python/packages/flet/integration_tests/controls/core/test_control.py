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


@pytest.mark.asyncio(loop_scope="function")
async def test_tooltip_property(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.add(
        ft.IconButton(
            icon=ft.Icons.INFO_OUTLINED,
            tooltip="Info tooltip",
        )
    )
    await flet_app_function.tester.pump_and_settle()

    finder = await flet_app_function.tester.find_by_tooltip("Info tooltip")
    assert finder.count == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_tooltip_hover_screenshot(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(420, 300)
    flet_app_function.page.update()

    flet_app_function.page.add(
        ft.Container(
            padding=100,
            content=ft.IconButton(
                key="info_btn",
                icon=ft.Icons.INFO_OUTLINED,
                tooltip=ft.Tooltip(message="Tooltip message"),
            ),
        )
    )
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    button = await flet_app_function.tester.find_by_key("info_btn")
    await flet_app_function.tester.mouse_hover(button)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        request.node.name,
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_tooltip_custom_properties_screenshot(
    flet_app_function: ftt.FletTestApp, request
):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(460, 320)
    flet_app_function.page.update()

    flet_app_function.page.add(
        ft.Container(
            padding=100,
            content=ft.IconButton(
                key="info_btn_custom",
                icon=ft.Icons.HELP_OUTLINE,
                tooltip=ft.Tooltip(
                    message="Customized tooltip for Control.tooltip",
                    wait_duration=0,
                    show_duration=5000,
                    prefer_below=True,
                    vertical_offset=20,
                    bgcolor=ft.Colors.BLUE_GREY_900,
                    text_style=ft.TextStyle(
                        color=ft.Colors.WHITE, weight=ft.FontWeight.W_600, size=14
                    ),
                    padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                    margin=ft.Margin.only(top=8, left=8, right=8),
                    text_align=ft.TextAlign.CENTER,
                    decoration=ft.BoxDecoration(
                        border_radius=ft.BorderRadius.all(10),
                    ),
                ),
            ),
        )
    )
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    button = await flet_app_function.tester.find_by_key("info_btn_custom")
    await flet_app_function.tester.mouse_hover(button)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        request.node.name,
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
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


@pytest.mark.asyncio(loop_scope="module")
async def test_expand_loose_row(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            spacing=12,
            width=200,
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            expand=True,
                            bgcolor=ft.Colors.AMBER_300,
                            border_radius=8,
                            padding=10,
                            content=ft.Text("Strict expand"),
                        )
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Container(
                            expand=True,
                            expand_loose=True,
                            bgcolor=ft.Colors.CYAN_300,
                            border_radius=8,
                            padding=10,
                            content=ft.Text("Loose expand"),
                        ),
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Container(
                            expand=True,
                            expand_loose=True,
                            bgcolor=ft.Colors.LIGHT_GREEN_300,
                            border_radius=8,
                            padding=10,
                            content=ft.Text(
                                "Loose expand with longer text to show content-driven "
                                "width"
                            ),
                        ),
                    ],
                ),
            ],
        ),
    )
