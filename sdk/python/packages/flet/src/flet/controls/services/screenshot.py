from typing import Optional, Union

from flet.controls.base_control import control
from flet.controls.duration import Duration
from flet.controls.keys import ScreenshotKey
from flet.controls.services.service import Service
from flet.controls.types import Number

__all__ = ["Screenshot"]


@control("Screenshot")
class Screenshot(Service):
    async def capture_async(
        self,
        screenshot_key: Union[ScreenshotKey, str, int, float, bool, None],
        pixel_ratio: Optional[Number] = None,
        delay: Optional[Duration] = None,
    ):
        return await self._invoke_method_async(
            "capture",
            arguments={
                "screenshot_key": screenshot_key,
                "pixel_ratio": pixel_ratio,
                "delay": delay,
            },
        )
