import pytest

import flet as ft
import flet.testing as ftt

from . import app


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
    async def test_auto_update(self, flet_app: ftt.FletTestApp):
        tester = flet_app.tester
        await tester.pump_and_settle()
        auto_update_enabled = await tester.find_by_text("Auto update enabled: True")
        assert auto_update_enabled.count == 1

        # tap 1st button
        await tester.tap(await tester.find_by_text("auto_update_global_enabled"))
        await tester.pump_and_settle()
        assert (await tester.find_by_text("Global auto update")).count == 1

        # tap 2nd button
        await tester.tap(await tester.find_by_text("disable_autoupdate_no_update"))
        await tester.pump_and_settle()
        assert (await tester.find_by_text("Auto update no update")).count == 0

        # tap 3rd button
        await tester.tap(await tester.find_by_text("disable_autoupdate_with_update"))
        await tester.pump_and_settle()
        assert (await tester.find_by_text("Auto update with update")).count == 1
        assert (await tester.find_by_text("Auto update no update")).count == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_context_throws_exception_outside_flet_app():
    with pytest.raises(Exception, match="The context is not associated with any page."):
        p = ft.context.page  # noqa: F841
