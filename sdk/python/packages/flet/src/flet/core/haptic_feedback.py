import asyncio
from typing import Any, Optional

from flet.core.control import Service, control
from flet.core.ref import Ref

__all__ = ["HapticFeedback"]


@control("HapticFeedback")
class HapticFeedback(Service):
    """
    Allows access to the haptic feedback interface on the device.

    It is non-visual and should be added to `page.overlay` list.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        hf = ft.HapticFeedback()
        page.services.append(hf)

        page.add(
            ft.ElevatedButton("Heavy impact", on_click=lambda _: hf.heavy_impact()),
            ft.ElevatedButton("Medium impact", on_click=lambda _: hf.medium_impact()),
            ft.ElevatedButton("Light impact", on_click=lambda _: hf.light_impact()),
            ft.ElevatedButton("Vibrate", on_click=lambda _: hf.vibrate()),
        )

    ft.run(main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/hapticfeedback
    """

    async def heavy_impact_async(self):
        await self._invoke_method_async("heavy_impact")

    def heavy_impact(self):
        asyncio.create_task(self.heavy_impact_async())

    async def light_impact_async(self):
        await self._invoke_method_async("light_impact")

    def light_impact(self):
        asyncio.create_task(self.light_impact_async())

    async def medium_impact_async(self):
        await self._invoke_method_async("medium_impact")

    def medium_impact(self):
        asyncio.create_task(self.medium_impact_async())

    async def vibrate_async(self):
        await self._invoke_method_async("vibrate")

    def vibrate(self):
        asyncio.create_task(self.vibrate_async())

    async def selection_click_async(self):
        await self._invoke_method_async("selection_click")

    def selection_click(self):
        asyncio.create_task(self.selection_click_async())
