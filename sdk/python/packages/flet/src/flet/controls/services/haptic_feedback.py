from flet.controls.base_control import control
from flet.controls.services.service import Service

__all__ = ["HapticFeedback"]


@control("HapticFeedback")
class HapticFeedback(Service):
    """
    Allows access to the haptic feedback interface on the device.
    """

    async def heavy_impact(self):
        """
        Provides a haptic feedback corresponding a collision impact with a heavy mass.
        """
        await self._invoke_method("heavy_impact")

    async def light_impact(self):
        """
        Provides a haptic feedback corresponding a collision impact with a light mass.
        """
        await self._invoke_method("light_impact")

    async def medium_impact(self):
        """
        Provides a haptic feedback corresponding a collision impact with a medium mass.
        """
        await self._invoke_method("medium_impact")

    async def vibrate(self):
        """
        Provides vibration haptic feedback to the user for a short duration.
        """
        await self._invoke_method("vibrate")

    async def selection_click(self):
        """
        TBD
        """
        await self._invoke_method("selection_click")
