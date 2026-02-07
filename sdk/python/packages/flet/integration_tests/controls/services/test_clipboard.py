import base64
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt
from flet.controls.exceptions import FletUnimplementedPlatformException


# Create a new flet_app instance for each test method.
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_text(flet_app: ftt.FletTestApp):
    clipboard = ft.Clipboard()

    expected = "Flet clipboard integration test value"
    await clipboard.set(expected)
    actual = await clipboard.get()

    assert actual == expected


@pytest.mark.asyncio(loop_scope="function")
async def test_image(flet_app: ftt.FletTestApp):
    bytes_image = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAABkAAAAgCAYAAADnnNMGAAAACXBIWXMAAAORAAADkQFnq8zdAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAA6dJREFUSImllltoHFUYx3/fzOzm0lt23ZrQ1AQbtBehNpvQohgkBYVo410RwQctNE3Sh0IfiiBoIAjqi6TYrKnFy4O3oiiRavDJFi3mXomIBmOxNZe63ay52GR3Zj4f2sTEzmx3m//TYf7/c35zvgPnO6KqrESXqpq3muocAikv6m+/zytj3ejik1VN21G31YA9CgJ6xC+bMyQZPVCuarciPAMYC99V6Vw5pLbFSibHmlVoRVj9P3cmPBM8tSJI/M6mzabpfoAQ9fIF7WK4bd5vvuFnLGgy2vi0abg94A0AcJGvMq3hDxGRyar9r4F+iLAm0yIiRk8m37tctS1WsrIhhrI30+Srmg+J87OXUf3lWGS1q89dC6ltsSanxk4Aj2QBABii96300g87P/rtlrWr8l+vyDMfdlXSyyEikqxsiOUAQJCBhfHdXRfCq1LSsSlcWG+KBAGStvvrMkgiuv8lUc2mREukPwLUfHG+uTQv8Eown7VL3XlbBxYhf1c17hbVF3MDwA9bts280TnaU1YYqPby07aeFlUlHt27wSQ4CLo+F8AvoTCvHmyKF+ZbEb/M77P2LgvAwmrTHAHflN3KZxVbMC2jMFNOpgPnrMSOhvvFkMezXdwV4ePbtvHtxnJAMQ0j4JtVnO+eLb5oiSlt5HDbv7t1O90lpYCCCKbhfzW5kAIwUAazR0BlfII8Ow0I6uoVmI9MyAMwbMs8CExmDbk4zgu931MyO4OI4KrYflkRjOoTI+uM9d1vjotwKPu9QMk/sxzuO8POiVFcdZ1M2YBVsMEAKOqLvaPIe7mACuw0z/80SMH58SMplxlfiDhVi7dw2pltRhjKBQTQdrSja2KKTfE551NHuaZ0QVPvWYQUn31/Vm2nDvgjF4grVJx6suSvrvrSJ/6cSW2Oz9mf264uNrB806xZ1k/CZ49dUKgDEtlCROX2hfHpx8pGuuo3PpqYulw8fjndOp1yhgtNKRevJ1FyR2Ola+jXAjdnwTkZ6o896GdWdxDw7IxFg+0DpmXchTKSBWQnIuJn9u4j7dt+13UfHXEkXQOcuQ4kMhVtqsgUyPiQiPQfHw1NB2sRjmXKuTg1NwwBYLhtPtQX26eqTwGXPDOqvmcC4Hnwfrrad94GrVsOYTqUTkQY+iTlNe/6O1miSP/x0VB/+wMIDwHn/vtV1iQC4Xv95uUEWVCoL9Y5Z+gdovoyMHUFJHv88jmVy0vTuw7cZNv2YaA61Bfb7ZX5F8SaUv2xwZevAAAAAElFTkSuQmCC"
    )
    clipboard = ft.Clipboard()

    if not (flet_app.page.web or flet_app.page.platform.is_mobile()):
        with pytest.raises(FletUnimplementedPlatformException):
            await clipboard.set_image(bytes_image)
        return

    await clipboard.set_image(bytes_image)
    actual = await clipboard.get_image()

    assert isinstance(actual, bytes) and len(actual) > 0


@pytest.mark.asyncio(loop_scope="function")
async def test_files(flet_app: ftt.FletTestApp):
    clipboard = ft.Clipboard()

    if flet_app.page.web or not flet_app.page.platform.is_desktop():
        with pytest.raises(FletUnimplementedPlatformException):
            await clipboard.set_files(["/tmp/not-used.txt"])
        return

    with TemporaryDirectory() as tmp:
        file1 = Path(tmp) / "clipboard_file_1.txt"
        file1.write_text("file 1")
        file2 = Path(tmp) / "clipboard_file_2.txt"
        file2.write_text("file 2")

        expected = [str(file1), str(file2)]
        ok = await clipboard.set_files(expected)
        actual = await clipboard.get_files()

    assert ok is True
    assert set(actual) == set(expected)
