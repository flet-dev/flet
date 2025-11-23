import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Pagelet(
            appbar=ft.AppBar(title="Pagelet AppBar"),
            content=ft.Text("Pagelet Content"),
            width=350,
            height=300,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_cupertino_adaptive(flet_app: ftt.FletTestApp, request):
    flet_app.page.platform = ft.PagePlatform.MACOS
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Pagelet(
            adaptive=True,
            width=350,
            height=300,
            appbar=ft.AppBar(title="Pagelet AppBar"),
            content=ft.Text("Pagelet Content"),
            navigation_bar=ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(icon=ft.Icons.ADD, label="New"),
                    ft.NavigationBarDestination(icon=ft.Icons.INBOX, label="Inbox"),
                ],
            ),
        ),
    )
