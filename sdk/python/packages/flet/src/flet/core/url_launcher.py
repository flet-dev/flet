from typing import Optional

from flet.core.control import Service, control


@control("UrlLauncher")
class UrlLauncher(Service):

    def launch_url(
        self,
        url: str,
        web_window_name: Optional[str] = None,
        web_popup_window: Optional[bool] = False,
        window_width: Optional[int] = None,
        window_height: Optional[int] = None,
    ) -> None:
        args = {"url": url}
        if web_window_name:
            args["web_window_name"] = web_window_name
        if web_popup_window:
            args["web_popup_window"] = str(web_popup_window)
        if window_width:
            args["window_width"] = str(window_width)
        if window_height:
            args["window_height"] = str(window_height)
        self.invoke_method("launch_url", args)

    def can_launch_url(self, url: str) -> bool:
        return self.invoke_method("can_launch_url", {"url": url})

    async def can_launch_url_async(self, url: str) -> bool:
        return await self.invoke_method_async("can_launch_url", {"url": url})

    def close_in_app_web_view(self) -> None:
        self.invoke_method("close_in_app_web_view")
