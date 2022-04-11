import pytest

from flet import TextField


@pytest.mark.skip(reason="no way of currently testing this")
def test_update_single_control(page):
    txt = TextField(id="txt1", label="First name:")
    page.add(txt)
    page.update(txt)
