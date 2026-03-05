import pytest

import flet.testing as ftt
from examples.apps.expand import (
    expand_loose_chat_messages,
    expand_row_equal_split,
    expand_row_proportional_1_3_1,
    expand_textfield_in_row,
)


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": expand_textfield_in_row.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_expand_textfield_in_row(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "expand_textfield_in_row",
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": expand_row_proportional_1_3_1.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_expand_row_proportional_1_3_1(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "expand_row_proportional_1_3_1",
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": expand_row_equal_split.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_expand_row_equal_split(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "expand_row_equal_split",
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": expand_loose_chat_messages.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_expand_loose_chat_messages(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "expand_loose_chat_messages",
        await flet_app_function.take_page_controls_screenshot(),
    )
