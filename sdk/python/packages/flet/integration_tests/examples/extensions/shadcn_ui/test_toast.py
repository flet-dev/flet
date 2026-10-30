import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.toast.main as toast
import flet as ft
import flet.testing as ftt


async def _capture(app: ftt.FletTestApp, name: str):
    app.assert_screenshot(
        name,
        await app.page.take_screenshot(pixel_ratio=app.screenshots_pixel_ratio),
    )


async def _prepare(app: ftt.FletTestApp, width: int, height: int):
    app.page.theme_mode = ft.ThemeMode.LIGHT
    app.page.enable_screenshots = True
    app.resize_page(width, height)
    app.page.update()
    await app.tester.pump_and_settle()


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    await _prepare(flet_app_function, 520, 220)
    flet_app_function.page.show_dialog(
        shad.Toast(
            title="Scheduled: Catch up",
            description="Friday, February 10, 2023 at 5:57 PM",
            action=shad.Button("Undo", variant=shad.ButtonVariant.OUTLINE),
            duration=ft.Duration(seconds=60),
        )
    )
    await flet_app_function.tester.pump_and_settle()
    await _capture(flet_app_function, request.node.name)


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": toast.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_toast(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    await _prepare(flet_app_function, 560, 320)

    await tester.tap(await tester.find_by_text("Show toast"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Scheduled: Catch up")).count == 1
    await _capture(flet_app_function, "toast_regular")

    await tester.tap(await tester.find_by_text("Undo"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Undone")).count == 1
    assert (await tester.find_by_text("Scheduled: Catch up")).count == 0

    await tester.tap(await tester.find_by_text("Show error"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Uh oh! Something went wrong.")).count == 1
    await _capture(flet_app_function, "toast")

    await tester.tap(await tester.find_by_text("Try again"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Uh oh! Something went wrong.")).count == 0
    flet_app_function.create_gif(
        ["toast_regular", "toast"], "toast_flow", duration=1200
    )
