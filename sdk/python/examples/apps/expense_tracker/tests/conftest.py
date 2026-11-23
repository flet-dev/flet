"""In-memory stand-ins for device storage, so tests never touch real data."""

import pytest
from services.receipts import ReceiptPhotos
from state import AppState
from storage import Storage


class MemoryPreferences:
    """SharedPreferences in a dict. Set `fail` to make every write fail."""

    def __init__(self, values=None):
        self.values = dict(values or {})
        self.fail = False

    async def get(self, key):
        return self.values.get(key)

    async def set(self, key, value):
        if self.fail:
            return False
        self.values[key] = value
        return True

    async def remove(self, key):
        self.values.pop(key, None)
        return True

    async def get_keys(self, prefix):
        return [key for key in self.values if key.startswith(prefix)]


@pytest.fixture
def storage():
    # Storage() and ReceiptPhotos() need a running page; skip __init__.
    storage = object.__new__(Storage)
    storage.prefs = MemoryPreferences()
    return storage


@pytest.fixture
def photos():
    photos = object.__new__(ReceiptPhotos)
    photos.web = True  # browser mode: photos live in preferences
    photos.mobile = False
    photos.prefs = MemoryPreferences()
    return photos


@pytest.fixture
async def state(storage, photos):
    state = AppState(storage, photos)
    await state.load()
    assert state.status == "ready"
    return state
