import asyncio

from flet.controls.base_control import control
from flet.controls.services.service import Service

__all__ = ["HapticFeedback"]


@control("HapticFeedback")
class HapticFeedback(Service):
    """
    Allows access to the haptic feedback interface on the device.

    It is non-visual and should be added to `page.services` list.

    Online docs: https://flet.dev/docs/controls/hapticfeedback
    """

    async def heavy_impact_async(self):
        """
        Provides a haptic feedback corresponding a collision impact with a heavy mass.
        """
        await self._invoke_method_async("heavy_impact")

    def heavy_impact(self):
        """
        Provides a haptic feedback corresponding a collision impact with a heavy mass.
        """
        asyncio.create_task(self.heavy_impact_async())

    async def light_impact_async(self):
        """
        Provides a haptic feedback corresponding a collision impact with a light mass.
        """
        await self._invoke_method_async("light_impact")

    def light_impact(self):
        """
        Provides a haptic feedback corresponding a collision impact with a light mass.
        """
        asyncio.create_task(self.light_impact_async())

    async def medium_impact_async(self):
        """
        Provides a haptic feedback corresponding a collision impact with a medium mass.
        """
        await self._invoke_method_async("medium_impact")

    def medium_impact(self):
        """
        Provides a haptic feedback corresponding a collision impact with a medium mass.
        """
        asyncio.create_task(self.medium_impact_async())

    async def vibrate_async(self):
        """
        Provides vibration haptic feedback to the user for a short duration.
        """
        await self._invoke_method_async("vibrate")

    def vibrate(self):
        """
        Provides vibration haptic feedback to the user for a short duration.
        """
        asyncio.create_task(self.vibrate_async())

    async def selection_click_async(self):
        """
        TBD
        """
        await self._invoke_method_async("selection_click")

    def selection_click(self):
        """
        TBD
        """
        asyncio.create_task(self.selection_click_async())
