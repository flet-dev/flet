import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.material.outlined_button.basic.main import main as basic
from examples.controls.material.outlined_button.custom_content.main import (
    main as custom_content,
)
from examples.controls.material.outlined_button.handling_clicks.main import (
    main as handling_clicks,
)
from examples.controls.material.outlined_button.icons.main import main as icons


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.OutlinedButton(content="Outlined button"),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic}],
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
    [{"flet_app_main": custom_content}],
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
    [{"flet_app_main": icons}],
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
    [{"flet_app_main": handling_clicks}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_handling_clicks(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(300, 150)
    flet_app_function.page.update()
    ob = await flet_app_function.tester.find_by_text_containing("event")
    await flet_app_function.tester.tap(ob)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "handling_clicks1",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    await flet_app_function.tester.tap(ob)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "handling_clicks2",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    await flet_app_function.tester.tap(ob)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "handling_clicks3",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    flet_app_function.create_gif(
        ["handling_clicks1", "handling_clicks2", "handling_clicks3"],
        "handling_clicks",
        duration=1600,
    )
