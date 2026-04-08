import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.CupertinoListTile(
            title="Notifications",
            subtitle="Enabled",
            width=400,
            leading=ft.Icon(ft.Icons.NOTIFICATIONS_OUTLINED),
            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        ),
    )
