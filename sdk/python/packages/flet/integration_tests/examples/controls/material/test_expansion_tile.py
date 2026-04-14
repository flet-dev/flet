import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.material.expansion_tile.basic import main as basic
from examples.controls.material.expansion_tile.borders import main as borders


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.ExpansionTile(
            width=400,
            title="Account",
            subtitle="Manage profile and security",
            expanded=True,
            controls=[
                ft.ListTile(title=ft.Text("Profile")),
                ft.ListTile(title=ft.Text("Security")),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        test_basic.__name__,
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": borders.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_borders(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(460, 300)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "borders_closed",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    expand_icons = await flet_app_function.tester.find_by_icon(ft.Icons.EXPAND_MORE)
    assert expand_icons.count >= 1
    await flet_app_function.tester.tap(expand_icons.first)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "borders_opened",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    flet_app_function.create_gif(
        ["borders_closed", "borders_opened"],
        "borders_flow",
        duration=1000,
    )
