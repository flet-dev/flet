import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.PageView(
            height=220,
            viewport_fraction=0.85,
            controls=[
                ft.Container(
                    bgcolor=ft.Colors.PURPLE,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text("One", color=ft.Colors.WHITE),
                ),
                ft.Container(
                    bgcolor=ft.Colors.TEAL,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text("Two", color=ft.Colors.WHITE),
                ),
                ft.Container(
                    bgcolor=ft.Colors.AMBER,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Text("Three", color=ft.Colors.BLACK),
                ),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_unbounded_height(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            controls=[
                ft.PageView(
                    controls=[
                        ft.Container(
                            bgcolor=ft.Colors.PURPLE,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Text("One", color=ft.Colors.WHITE),
                        ),
                        ft.Container(
                            bgcolor=ft.Colors.TEAL,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Text("Two", color=ft.Colors.WHITE),
                        ),
                    ],
                )
            ]
        ),
    )
