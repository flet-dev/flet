from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.duration import Duration
from flet.controls.types import Number

__all__ = ["Screenshot"]


@control("Screenshot")
class Screenshot(ConstrainedControl):
    """
    Screenshot takes a screenshot of containing control.

    Online docs: https://flet.dev/docs/controls/screenshot
    """

    content: Control
    """
    The `Control` to be captured.
    """

    async def capture_async(
        self, pixel_ratio: Optional[Number] = None, delay: Optional[Duration] = None
    ):
        return await self._invoke_method_async(
            "capture", arguments={"pixel_ratio": pixel_ratio, "delay": delay}
        )
