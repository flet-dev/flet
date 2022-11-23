import beartype.roar
import pytest

import flet as ft
from flet.protocol import Command


@pytest.mark.skip(reason="no way of currently testing this")
def test_page(page):
    assert page.url != "" and page.url.startswith("http"), "Test failed"
