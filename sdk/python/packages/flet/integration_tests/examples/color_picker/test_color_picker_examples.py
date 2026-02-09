import pytest

import flet as ft
import flet.testing as ftt
from flet_color_picker import (
    BlockPicker,
    ColorPicker,
    HueRingPicker,
    MaterialPicker,
    MultipleChoiceBlockPicker,
    SlidePicker,
)


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Column(
            intrinsic_width=True,
            controls=[ColorPicker()],
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_hue_ring_picker(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Column(
            intrinsic_width=True,
            controls=[HueRingPicker(color="#00ff00")],
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_slide_picker(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Column(
            intrinsic_width=True,
            controls=[SlidePicker(color="#0000ff")],
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_material_picker(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Column(
            intrinsic_width=True,
            controls=[MaterialPicker(color="#ff9800")],
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_block_picker(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Column(
            intrinsic_width=True,
            controls=[BlockPicker(color="#9c27b0")],
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_multiple_choice_block_picker(
    flet_app_function: ftt.FletTestApp, request
):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Column(
            intrinsic_width=True,
            controls=[
                MultipleChoiceBlockPicker(colors=["#03a9f4", "#4caf50", "#ffeb3b"])
            ],
        ),
    )
