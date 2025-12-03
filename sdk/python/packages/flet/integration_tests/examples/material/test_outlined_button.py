import pytest

import flet as ft
import flet.testing as ftt

from examples.controls.outlined_button import (
    basic,
    custom_content,
    icons,
    handling_clicks,
)


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.OutlinedButton(content="Outlined button"),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.assert_screenshot(
        "basic",
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": custom_content.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_custom_content(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.assert_screenshot(
        "custom_content",
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": icons.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_icons(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.assert_screenshot(
        "icons",
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": handling_clicks.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_handling_clicks(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(300, 150)
    flet_app_function.page.update()
    ob = await flet_app_function.tester.find_by_text_containing("event")
    await flet_app_function.tester.tap(ob)
    await flet_app_function.tester.pump_and_settle(
        duration=ft.Duration(milliseconds=500)
    )
    flet_app_function.assert_screenshot(
        "handling_clicks1",
        await flet_app_function.page.take_screenshot(),
    )
    await flet_app_function.tester.tap(ob)
    await flet_app_function.tester.pump_and_settle(
        duration=ft.Duration(milliseconds=500)
    )
    flet_app_function.assert_screenshot(
        "handling_clicks2",
        await flet_app_function.page.take_screenshot(),
    )
    await flet_app_function.tester.tap(ob)
    await flet_app_function.tester.pump_and_settle(
        duration=ft.Duration(milliseconds=500)
    )
    flet_app_function.assert_screenshot(
        "handling_clicks3",
        await flet_app_function.page.take_screenshot(),
    )

    flet_app_function.create_gif(
        ["handling_clicks1", "handling_clicks2", "handling_clicks3"],
        "handling_clicks",
        duration=1600,
    )
