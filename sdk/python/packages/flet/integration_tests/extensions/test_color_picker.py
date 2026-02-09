import pytest

import flet.testing as ftt
from flet_color_picker import (
    BlockPicker,
    ColorPicker,
    HueRingPicker,
    MaterialPicker,
    MultipleChoiceBlockPicker,
    SlidePicker,
)


@pytest.mark.asyncio(loop_scope="module")
async def test_color_picker_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ColorPicker(
            color="#ff0000",
            color_picker_width=320,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_color_picker_hue_ring(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        HueRingPicker(
            color="#00ff00",
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_color_picker_slide(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        SlidePicker(
            color="#0000ff",
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_color_picker_material(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        MaterialPicker(
            color="#ff9800",
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_color_picker_block(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        BlockPicker(
            color="#9c27b0",
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_color_picker_multiple_choice_block(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        MultipleChoiceBlockPicker(
            colors=["#03a9f4", "#4caf50", "#ffeb3b"],
        ),
    )
