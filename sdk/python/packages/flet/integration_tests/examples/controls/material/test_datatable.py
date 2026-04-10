import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.material.data_table.adaptive_row_heights import (
    main as adaptive_row_heights,
)
from examples.controls.material.data_table.basic import main as basic
from examples.controls.material.data_table.handling_events import (
    main as handling_events,
)
from examples.controls.material.data_table.sortable_and_selectable import (
    main as sortable_and_selectable,
)


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Name")),
                ft.DataColumn(label=ft.Text("Role")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Alice")),
                        ft.DataCell(ft.Text("Engineer")),
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Bob")),
                        ft.DataCell(ft.Text("Designer")),
                    ]
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
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(355, 260)
    flet_app_function.page.update()

    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "basic",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": sortable_and_selectable.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_sortable_and_selectable(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(500, 620)
    flet_app_function.page.update()

    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "sortable_and_selectable",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": adaptive_row_heights.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_adaptive_row_heights(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(620, 420)
    flet_app_function.page.update()

    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "adaptive_row_heights",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": handling_events.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_handling_events(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(760, 380)
    flet_app_function.page.update()

    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "handling_events_initial",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    row_a = await flet_app_function.tester.find_by_text("A")
    await flet_app_function.tester.mouse_hover(row_a)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "handling_events_hover_row_a",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    await flet_app_function.tester.tap(row_a)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "handling_events_click_row_a",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    column_1 = await flet_app_function.tester.find_by_text("Column 1")
    await flet_app_function.tester.mouse_hover(column_1)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "handling_events_hover_column_1",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    await flet_app_function.tester.tap(column_1)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "handling_events_click_column_1",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    flet_app_function.create_gif(
        [
            "handling_events_initial",
            "handling_events_hover_row_a",
            "handling_events_click_row_a",
            "handling_events_hover_column_1",
            "handling_events_click_column_1",
        ],
        "handling_events_flow",
        duration=1000,
    )
