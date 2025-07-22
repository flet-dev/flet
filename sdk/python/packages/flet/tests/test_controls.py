import logging

import flet as ft
import pytest
import pytest_asyncio

from .flutter_test import FlutterTest

logging.basicConfig(level=logging.DEBUG)


@pytest_asyncio.fixture
async def flutter_test():
    """Async Pytest fixture for the FlutterTest class."""
    test = FlutterTest(
        flutter_app_dir="/Users/feodor/projects/flet-dev/flet/client", tcp_port=9010
    )
    await test.start()
    yield test
    await test.teardown()


@pytest.mark.asyncio
async def test_hello(flutter_test):
    print("Session acquired!")
    flutter_test.page.add(ft.Text("Hello, world!"))
