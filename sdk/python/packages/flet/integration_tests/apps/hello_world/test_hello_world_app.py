import app
import pytest

import flet.testing as ftt


@pytest.mark.parametrize(
    "flet_app",
    [
        {
            "flet_app_main": app.main,
        }
    ],
    indirect=True,
)
class TestHelloWorld:
    @pytest.mark.asyncio(loop_scope="module")
    async def test_app(self, flet_app: ftt.FletTestApp):
        await flet_app.tester.pump_and_settle()
        finder = await flet_app.tester.find_by_text("Hello, world!")
        assert finder.count == 1
        # bytes = await flet_app.tester.take_screenshot("scr1")
        # p = Path(get_current_script_dir(), "scr_1.png")
        # print(p)
        # with open(p, "wb") as f:
        #     f.write(bytes)

    @pytest.mark.asyncio(loop_scope="module")
    async def test_1(self, flet_app: ftt.FletTestApp):
        print("Test 1")

    @pytest.mark.asyncio(loop_scope="module")
    async def test_2(self, flet_app: ftt.FletTestApp):
        print("Test 2")
