import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Text("Hello, world!"),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_bold(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Text("Hello, world!", weight=ft.FontWeight.BOLD),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_overflow(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            width=100,
            controls=[
                ft.Text(
                    value="Hello World! This is some very long text.",
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
                ft.Text(
                    value="Hello World! This is some very long text.",
                    style=ft.TextStyle(
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                ),
            ],
        ),
    )
