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
        ft.Divider(),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_properties(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Divider(
            color=ft.Colors.RED,
            height=50,
            thickness=2,
            leading_indent=20,
            trailing_indent=20,
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_divider_radius(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Divider(
            color=ft.Colors.RED,
            height=40,
            radius=20,
            thickness=30,
            leading_indent=20,
            trailing_indent=20,
        ),
    )
