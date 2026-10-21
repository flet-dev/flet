from dataclasses import dataclass
from typing import Any, Optional, Union

import flet as ft


@dataclass
class WebViewPageEvent(ft.Event["FletWebviewAll"]):
    """A page-load event containing the affected URL."""

    url: str


@dataclass
class WebViewProgressEvent(ft.Event["FletWebviewAll"]):
    """A page-load progress update, from 0 through 100."""

    progress: int


@dataclass
class WebViewResourceErrorEvent(ft.Event["FletWebviewAll"]):
    """Details reported by the platform for a failed web resource."""

    domain: str
    description: str
    error_code: int
    error_type: str
    is_for_main_frame: bool


@dataclass
class WebViewJavaScriptMessageEvent(ft.Event["FletWebviewAll"]):
    """A message posted by a registered JavaScript channel."""

    channel_name: str
    message_body: str


@dataclass
class WebViewNavigationRequestEvent(ft.Event["FletWebviewAll"]):
    """A navigation request observed by the WebView."""

    url: str
    is_main_frame: bool


@dataclass
class WebViewPermissionRequestEvent(ft.Event["FletWebviewAll"]):
    """A web page requested access to protected WebView resources."""

    resource_types: list[str]


@dataclass
class WebViewScrollEvent(ft.Event["FletWebviewAll"]):
    """A WebView scroll-position update."""

    x: int
    y: int


@dataclass
class WebViewConsoleMessageEvent(ft.Event["FletWebviewAll"]):
    """A message written to the page JavaScript console."""

    message: str
    level: str


@ft.control("flet_webview_all")
class FletWebviewAll(ft.LayoutControl):
    """A unified, controllable WebView backed by ``webview_all``.

    Event handlers receive the typed event objects declared above. Controller
    methods are coroutines and must be awaited after the control is on a page.
    """

    url: Optional[str] = None
    html: Optional[str] = None
    allow_navigation: bool = True
    zoom_enabled: bool = True
    javascript_enabled: bool = True
    javascript_mode: Optional[Union[str, bool]] = None
    javascript_channels: Optional[list[str]] = None
    user_agent: Optional[str] = None
    debugging_enabled: bool = False
    background_color: Optional[ft.ColorValue] = None
    allow_webview_permissions: bool = False
    remote_debugging_port: Optional[int] = None

    on_page_started: Optional[ft.EventHandler[WebViewPageEvent]] = None
    on_page_finished: Optional[ft.EventHandler[WebViewPageEvent]] = None
    on_progress: Optional[ft.EventHandler[WebViewProgressEvent]] = None
    on_web_resource_error: Optional[ft.EventHandler[WebViewResourceErrorEvent]] = None
    on_navigation_request: Optional[ft.EventHandler[WebViewNavigationRequestEvent]] = None
    on_javascript_message: Optional[
        ft.EventHandler[WebViewJavaScriptMessageEvent]
    ] = None
    on_permission_request: Optional[ft.EventHandler[WebViewPermissionRequestEvent]] = None
    on_scroll_position_change: Optional[ft.EventHandler[WebViewScrollEvent]] = None
    on_console_message: Optional[ft.EventHandler[WebViewConsoleMessageEvent]] = None

    async def reload(self) -> None:
        """Reload the current page."""
        await self._invoke_method("reload")

    async def stop_loading(self) -> None:
        """Best-effort cancellation of the current document load."""
        await self._invoke_method("stop_loading")

    async def can_go_back(self) -> bool:
        """Return whether browser history has a previous entry."""
        return await self._invoke_method("can_go_back")

    async def go_back(self) -> None:
        """Navigate to the previous history entry, if any."""
        await self._invoke_method("go_back")

    async def can_go_forward(self) -> bool:
        """Return whether browser history has a following entry."""
        return await self._invoke_method("can_go_forward")

    async def go_forward(self) -> None:
        """Navigate to the next history entry, if any."""
        await self._invoke_method("go_forward")

    async def clear_cache(self) -> None:
        """Clear the browser HTTP, Cache API, and application caches."""
        await self._invoke_method("clear_cache")

    async def clear_cookies(self) -> bool:
        """Clear cookies shared by WebViews in this application."""
        return await self._invoke_method("clear_cookies")

    async def get_current_url(self) -> Optional[str]:
        """Return the URL currently displayed by the WebView."""
        return await self._invoke_method("get_current_url")

    async def run_javascript(self, script: str) -> None:
        """Evaluate JavaScript in the active document without returning a value."""
        await self._invoke_method("run_javascript", {"script": script})

    async def run_javascript_returning_result(self, script: str) -> Any:
        """Evaluate JavaScript and return a platform-serializable result."""
        return await self._invoke_method(
            "run_javascript_returning_result", {"script": script}
        )

    async def scroll_to(self, x: int, y: int) -> None:
        """Scroll to an absolute document position."""
        await self._invoke_method("scroll_to", {"x": x, "y": y})

    async def scroll_by(self, delta_x: int, delta_y: int) -> None:
        """Scroll by a relative document offset."""
        await self._invoke_method("scroll_by", {"x": delta_x, "y": delta_y})

    async def get_scroll_position(self) -> dict[str, int]:
        """Return the current horizontal and vertical scroll offsets."""
        return await self._invoke_method("get_scroll_position")

    async def supports_set_scrollbars_enabled(self) -> bool:
        """Return whether the current engine supports scrollbar visibility."""
        return await self._invoke_method("supports_set_scrollbars_enabled")

    async def set_vertical_scrollbar_enabled(self, enabled: bool) -> None:
        """Show or hide the vertical scrollbar when supported."""
        await self._invoke_method("set_vertical_scrollbar_enabled", {"enabled": enabled})

    async def set_horizontal_scrollbar_enabled(self, enabled: bool) -> None:
        """Show or hide the horizontal scrollbar when supported."""
        await self._invoke_method("set_horizontal_scrollbar_enabled", {"enabled": enabled})

    async def open_devtools(self) -> None:
        """Open native WebView developer tools (Windows/WebView2 only)."""
        await self._invoke_method("open_devtools")

    async def get_webview_version(self) -> Optional[str]:
        """Return the Windows WebView2 runtime version, when available."""
        return await self._invoke_method("get_webview_version")