import flet_core as ft
import pytest
from flet_core.protocol import Command


@pytest.mark.skip(reason="no way of currently testing this")
def test_page(page):
    assert page.url != "" and page.url.startswith("http"), "Test failed"
