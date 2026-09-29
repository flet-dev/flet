import flet_shadcn_ui as shad
import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_button_variants(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Row(
            [shad.Button(v.name.title(), variant=v) for v in shad.ButtonVariant],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_button_sizes(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Row([shad.Button(s.name.title(), size=s) for s in shad.ButtonSize]),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_button_lucide_icons(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Row(
            [
                shad.Button("Mail", leading=shad.LucideIcons.MAIL),
                shad.Button(
                    "Next",
                    trailing=shad.LucideIcons.CHEVRON_RIGHT,
                    variant=shad.ButtonVariant.OUTLINE,
                ),
            ]
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_card(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        shad.Card(
            width=320,
            title="Create project",
            description="Deploy your new project in one-click.",
            content=ft.Container(
                padding=ft.Padding.symmetric(vertical=16),
                content=shad.Input(placeholder="Name of your project"),
            ),
            footer=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    shad.Button("Cancel", variant=shad.ButtonVariant.OUTLINE),
                    shad.Button("Deploy"),
                ],
            ),
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_input(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            width=300,
            controls=[
                shad.Input(placeholder="Email", leading=shad.LucideIcons.MAIL),
                shad.Input(value="secret", password=True),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_checkbox(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            [
                shad.Checkbox(label="Unchecked"),
                shad.Checkbox(label="Checked", sublabel="With a sublabel", value=True),
            ]
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_switch(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            [
                shad.Switch(label="Off"),
                shad.Switch(label="On", value=True),
            ]
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_theme_violet_dark(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        shad.Theme(
            color_scheme=shad.ColorScheme.VIOLET,
            brightness=ft.Brightness.DARK,
            content=ft.Container(
                bgcolor="#020817",
                padding=16,
                content=ft.Row(
                    [
                        shad.Button("Primary"),
                        shad.Checkbox(label="Checked", value=True),
                        shad.Switch(value=True),
                    ]
                ),
            ),
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_follows_page_dark_mode(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.DARK
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Container(
            bgcolor=ft.Colors.SURFACE,
            padding=16,
            content=ft.Row([shad.Button("Primary"), shad.Switch(value=True)]),
        ),
    )
