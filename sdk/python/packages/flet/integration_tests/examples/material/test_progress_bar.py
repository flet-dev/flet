import pytest

import flet as ft
import flet.testing as ftt

from examples.controls.progress_ring import determinate_and_indeterminate


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.ProgressBar(width=400, value=0.8),
    )


@pytest.mark.skip(reason="Test runs asynchronously")
@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": determinate_and_indeterminate.main}],
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
