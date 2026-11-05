import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.theme.main as theme
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Column(
            intrinsic_width=True,
            controls=[
                shad.Theme(
                    color_scheme=scheme,
                    content=ft.Row(
                        [
                            shad.Button(scheme.name.title(), width=90),
                            shad.Switch(value=True),
                            shad.Checkbox(value=True),
                        ]
                    ),
                )
                for scheme in [
                    shad.ColorScheme.SLATE,
                    shad.ColorScheme.VIOLET,
                    shad.ColorScheme.ROSE,
                    shad.ColorScheme.GREEN,
                ]
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": theme.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_theme(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    scr = await flet_app_function.wrap_page_controls_in_screenshot(
        bgcolor=ft.Colors.SURFACE
    )
    flet_app_function.assert_screenshot(
        "theme",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )

    frames = ["theme"]
    for scheme in ["Rose", "Green"]:
        await flet_app_function.tester.tap(
            await flet_app_function.tester.find_by_key("color_scheme")
        )
        await flet_app_function.tester.pump_and_settle()
        await flet_app_function.tester.tap(
            (await flet_app_function.tester.find_by_text(scheme)).last
        )
        await flet_app_function.tester.pump_and_settle()
        name = f"theme_{scheme.lower()}"
        flet_app_function.assert_screenshot(
            name,
            await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
        )
        frames.append(name)

    flet_app_function.create_gif(frames, "theme_flow", duration=1000)
