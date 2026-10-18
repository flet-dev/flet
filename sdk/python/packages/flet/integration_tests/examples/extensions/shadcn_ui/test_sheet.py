import asyncio

import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.sheet.main as sheet
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
    await _prepare(flet_app_function, 640, 360)
    flet_app_function.page.show_dialog(
        shad.Sheet(
            side=shad.SheetSide.RIGHT,
            title="Edit profile",
            description="Make changes to your profile here.",
            content=shad.Input(value="Pedro Duarte", width=260),
            actions=[shad.Button("Save changes")],
        )
    )
    await flet_app_function.tester.pump_and_settle()
    await _capture(flet_app_function, request.node.name)


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": sheet.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_sheet(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    await _prepare(flet_app_function, 720, 440)

    await tester.tap(await tester.find_by_text("Right"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Pedro Duarte")).count == 1
    await _capture(flet_app_function, "sheet_open")

    await tester.tap(await tester.find_by_text("Save changes"))
    await tester.pump_and_settle()
    # Give the dismiss animation + on_dismiss round-trip one more settle pass.
    await asyncio.sleep(0.5)
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Closed the right sheet")).count == 1
    await _capture(flet_app_function, "sheet")
    flet_app_function.create_gif(["sheet_open", "sheet"], "sheet_flow", duration=1200)
