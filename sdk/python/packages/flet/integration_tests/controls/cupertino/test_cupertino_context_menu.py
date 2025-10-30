import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_cupertino_context_menu_basic(flet_app: ftt.FletTestApp, request):
    ccm = ft.CupertinoContextMenu(
        enable_haptic_feedback=True,
        key="ccm",
        content=ft.Button("Click me", key="button"),
        actions=[
            ft.CupertinoContextMenuAction(
                content="Action 1",
                default=True,
                trailing_icon=ft.Icons.CHECK,
                on_click=lambda e: print("Action 1"),
            ),
            ft.CupertinoContextMenuAction(
                content="Action 2",
                trailing_icon=ft.Icons.MORE,
                on_click=lambda e: print("Action 2"),
            ),
            ft.CupertinoContextMenuAction(
                content="Action 3",
                destructive=True,
                trailing_icon=ft.Icons.CANCEL,
                on_click=lambda e: print("Action 3"),
            ),
        ],
    )
    flet_app.page.enable_screenshots = True
    await flet_app.resize_page(400, 600)
    flet_app.page.add(ccm)
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "cupertino_context_menu_basic",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )

    # open state
    await flet_app.tester.long_press(await flet_app.tester.find_by_key("ccm"))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "cupertino_context_menu_basic_open",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
