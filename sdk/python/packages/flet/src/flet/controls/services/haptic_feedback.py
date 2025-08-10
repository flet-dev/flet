from flet.controls.base_control import control
from flet.controls.services.service import Service

__all__ = ["HapticFeedback"]


@control("HapticFeedback")
class HapticFeedback(Service):
    """
    Allows access to the haptic feedback interface on the device.

    It is non-visual and should be added to
    [`Page.services`][flet.Page.services] list before it can be used.
    """

    async def heavy_impact_async(self):
        """
        Provides a haptic feedback corresponding a collision impact with a heavy mass.
        """
        await self._invoke_method_async("heavy_impact")

    async def light_impact_async(self):
        """
        Provides a haptic feedback corresponding a collision impact with a light mass.
        """
        await self._invoke_method_async("light_impact")

    async def medium_impact_async(self):
        """
        Provides a haptic feedback corresponding a collision impact with a medium mass.
        """
        await self._invoke_method_async("medium_impact")

    async def vibrate_async(self):
        """
        Provides vibration haptic feedback to the user for a short duration.
        """
        await self._invoke_method_async("vibrate")

    async def selection_click_async(self):
        """
        TBD
        """
        await self._invoke_method_async("selection_click")
