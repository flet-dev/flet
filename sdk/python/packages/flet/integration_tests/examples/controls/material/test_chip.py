import pytest

import examples.controls.material.chip.assist_chips.main as assist_chips
import examples.controls.material.chip.filter_chips.main as filter_chips
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Chip(
            label="Explore topics",
            leading=ft.Icon(ft.Icons.EXPLORE_OUTLINED),
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": assist_chips.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_assist_chips(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(450, 220)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "assist_chips",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": filter_chips.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_filter_chips(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(950, 250)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    dogs_ok = await flet_app_function.tester.find_by_text("Dogs OK")
    await flet_app_function.tester.tap(dogs_ok)
    await flet_app_function.tester.pump_and_settle()

    cats_ok = await flet_app_function.tester.find_by_text("Cats OK")
    await flet_app_function.tester.tap(cats_ok)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "filter_chips",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
