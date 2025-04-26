import asyncio
from typing import Any, Optional

from flet.controls.base_control import control
from flet.controls.services.service import Service

__all__ = ["UrlLauncher"]


@control("UrlLauncher")
class UrlLauncher(Service):
    async def launch_url_async(
        self,
        url: str,
        web_window_name: Optional[str] = None,
        web_popup_window: Optional[bool] = False,
        window_width: Optional[int] = None,
        window_height: Optional[int] = None,
    ) -> None:

        await self._invoke_method_async(
            "launch_url",
            {
                "url": url,
                "web_window_name": web_window_name,
                "web_popup_window": web_popup_window,
                "window_width": window_width,
                "window_height": window_height,
            },
        )

    def launch_url(
        self,
        url: str,
        web_window_name: Optional[str] = None,
        web_popup_window: Optional[bool] = False,
        window_width: Optional[int] = None,
        window_height: Optional[int] = None,
    ) -> None:
        asyncio.create_task(
            self.launch_url_async(
                url, web_window_name, web_popup_window, window_width, window_height
            )
        )

    async def can_launch_url_async(self, url: str) -> bool:
        return await self._invoke_method_async("can_launch_url", {"url": url})

    async def close_in_app_web_view_async(self) -> None:
        await self._invoke_method_async("close_in_app_web_view")

    def close_in_app_web_view(self) -> None:
        asyncio.create_task(self.close_in_app_web_view_async())
