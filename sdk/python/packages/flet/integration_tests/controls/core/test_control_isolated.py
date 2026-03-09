import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_tooltip_property(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.add(
        ft.IconButton(
            icon=ft.Icons.INFO_OUTLINED,
            tooltip="Info tooltip",
        )
    )
    await flet_app_function.tester.pump_and_settle()

    finder = await flet_app_function.tester.find_by_tooltip("Info tooltip")
    assert finder.count == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_tooltip_hover_screenshot(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(420, 300)
    flet_app_function.page.update()

    flet_app_function.page.add(
        ft.Container(
            padding=100,
            content=ft.IconButton(
                key="info_btn",
                icon=ft.Icons.INFO_OUTLINED,
                tooltip=ft.Tooltip(message="Tooltip message"),
            ),
        )
    )
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    button = await flet_app_function.tester.find_by_key("info_btn")
    await flet_app_function.tester.mouse_hover(button)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        request.node.name,
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_tooltip_custom_properties_screenshot(
    flet_app_function: ftt.FletTestApp, request
):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(460, 320)
    flet_app_function.page.update()

    flet_app_function.page.add(
        ft.Container(
            padding=100,
            content=ft.IconButton(
                key="info_btn_custom",
                icon=ft.Icons.HELP_OUTLINE,
                tooltip=ft.Tooltip(
                    message="Customized tooltip for Control.tooltip",
                    wait_duration=0,
                    show_duration=5000,
                    prefer_below=True,
                    vertical_offset=20,
                    bgcolor=ft.Colors.BLUE_GREY_900,
                    text_style=ft.TextStyle(
                        color=ft.Colors.WHITE, weight=ft.FontWeight.W_600, size=14
                    ),
                    padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                    margin=ft.Margin.only(top=8, left=8, right=8),
                    text_align=ft.TextAlign.CENTER,
                    decoration=ft.BoxDecoration(
                        border_radius=ft.BorderRadius.all(10),
                    ),
                ),
            ),
        )
    )
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    button = await flet_app_function.tester.find_by_key("info_btn_custom")
    await flet_app_function.tester.mouse_hover(button)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        request.node.name,
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
