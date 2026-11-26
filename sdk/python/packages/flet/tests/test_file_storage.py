import asyncio

import pytest

import flet as ft


class _Recorder(ft.FileStorage):
    """Captures what would be sent to the client instead of sending it."""

    def __init__(self):
        super().__init__()
        self.calls = []

    async def _invoke_method(self, method_name, arguments=None, timeout=None):
        self.calls.append((method_name, arguments))
        return None


def test_write_sends_bytes():
    fs = _Recorder()
    for data in (b"abc", bytearray(b"abc"), memoryview(b"abc")):
        asyncio.run(fs.write("db/app.sqlite", data))
    assert fs.calls == [("write", {"name": "db/app.sqlite", "data": b"abc"})] * 3
    assert all(type(args["data"]) is bytes for _, args in fs.calls)


@pytest.mark.parametrize("data", ["text", 42, [1, 2], None])
def test_write_refuses_anything_but_bytes(data):
    fs = _Recorder()
    with pytest.raises(TypeError):
        asyncio.run(fs.write("a", data))
    assert fs.calls == []


def test_methods_send_their_arguments():
    fs = _Recorder()
    asyncio.run(fs.read("a"))
    asyncio.run(fs.list("db/"))
    asyncio.run(fs.lock("db", timeout=0))
    asyncio.run(fs.unlock("db"))
    asyncio.run(fs.size())
    assert fs.calls == [
        ("read", {"name": "a"}),
        ("list", {"prefix": "db/"}),
        ("lock", {"name": "db", "timeout": 0}),
        ("unlock", {"name": "db"}),
        ("size", None),
    ]
