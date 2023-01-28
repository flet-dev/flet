import dataclasses
import time
from typing import Any, Optional

from flet_core.callable_control import CallableControl
from flet_core.ref import Ref


class HapticFeedback(CallableControl):
    """
    Allows access to the haptic feedback interface on the device.

    It is non-visual and should be added to `page.overlay` list.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        hf = ft.HapticFeedback()
        page.overlay.append(hf)

        page.add(
            ft.ElevatedButton("Heavy impact", on_click=lambda _: hf.heavy_impact()),
            ft.ElevatedButton("Medium impact", on_click=lambda _: hf.medium_impact()),
            ft.ElevatedButton("Light impact", on_click=lambda _: hf.light_impact()),
            ft.ElevatedButton("Vibrate", on_click=lambda _: hf.vibrate()),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/hapticfeedback
    """

    def __init__(
        self,
        ref: Optional[Ref] = None,
        data: Any = None,
    ):

        CallableControl.__init__(
            self,
            ref=ref,
            data=data,
        )

    def _get_control_name(self):
        return "hapticfeedback"

    def _is_isolated(self):
        return True

    def heavy_impact(self):
        self._call_method("heavy_impact", [], wait_for_result=False)

    async def heavy_impact_async(self):
        await self._call_method_async("heavy_impact", [], wait_for_result=False)

    def light_impact(self):
        self._call_method("light_impact", [], wait_for_result=False)

    async def light_impact_async(self):
        await self._call_method_async("light_impact", [], wait_for_result=False)

    def medium_impact(self):
        self._call_method("medium_impact", [], wait_for_result=False)

    async def medium_impact_async(self):
        await self._call_method_async("medium_impact", [], wait_for_result=False)

    def vibrate(self):
        self._call_method("vibrate", [], wait_for_result=False)

    async def vibrate_async(self):
        await self._call_method_async("vibrate", [], wait_for_result=False)
