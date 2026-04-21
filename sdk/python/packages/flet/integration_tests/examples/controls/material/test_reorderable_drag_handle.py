import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.material.reorderable_drag_handle.basic.main import main as basic


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.resize_page(420, 500)
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.ReorderableListView(
            show_default_drag_handles=False,
            controls=[
                ft.ListTile(
                    title=ft.Text(f"Draggable Item {i}", color=ft.Colors.BLACK),
                    leading=ft.ReorderableDragHandle(
                        content=ft.Icon(ft.Icons.DRAG_INDICATOR, color=ft.Colors.RED),
                        mouse_cursor=ft.MouseCursor.GRAB,
                    ),
                )
                for i in range(10)
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.resize_page(420, 500)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    initial_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot("basic_initial", initial_frame)
    frames = [initial_frame]

    drag_handle = await flet_app_function.tester.find_by_key("drag_handle_0")

    # Step 1: move item 0 downward and capture the intermediate state.
    await flet_app_function.tester.drag(drag_handle, ft.Offset(0, 110))
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    # Step 2: continue dragging the same item downward and capture again.
    drag_handle = await flet_app_function.tester.find_by_key("drag_handle_0")
    await flet_app_function.tester.drag(drag_handle, ft.Offset(0, 110))
    await flet_app_function.tester.pump_and_settle()
    frames.append(
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        )
    )

    # Step 3: move item 0 to its expected final position.
    drag_handle = await flet_app_function.tester.find_by_key("drag_handle_0")
    await flet_app_function.tester.drag(drag_handle, ft.Offset(0, 110))
    await flet_app_function.tester.pump_and_settle()

    reordered_frame = await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    )
    flet_app_function.assert_screenshot("basic_reordered", reordered_frame)
    frames.append(reordered_frame)

    flet_app_function.create_gif(frames=frames, output_name="basic", duration=800)
