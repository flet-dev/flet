from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.duration import DurationValue
from flet.controls.types import Number

__all__ = ["Screenshot"]


@control("Screenshot")
class Screenshot(Control):
    """
    Takes a screenshot of containing control.
    """

    content: Control
    """
    The control to be captured.
    """

    async def capture(
        self,
        pixel_ratio: Optional[Number] = None,
        delay: Optional[DurationValue] = None,
    ) -> bytes:
        """
        Captures a screenshot of the enclosed content control.

        Args:
            pixel_ratio: A pixel ratio of the captured screenshot.
                If `None`, device-specific pixel ratio will be used.
            delay: A delay before taking a screenshot.
                The delay will be 20 milliseconds if not specified.

        Returns:
            Screenshot in PNG format.
        """
        return await self._invoke_method(
            "capture", arguments={"pixel_ratio": pixel_ratio, "delay": delay}
        )
