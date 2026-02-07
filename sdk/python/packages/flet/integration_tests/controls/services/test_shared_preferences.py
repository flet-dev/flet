from uuid import uuid4

import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method.
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_crud_flow(flet_app: ftt.FletTestApp):
    prefs = ft.SharedPreferences()
    prefix = f"it_sp_{uuid4().hex}_"
    key_1 = f"{prefix}key_1"
    key_2 = f"{prefix}key_2"

    assert await prefs.contains_key(key_1) is False
    assert await prefs.set(key_1, "value-1") is True
    assert await prefs.set(key_2, "value-2") is True
    assert await prefs.get(key_1) == "value-1"
    assert await prefs.contains_key(key_1) is True

    keys = await prefs.get_keys(prefix)
    assert key_1 in keys
    assert key_2 in keys

    assert await prefs.remove(key_1) is True
    assert await prefs.contains_key(key_1) is False
    assert await prefs.get(key_1) is None

    assert await prefs.clear() is True
    assert await prefs.get(key_2) is None
