import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.material.list_tile.basic import main as basic


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.ListTile(
            width=400,
            leading=ft.Icon(ft.Icons.ACCOUNT_CIRCLE),
            title="Jane Doe",
            subtitle="Product Manager",
            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        ),
    )


# @pytest.mark.skip(reason="Will fix later")
@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.resize_page(560, 620)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    # Asset-backed Image in the example needs one timed pump to finish painting.
    flet_app_function.assert_screenshot(
        "basic",
        await flet_app_function.take_page_controls_screenshot(
            pump_times=7,
            pump_duration=1000,
        ),
    )
