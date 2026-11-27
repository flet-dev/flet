import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.command_bar.main as command_bar
import flet as ft
import flet.testing as ftt


async def _capture(app: ftt.FletTestApp, name: str):
    # The "More" menu opens over the page, so these are full-page screenshots.
    app.assert_screenshot(
        name,
        await app.page.take_screenshot(pixel_ratio=app.screenshots_pixel_ratio),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Column(
            width=460,
            controls=[
                fluent.CommandBar(
                    primary_items=[
                        fluent.CommandBarButton(
                            icon=fluent.FluentIcons.ADD, content="New"
                        ),
                        fluent.CommandBarButton(
                            icon=fluent.FluentIcons.DELETE, content="Delete"
                        ),
                        fluent.CommandBarSeparator(),
                        fluent.CommandBarButton(
                            icon=fluent.FluentIcons.SHARE, content="Share"
                        ),
                    ],
                    secondary_items=[
                        fluent.CommandBarButton(
                            icon=fluent.FluentIcons.SETTINGS, content="Settings"
                        ),
                    ],
                )
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": command_bar.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_command_bar(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(520, 260)
    flet_app_function.page.update()
    await tester.pump_and_settle()
    await _capture(flet_app_function, "command_bar_initial")

    await tester.tap(await tester.find_by_text("Archive"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Archive clicked")).count == 1
    await _capture(flet_app_function, "command_bar_clicked")

    await tester.tap(await tester.find_by_tooltip("See more"))
    await tester.pump_and_settle()
    await _capture(flet_app_function, "command_bar_open")

    await tester.tap(await tester.find_by_text("Mark as read"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Mark as read clicked")).count == 1
    await _capture(flet_app_function, "command_bar")
    flet_app_function.create_gif(
        [
            "command_bar_initial",
            "command_bar_clicked",
            "command_bar_open",
            "command_bar",
        ],
        "command_bar_flow",
        duration=1000,
    )
