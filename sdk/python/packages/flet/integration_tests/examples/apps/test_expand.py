import pytest

import flet.testing as ftt
from examples.apps.expand import expand_example_1, expand_example_2, expand_example_3


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": expand_example_1.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_expand_example_1(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "expand_example_1",
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": expand_example_2.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_expand_example_2(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "expand_example_2",
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": expand_example_3.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_expand_example_3(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "expand_example_3",
        await flet_app_function.take_page_controls_screenshot(),
    )
