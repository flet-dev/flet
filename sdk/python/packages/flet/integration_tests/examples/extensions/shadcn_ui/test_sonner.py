import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.sonner.main as sonner
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
    await _prepare(flet_app_function, 520, 260)
    for i in (1, 2):
        flet_app_function.page.show_dialog(
            shad.Sonner(
                title=f"Event {i} has been created",
                description="Sunday, December 03, 2023 at 9:00 AM",
                duration=ft.Duration(seconds=60),
            )
        )
        await flet_app_function.tester.pump_and_settle()
    await _capture(flet_app_function, request.node.name)


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": sonner.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_sonner(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    await _prepare(flet_app_function, 560, 360)

    frames = []
    for i in range(1, 4):
        await tester.tap(await tester.find_by_text("Add to calendar"))
        await tester.pump_and_settle()
        assert (await tester.find_by_text(f"Event {i} has been created")).count == 1
        name = f"sonner_{i}"
        await _capture(flet_app_function, name)
        frames.append(name)
    # Hovering expands the stack and shows each toast's close button.
    await tester.mouse_hover(await tester.find_by_text("Event 3 has been created"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "sonner_hover")
    frames.append("sonner_hover")

    flet_app_function.create_gif(frames, "sonner_flow", duration=1000)
