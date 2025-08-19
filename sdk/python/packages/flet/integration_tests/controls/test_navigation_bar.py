import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_navigation_bar(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Explore"),
                ft.NavigationBarDestination(icon=ft.Icons.COMMUTE, label="Commute"),
                ft.NavigationBarDestination(
                    icon=ft.Icons.BOOKMARK_BORDER,
                    selected_icon=ft.Icons.BOOKMARK,
                    label="Favorites",
                ),
            ]
        ),
    )
