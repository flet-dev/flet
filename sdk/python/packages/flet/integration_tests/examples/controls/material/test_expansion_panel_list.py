import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.material.expansion_panel_list.basic import main as basic
from examples.controls.material.expansion_panel_list.scrollable import (
    main as scrollable,
)


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.ExpansionPanelList(
            width=400,
            controls=[
                ft.ExpansionPanel(
                    header=ft.Text("Details"),
                    content=ft.Text("More information here"),
                    expanded=True,
                ),
                ft.ExpansionPanel(
                    header=ft.Text("History"),
                    content=ft.Text("View previous updates"),
                ),
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
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(420, 500)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "basic_header_placeholder_opened",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    expand_icons = await flet_app_function.tester.find_by_icon(ft.Icons.EXPAND_MORE)
    assert expand_icons.count >= 1
    await flet_app_function.tester.tap(expand_icons.first)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "basic_header_placeholder_closed",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    expand_icons = await flet_app_function.tester.find_by_icon(ft.Icons.EXPAND_MORE)
    assert expand_icons.count >= 2
    await flet_app_function.tester.tap(expand_icons.at(1))
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "basic_panel_0_opened",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    delete_icons = await flet_app_function.tester.find_by_icon(ft.Icons.DELETE)
    assert delete_icons.count >= 1
    await flet_app_function.tester.mouse_hover(delete_icons.first)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "basic_panel_0_delete_hovered",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    await flet_app_function.tester.tap(delete_icons.first)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "basic_panel_0_deleted",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    flet_app_function.create_gif(
        [
            "basic_header_placeholder_opened",
            "basic_header_placeholder_closed",
            "basic_panel_0_opened",
            "basic_panel_0_delete_hovered",
            "basic_panel_0_deleted",
        ],
        "basic_flow",
        duration=1000,
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": scrollable.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_scrollable(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(420, 500)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "scrollable",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
