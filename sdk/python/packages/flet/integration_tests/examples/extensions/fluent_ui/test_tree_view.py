import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.tree_view.main as tree_view
import flet as ft
import flet.testing as ftt


async def _capture(app: ftt.FletTestApp, name: str):
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
            width=260,
            controls=[
                fluent.TreeView(
                    items=[
                        fluent.TreeViewItem(
                            "Documents",
                            expanded=True,
                            items=[
                                fluent.TreeViewItem("Report.docx"),
                                fluent.TreeViewItem("Budget.xlsx"),
                            ],
                        ),
                        fluent.TreeViewItem(
                            "Pictures", items=[fluent.TreeViewItem("Cat.png")]
                        ),
                    ]
                )
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": tree_view.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_tree_view(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(340, 280)
    flet_app_function.page.update()
    await tester.pump_and_settle()
    await _capture(flet_app_function, "tree_view_initial")

    # Items are selected with their checkboxes, which have no text or Flet
    # icon to find them by. Selecting a folder selects its files.
    await tester.tap_at(ft.Offset(32, 22))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("2 files to back up")).count == 1
    await _capture(flet_app_function, "tree_view_folder")

    await tester.tap_at(ft.Offset(56, 70))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("1 files to back up")).count == 1
    await _capture(flet_app_function, "tree_view")
    flet_app_function.create_gif(
        ["tree_view_initial", "tree_view_folder", "tree_view"],
        "tree_view_flow",
        duration=1000,
    )
