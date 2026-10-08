"""Images for the Shadcn overview page (index.md); each matches a snippet there."""

import flet_shadcn_ui as shad
import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_usage(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=shad.Button("Continue", leading=shad.LucideIcons.ARROW_RIGHT),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_theming(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=shad.Theme(
            color_scheme=shad.ColorScheme.VIOLET,
            content=ft.Column([shad.Button("Save"), shad.Switch(label="Notify me")]),
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_icons(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Row(
            tight=True,
            controls=[
                ft.Icon(shad.LucideIcons.HOUSE),
                ft.Icon(shad.LucideIcons.BELL, color=ft.Colors.AMBER),
                ft.IconButton(shad.LucideIcons.SETTINGS),
                shad.IconButton(icon=shad.LucideIcons.HEART),
            ],
        ),
    )
