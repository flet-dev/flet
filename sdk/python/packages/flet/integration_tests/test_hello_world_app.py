import logging
from pathlib import Path

import apps.hello_world as app
import flet as ft
import pytest
import pytest_asyncio

logging.basicConfig(level=logging.DEBUG)


@pytest_asyncio.fixture
async def flet_app():
    flet_app = ft.FletTestApp(
        flutter_app_dir=(Path(__file__).parent / "../../../../../client").resolve(),
        flet_app_main=app.main,
        tcp_port=9010,
    )
    await flet_app.start()
    yield flet_app
    await flet_app.teardown()


@pytest.mark.asyncio
async def test_app(flet_app: ft.FletTestApp):
    await flet_app.tester.pump_and_settle()
    count = await flet_app.tester.count_by_text("Hello, world!")
    assert count == 1
