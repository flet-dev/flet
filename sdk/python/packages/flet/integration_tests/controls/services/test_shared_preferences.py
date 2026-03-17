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
    prefix = f"it_sp_{uuid4().hex}"

    values = {
        f"{prefix}_str": "hello",
        f"{prefix}_int": 123,
        f"{prefix}_float": 123.25,
        f"{prefix}_bool": True,
        f"{prefix}_list": ["a", "b", "c"],
    }

    # initially keys should not exist
    for key in values:
        assert await prefs.contains_key(key) is False

    # set values
    for key, value in values.items():
        assert await prefs.set(key, value) is True

    # get values
    for key, value in values.items():
        assert await prefs.get(key) == value
        assert await prefs.contains_key(key) is True

    # keys with prefix should be returned
    keys = await prefs.get_keys(prefix)
    for key in values:
        assert key in keys

    # remove one key
    first_key = next(iter(values))
    assert await prefs.remove(first_key) is True
    assert await prefs.contains_key(first_key) is False
    assert await prefs.get(first_key) is None

    # clear everything
    assert await prefs.clear() is True
    for key in values:
        assert await prefs.contains_key(key) is False
        assert await prefs.get(key) is None

    # unsupported types should fail
    unsupported_values = {
        f"{prefix}_dict": {"a": 1},
        f"{prefix}_tuple": ("a", "b"),
        f"{prefix}_list_int": [1, 2, 3],
        f"{prefix}_none": None,
    }
    for key, value in unsupported_values.items():
        with pytest.raises(ValueError, match="Unsupported value type"):
            await prefs.set(key, value)  # type: ignore[arg-type]
        assert await prefs.contains_key(key) is False
