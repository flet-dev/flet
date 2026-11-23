import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.content_dialog.main as content_dialog
import flet as ft
import flet.testing as ftt


async def _capture(app: ftt.FletTestApp, name: str):
    # The dialog is drawn over the page, so these are full-page screenshots.
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
    await _prepare(flet_app_function, 560, 320)
    flet_app_function.page.show_dialog(
        fluent.ContentDialog(
            title="Delete file?",
            content="The file will be deleted permanently.",
            actions=[fluent.FilledButton("Delete"), fluent.Button("Cancel")],
        )
    )
    await flet_app_function.tester.pump_and_settle()
    await _capture(flet_app_function, request.node.name)


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": content_dialog.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_content_dialog(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    await _prepare(flet_app_function, 560, 320)

    await tester.tap(await tester.find_by_text("Delete file"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "content_dialog_open")

    await tester.tap(await tester.find_by_text("Delete"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("File deleted")).count == 1
    await _capture(flet_app_function, "content_dialog")
    flet_app_function.create_gif(
        ["content_dialog_open", "content_dialog"],
        "content_dialog_flow",
        duration=1200,
    )
