import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.accordion.main as accordion
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=shad.Accordion(
            width=360,
            value=["a11y"],
            items=[
                shad.AccordionItem(
                    value="a11y",
                    title="Is it accessible?",
                    content=ft.Text("Yes. It adheres to WAI-ARIA."),
                ),
                shad.AccordionItem(
                    value="styled",
                    title="Is it styled?",
                    content=ft.Text("Yes."),
                ),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": accordion.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_accordion(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    scr = await flet_app_function.wrap_page_controls_in_screenshot(
        bgcolor=ft.Colors.SURFACE
    )
    flet_app_function.assert_screenshot(
        "accordion_initial",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Is it styled?")
    )
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("Expanded: styled")).count == 1
    flet_app_function.assert_screenshot(
        "accordion",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
    flet_app_function.create_gif(
        ["accordion_initial", "accordion"], "accordion_flow", duration=1000
    )
