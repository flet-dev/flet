from pathlib import Path

import flet as ft
import flet.testing as ftt
import pytest
import pytest_asyncio


@pytest_asyncio.fixture(scope="module")
async def flet_app(request):
    flet_app = ftt.FletTestApp(
        flutter_app_dir=(Path(__file__).parent / "../../../../../client").resolve(),
        test_path=request.fspath,
    )
    await flet_app.start()
    yield flet_app
    await flet_app.teardown()


@pytest.mark.asyncio(loop_scope="module")
async def test_app_bar(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.AppBar(
            bgcolor=ft.Colors.PRIMARY_CONTAINER,
            leading=ft.Icon(ft.Icons.PALETTE),
            leading_width=40,
            title=ft.Text("AppBar Test"),
            center_title=False,
            actions=[
                ft.IconButton(icon=ft.Icons.TAB),
                ft.IconButton(icon=ft.Icons.WALLET),
            ],
        ),
    )


# @pytest.mark.asyncio(loop_scope="module")
# async def test_checkbox_theme(flet_app: ftt.FletTestApp, request):
#     flet_app.page.theme_mode = ft.ThemeMode.LIGHT
#     await flet_app.assert_control_screenshot(
#         request.node.name,
#         ft.AlertDialog(),
#     )
