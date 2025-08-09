import apps.finders as app
import flet as ft
import flet.testing as ftt
import pytest


@pytest.mark.parametrize(
    "flet_app",
    [
        {
            "flet_app_main": app.main,
        }
    ],
    indirect=True,
)
class TestFinders:
    @pytest.mark.asyncio(loop_scope="module")
    async def test_find_by_text(self, flet_app: ftt.FletTestApp):
        await flet_app.tester.pump(1000)
        finder = await flet_app.tester.find_by_text("Hello, world!")
        assert finder.count == 2

    @pytest.mark.asyncio(loop_scope="module")
    async def test_find_by_text_containing(self, flet_app: ftt.FletTestApp):
        finder = await flet_app.tester.find_by_text_containing("Hello, world!")
        assert finder.count == 3

        finder = await flet_app.tester.find_by_text_containing("Hello")
        assert finder.count == 4

        finder = await flet_app.tester.find_by_text_containing("(\\s+)world")
        assert finder.count == 3

        finder = await flet_app.tester.find_by_text_containing("world!$")
        assert finder.count == 3

    @pytest.mark.asyncio(loop_scope="module")
    async def test_find_by_icon(self, flet_app: ftt.FletTestApp):
        finder = await flet_app.tester.find_by_icon(ft.Icons.ADD_A_PHOTO)
        assert finder.count == 1

    @pytest.mark.asyncio(loop_scope="module")
    async def test_find_by_tooltip(self, flet_app: ftt.FletTestApp):
        finder = await flet_app.tester.find_by_tooltip("Tooltip1")
        assert finder.count == 1

    @pytest.mark.asyncio(loop_scope="module")
    async def test_find_by_key(self, flet_app: ftt.FletTestApp):
        finder = await flet_app.tester.find_by_key("value_key_1")
        assert finder.count == 1

        finder = await flet_app.tester.find_by_key(ft.ScrollKey("scroll_key_1"))
        assert finder.count == 1
