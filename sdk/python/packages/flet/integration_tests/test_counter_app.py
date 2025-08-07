import apps.counter as app
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
class TestApp:
    @pytest.mark.asyncio(loop_scope="module")
    async def test_app(self, flet_app: ftt.FletTestApp):
        tester = flet_app.tester
        await tester.pump_and_settle()
        zero_text = await tester.find_by_text("0")
        assert zero_text.count == 1

        # tap increment button
        increment_btn = await tester.find_by_icon(ft.Icons.ADD)
        assert increment_btn.count == 1
        await tester.tap(increment_btn)
        await tester.pump_and_settle()
        assert (await tester.find_by_text("1")).count == 1

        # tap decrement button
        decrement_button = await tester.find_by_key("decrement")
        assert decrement_button.count == 1
        await tester.tap(decrement_button)
        await tester.tap(decrement_button)
        await tester.pump_and_settle()
        assert (await tester.find_by_text("-1")).count == 1
