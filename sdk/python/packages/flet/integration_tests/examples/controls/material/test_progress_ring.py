import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.material.progress_ring.determinate_and_indeterminate import (
    main as determinate_and_indeterminate,
)
from examples.controls.material.progress_ring.gauge_with_progress import (
    main as gauge_with_progress,
)


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.ProgressRing(value=0.4, padding=ft.Padding.all(10)),
    )


@pytest.mark.skip(reason="Will fix later")
@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": gauge_with_progress}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_gauge_with_progress(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "gauge_with_progress",
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.skip(reason="Test runs asynchronously")
@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": determinate_and_indeterminate}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_determinate_and_indeterminate(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.page.update()

    flet_app_function.assert_screenshot(
        "determinate_and_indeterminate",
        await flet_app_function.page.take_screenshot(delay=ft.Duration(seconds=15)),
    )
