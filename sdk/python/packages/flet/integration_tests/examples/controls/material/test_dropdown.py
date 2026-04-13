import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.material.dropdown.color_selection_with_filtering import (
    main as color_selection_with_filtering,
)
from examples.controls.material.dropdown.icon_selection import main as icon_selection


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Dropdown(
            width=220,
            value="alice",
            options=[
                ft.dropdown.Option(key="alice", text="Alice"),
                ft.dropdown.Option(key="bob", text="Bob"),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": color_selection_with_filtering.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_color_selection_with_filtering(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(350, 300)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "closed_dropdown",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    dropdown = await flet_app_function.tester.find_by_key("color_dropdown")
    await flet_app_function.tester.tap(dropdown)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "opened_dropdown",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    await flet_app_function.tester.enter_text(dropdown, "re")
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "filtered_dropdown",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    red_options = await flet_app_function.tester.find_by_text("red")
    assert red_options.count >= 1
    await flet_app_function.tester.tap(red_options.last)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "selected_red",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    flet_app_function.create_gif(
        [
            "closed_dropdown",
            "opened_dropdown",
            "filtered_dropdown",
            "selected_red",
        ],
        "color_selection_with_filtering_flow",
        duration=1000,
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": icon_selection.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_icon_selection(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(350, 300)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "icon_selection_closed_dropdown",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    dropdown = await flet_app_function.tester.find_by_key("icon_dropdown")
    await flet_app_function.tester.tap(dropdown)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "icon_selection_opened_dropdown",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    heart_options = await flet_app_function.tester.find_by_icon(ft.Icons.FAVORITE)
    assert heart_options.count >= 1
    await flet_app_function.tester.tap(heart_options.last)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "icon_selection_selected_icon",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    flet_app_function.create_gif(
        [
            "icon_selection_closed_dropdown",
            "icon_selection_opened_dropdown",
            "icon_selection_selected_icon",
        ],
        "icon_selection_flow",
        duration=1000,
    )
