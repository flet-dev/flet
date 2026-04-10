import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.material.context_menu.custom_trigger import (
    main as custom_trigger,
)
from examples.controls.material.context_menu.programmatic_open import (
    main as programmatic_open,
)
from examples.controls.material.context_menu.triggers import main as triggers


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(250, 200)
    flet_app_function.page.add(
        menu := ft.ContextMenu(
            content=ft.IconButton(ft.Icons.MENU),
            items=[
                ft.PopupMenuItem("Rename"),
                ft.PopupMenuItem("Duplicate"),
            ],
        )
    )
    await flet_app_function.tester.pump_and_settle()

    # open menu
    await menu.open()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        request.node.name,
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": triggers.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_triggers(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(300, 300)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "before_click",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    trigger_area = await flet_app_function.tester.find_by_key(
        "context_menu_trigger_area"
    )
    await flet_app_function.tester.mouse_click(trigger_area)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "left_click_open",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    await flet_app_function.tester.tap_at(ft.Offset(20, 20))
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.tester.right_mouse_click(trigger_area)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "right_click_open",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    flet_app_function.create_gif(
        ["before_click", "left_click_open", "right_click_open"],
        "triggers_flow",
        duration=1000,
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": custom_trigger.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_custom_trigger(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(300, 300)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "before_double_click",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    trigger_area = await flet_app_function.tester.find_by_key(
        "context_menu_custom_trigger_area"
    )
    await flet_app_function.tester.mouse_double_click(trigger_area)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "after_double_click",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    flet_app_function.create_gif(
        ["before_double_click", "after_double_click"],
        "custom_trigger_flow",
        duration=1000,
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": programmatic_open.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_programmatic_open(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(300, 300)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    # click button to open menu
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Click to open menu")
    )
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        test_programmatic_open.__name__,
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
