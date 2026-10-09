import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.resizable.main as resizable
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Container(
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=8,
            content=shad.ResizablePanelGroup(
                width=300,
                height=120,
                show_handle=True,
                panels=[
                    shad.ResizablePanel(
                        default_size=0.4,
                        content=ft.Container(
                            alignment=ft.Alignment.CENTER, content=ft.Text("One")
                        ),
                    ),
                    shad.ResizablePanel(
                        default_size=0.6,
                        content=ft.Container(
                            alignment=ft.Alignment.CENTER, content=ft.Text("Two")
                        ),
                    ),
                ],
            ),
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": resizable.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_resizable(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    scr = await flet_app_function.wrap_page_controls_in_screenshot(
        bgcolor=ft.Colors.SURFACE
    )
    flet_app_function.assert_screenshot(
        "resizable_initial",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )

    handle = await flet_app_function.tester.find_by_icon(shad.LucideIcons.GRIP_VERTICAL)
    assert handle.count == 1
    await flet_app_function.tester.drag(handle, ft.Offset(-120, 0))
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "resizable",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
    flet_app_function.create_gif(
        ["resizable_initial", "resizable"], "resizable_flow", duration=1000
    )
