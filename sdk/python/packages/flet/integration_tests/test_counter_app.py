import logging
from pathlib import Path

import apps.counter as app
import flet as ft
import flet.testing as ftt
import pytest
import pytest_asyncio

logging.basicConfig(level=logging.DEBUG)


@pytest_asyncio.fixture(scope="module")
async def flet_app(request):
    flet_app = ftt.FletTestApp(
        flutter_app_dir=(Path(__file__).parent / "../../../../../client").resolve(),
        flet_app_main=app.main,
        test_path=request.fspath,
    )
    await flet_app.start()
    yield flet_app
    await flet_app.teardown()


@pytest.mark.asyncio(loop_scope="module")
async def test_app(flet_app: ftt.FletTestApp):
    tester = flet_app.tester
    await tester.pump_and_settle()
    zero_text = await tester.find_by_text("0")
    assert zero_text.count == 1

    # tap increment button
    increment_btn = await tester.find_by_icon(ft.Icons.ADD)
    assert increment_btn.count == 1
    await tester.tap(increment_btn)
    await tester.pump_and_settle()
    assert (await tester.find_by_text("1")).count == 1

    # tap decrement button
    decrement_button = await tester.find_by_key("decrement")
    assert decrement_button.count == 1
    await tester.tap(decrement_button)
    await tester.tap(decrement_button)
    await tester.pump_and_settle()
    assert (await tester.find_by_text("-1")).count == 1
