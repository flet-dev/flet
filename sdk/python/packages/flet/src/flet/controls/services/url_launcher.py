from typing import Optional, Union

from flet.controls.base_control import control
from flet.controls.services.service import Service
from flet.controls.types import UrlTarget

__all__ = ["UrlLauncher"]


@control("UrlLauncher")
class UrlLauncher(Service):
    async def launch_url(
        self,
        url: str,
        web_window_name: Optional[Union[str, UrlTarget]] = None,
        web_popup_window: Optional[bool] = False,
        window_width: Optional[int] = None,
        window_height: Optional[int] = None,
    ) -> None:
        await self._invoke_method(
            "launch_url",
            {
                "url": url,
                "web_window_name": web_window_name,
                "web_popup_window": web_popup_window,
                "window_width": window_width,
                "window_height": window_height,
            },
        )

    async def can_launch_url(self, url: str) -> bool:
        return await self._invoke_method("can_launch_url", {"url": url})

    async def close_in_app_web_view(self) -> None:
        await self._invoke_method("close_in_app_web_view")
