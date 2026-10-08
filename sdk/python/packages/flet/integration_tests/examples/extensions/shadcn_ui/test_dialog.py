import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.dialog.main as dialog
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
    await _prepare(flet_app_function, 520, 340)
    flet_app_function.page.show_dialog(
        shad.Dialog(
            title="Edit profile",
            description="Make changes to your profile here.",
            content=ft.Container(
                width=300,
                padding=ft.Padding.symmetric(vertical=12),
                content=shad.Input(value="Pedro Duarte"),
            ),
            actions=[shad.Button("Save changes")],
        )
    )
    await flet_app_function.tester.pump_and_settle()
    await _capture(flet_app_function, request.node.name)


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": dialog.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_dialog(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    await _prepare(flet_app_function, 640, 440)

    await tester.tap(await tester.find_by_text("Edit profile"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "dialog_profile")

    await tester.tap(await tester.find_by_text("Save changes"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Profile saved")).count == 1

    await tester.tap(await tester.find_by_text("Delete account"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "dialog_alert")

    await tester.tap(await tester.find_by_text("Continue"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Account deleted")).count == 1
    await _capture(flet_app_function, "dialog")
    flet_app_function.create_gif(
        ["dialog_profile", "dialog_alert", "dialog"], "dialog_flow", duration=1200
    )
