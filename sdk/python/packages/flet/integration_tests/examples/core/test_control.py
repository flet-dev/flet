import pytest

import flet.testing as ftt
from examples.controls.control.expand_loose_chat_messages import (
    main as expand_loose_chat_messages_main,
)
from examples.controls.control.expand_row_equal_split import (
    main as expand_row_equal_split_main,
)
from examples.controls.control.expand_row_proportional_1_3_1 import (
    main as expand_row_proportional_1_3_1_main,
)
from examples.controls.control.expand_textfield_in_row import (
    main as expand_textfield_in_row_main,
)


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": expand_textfield_in_row_main.main}],
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
    [{"flet_app_main": expand_row_proportional_1_3_1_main.main}],
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
    [{"flet_app_main": expand_row_equal_split_main.main}],
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
    [{"flet_app_main": expand_loose_chat_messages_main.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_expand_loose_chat_messages(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "expand_loose_chat_messages",
        await flet_app_function.take_page_controls_screenshot(),
    )
