import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.progress.main as progress
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=shad.Progress(value=0.6, width=300),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": progress.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_progress(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    scr = await flet_app_function.wrap_page_controls_in_screenshot(
        bgcolor=ft.Colors.SURFACE
    )
    flet_app_function.assert_screenshot(
        "progress_initial",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )

    frames = ["progress_initial"]
    for step in range(2):
        await flet_app_function.tester.tap(
            await flet_app_function.tester.find_by_text("Step")
        )
        await flet_app_function.tester.pump_and_settle()
        name = f"progress_step_{step + 1}"
        flet_app_function.assert_screenshot(
            name,
            await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
        )
        frames.append(name)

    assert (await flet_app_function.tester.find_by_text("60%")).count == 1
    flet_app_function.create_gif(frames, "progress_flow", duration=1000)
