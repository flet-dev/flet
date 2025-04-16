import json
from enum import Enum
from typing import Any, Optional, Union

from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber
from flet.core.control_event import ControlEvent
from flet.core.event_handler import EventHandler
from flet.core.exceptions import FletUnsupportedPlatformException
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    ColorEnums,
    ColorValue,
    OffsetValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
    PagePlatform,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)
from flet.utils import deprecated


class WebviewRequestMethod(Enum):
    GET = "get"
    POST = "post"


class WebviewLogLevelSeverity(Enum):
    ERROR = "error"
    WARNING = "warning"
    DEBUG = "debug"
    INFO = "info"
    LOG = "log"


class WebviewScrollEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.x: float = d.get("x", 0)
        self.y: float = d.get("y", 0)


class WebviewConsoleMessageEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.message: str = d.get("message")
        self.severity_level: WebviewLogLevelSeverity = WebviewLogLevelSeverity(
            d.get("level")
        )


class WebviewJavaScriptEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.message: str = d.get("message")
        self.url: str = d.get("url")


@deprecated(
    reason="WebView control has been moved to a separate Python package: https://pypi.org/project/flet-webview. "
    + "Read more about this change in Flet blog: https://flet.dev/blog/flet-v-0-26-release-announcement",
    version="0.26.0",
    delete_version="0.29.0",
)
class WebView(ConstrainedControl):
    """
    Easily load webpages while allowing user interaction.

    The `WebView` control is designed exclusively for iOS and Android platforms.

    ## Examples
    A simple webview implementation using this class could be like:

    ```python
    import flet

    def main(page: flet.Page):
        wv = flet.WebView(
            "https://flet.dev",
            expand=True,
            on_page_started=lambda _: print("Page started"),
            on_page_ended=lambda _: print("Page ended"),
            on_web_resource_error=lambda e: print("Page error:", e.data),
        )
        page.add(wv)

    flet.app(main)
    ```

    ## Properties

    ### `url`

    Start the webview by loading the `url` value.

    ### `javascript_enabled`

    Enable or disable the javascript execution of the page. Note that disabling the javascript execution of the page may result unexpected webpage behaviour.

    ### `prevent_link`

    Specify a link to prevent it from downloading.

    ### `bgcolor`

    Set the background color of the webview.

    ## Events

    ### `on_page_started`

    Fires soon as the first loading process of the webpage is started.

    ### `on_page_ended`

    Fires when all the webpage loading processes are ended.

    ### `on_web_resource_error`

    Fires when there is error with loading a webpage resource.

    View docs: [WebView](https://flet.dev/docs/controls/webview)
    """

    def __init__(
        self,
        url: str,
        enable_javascript: Optional[bool] = None,
        prevent_link: Optional[str] = None,
        bgcolor: Optional[ColorValue] = None,
        on_page_started: OptionalControlEventCallable = None,
        on_page_ended: OptionalControlEventCallable = None,
        on_web_resource_error: OptionalControlEventCallable = None,
        on_progress: OptionalControlEventCallable = None,
        on_url_change: OptionalControlEventCallable = None,
        on_scroll: OptionalEventCallable[WebviewScrollEvent] = None,
        on_console_message: OptionalEventCallable[WebviewConsoleMessageEvent] = None,
        on_javascript_alert_dialog: OptionalEventCallable[
            WebviewJavaScriptEvent
        ] = None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: Optional[RotateValue] = None,
        scale: Optional[ScaleValue] = None,
        offset: Optional[OffsetValue] = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: Optional[AnimationValue] = None,
        animate_size: Optional[AnimationValue] = None,
        animate_position: Optional[AnimationValue] = None,
        animate_rotation: Optional[AnimationValue] = None,
        animate_scale: Optional[AnimationValue] = None,
        animate_offset: Optional[AnimationValue] = None,
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: Optional[TooltipValue] = None,
        badge: Optional[BadgeValue] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            badge=badge,
            visible=visible,
            disabled=disabled,
            data=data,
        )
        self.__on_scroll = EventHandler(lambda e: WebviewScrollEvent(e))
        self._add_event_handler("scroll", self.__on_scroll.get_handler())
        self.__on_console_message = EventHandler(
            lambda e: WebviewConsoleMessageEvent(e)
        )
        self._add_event_handler(
            "console_message", self.__on_console_message.get_handler()
        )
        self.__on_javascript_alert_dialog = EventHandler(
            lambda e: WebviewJavaScriptEvent(e)
        )
        self._add_event_handler(
            "javascript_alert_dialog", self.__on_javascript_alert_dialog.get_handler()
        )

        self.url = url
        self.enable_javascript = enable_javascript
        self.prevent_link = prevent_link
        self.bgcolor = bgcolor
        self.on_page_started = on_page_started
        self.on_page_ended = on_page_ended
        self.on_web_resource_error = on_web_resource_error
        self.on_progress = on_progress
        self.on_url_change = on_url_change
        self.on_scroll = on_scroll
        self.on_console_message = on_console_message
        self.on_javascript_alert_dialog = on_javascript_alert_dialog

    def _get_control_name(self):
        return "webview"

    def _check_mobile_or_mac_platform(self):
        assert self.page is not None, "WebView must be added to page first."
        if self.page.platform not in [
            PagePlatform.ANDROID,
            PagePlatform.IOS,
            PagePlatform.MACOS,
        ]:
            raise FletUnsupportedPlatformException(
                "This method is supported on Android, iOS and macOS platforms only."
            )

    def reload(self):
        self._check_mobile_or_mac_platform()
        self.invoke_method("reload")

    def can_go_back(self, wait_timeout: OptionalNumber = 10) -> bool:
        self._check_mobile_or_mac_platform()
        return (
            self.invoke_method(
                "can_go_back",
                wait_for_result=True,
                wait_timeout=wait_timeout,
            )
            == "true"
        )

    def can_go_forward(self, wait_timeout: OptionalNumber = 10) -> bool:
        self._check_mobile_or_mac_platform()
        return (
            self.invoke_method(
                "can_go_forward",
                wait_for_result=True,
                wait_timeout=wait_timeout,
            )
            == "true"
        )

    def go_back(self):
        self._check_mobile_or_mac_platform()
        self.invoke_method("go_back")

    def go_forward(self):
        self._check_mobile_or_mac_platform()
        self.invoke_method("go_forward")

    def enable_zoom(self):
        self._check_mobile_or_mac_platform()
        self.invoke_method("enable_zoom")

    def disable_zoom(self):
        self._check_mobile_or_mac_platform()
        self.invoke_method("disable_zoom")

    def clear_cache(self):
        self._check_mobile_or_mac_platform()
        self.invoke_method("clear_cache")

    def clear_local_storage(self):
        self._check_mobile_or_mac_platform()
        self.invoke_method("clear_local_storage")

    def get_current_url(self, wait_timeout: OptionalNumber = 10) -> Optional[str]:
        self._check_mobile_or_mac_platform()
        return self.invoke_method(
            "get_current_url", wait_for_result=True, wait_timeout=wait_timeout
        )

    def get_title(self, wait_timeout: OptionalNumber = 10) -> Optional[str]:
        self._check_mobile_or_mac_platform()
        return self.invoke_method(
            "get_title", wait_for_result=True, wait_timeout=wait_timeout
        )

    def get_user_agent(self, wait_timeout: OptionalNumber = 10) -> Optional[str]:
        self._check_mobile_or_mac_platform()
        return self.invoke_method(
            "get_user_agent", wait_for_result=True, wait_timeout=wait_timeout
        )

    def load_file(self, absolute_path: str):
        self._check_mobile_or_mac_platform()
        self.invoke_method("load_file", arguments={"path": absolute_path})

    def load_request(
        self, url: str, method: WebviewRequestMethod = WebviewRequestMethod.GET
    ):
        self._check_mobile_or_mac_platform()
        self.invoke_method(
            "load_request",
            arguments={"url": url, "method": method.value},
        )

    def run_javascript(self, value: str):
        self._check_mobile_or_mac_platform()
        self.invoke_method("run_javascript", arguments={"value": value})

    def load_html(self, value: str, base_url: Optional[str] = None):
        self._check_mobile_or_mac_platform()
        self.invoke_method(
            "load_html", arguments={"value": value, "base_url": base_url}
        )

    def scroll_to(self, x: int, y: int):
        self._check_mobile_or_mac_platform()
        self.invoke_method("scroll_to", arguments={"x": str(x), "y": str(y)})

    def scroll_by(self, x: int, y: int):
        self._check_mobile_or_mac_platform()
        self.invoke_method("scroll_by", arguments={"x": str(x), "y": str(y)})

    # bgcolor
    @property
    def bgcolor(self) -> Optional[ColorValue]:
        return self.__bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Optional[ColorValue]):
        self.__bgcolor = value
        self._set_enum_attr("bgcolor", value, ColorEnums)

    # url
    @property
    def url(self) -> str:
        return self._get_attr("url")

    @url.setter
    def url(self, value: str):
        self._set_attr("url", value)
        if self.page:
            self.load_request(value, WebviewRequestMethod.GET)

    # enable_javascript
    @property
    def enable_javascript(self) -> bool:
        return self._get_attr("enableJavascript", data_type="bool", def_value=False)

    @enable_javascript.setter
    def enable_javascript(self, value: Optional[bool]):
        self._set_attr("enableJavascript", value)
        if self.page and value is not None:
            self.invoke_method(
                "set_javascript_mode",
                arguments={"value": str(value)},
            )

    # prevent_link
    @property
    def prevent_link(self) -> str:
        return self._get_attr("prevent_link")

    @prevent_link.setter
    def prevent_link(self, value: str):
        self._set_attr("prevent_link", value)

    # on_page_started
    @property
    def on_page_started(self) -> OptionalControlEventCallable:
        return self._get_event_handler("page_started")

    @on_page_started.setter
    def on_page_started(self, handler: OptionalControlEventCallable):
        self._add_event_handler("page_started", handler)

    # on_page_ended
    @property
    def on_page_ended(self) -> OptionalControlEventCallable:
        return self._get_event_handler("page_ended")

    @on_page_ended.setter
    def on_page_ended(self, handler: OptionalControlEventCallable):
        self._add_event_handler("page_ended", handler)

    # on_web_resource_error
    @property
    def on_web_resource_error(self) -> OptionalControlEventCallable:
        return self._get_event_handler("web_resource_error")

    @on_web_resource_error.setter
    def on_web_resource_error(self, handler: OptionalControlEventCallable):
        self._add_event_handler("web_resource_error", handler)

    # on_progress
    @property
    def on_progress(self) -> OptionalControlEventCallable:
        return self._get_event_handler("progress")

    @on_progress.setter
    def on_progress(self, handler: OptionalControlEventCallable):
        self._add_event_handler("progress", handler)

    # on_url_change
    @property
    def on_url_change(self) -> OptionalControlEventCallable:
        return self._get_event_handler("url_change")

    @on_url_change.setter
    def on_url_change(self, handler: OptionalControlEventCallable):
        self._add_event_handler("url_change", handler)

    # on_scroll
    @property
    def on_scroll(self) -> OptionalEventCallable[WebviewScrollEvent]:
        return self.__on_scroll.handler

    @on_scroll.setter
    def on_scroll(self, handler: OptionalEventCallable[WebviewScrollEvent]):
        self.__on_scroll.handler = handler

    # on_console_message
    @property
    def on_console_message(self) -> OptionalEventCallable[WebviewConsoleMessageEvent]:
        return self.__on_console_message.handler

    @on_console_message.setter
    def on_console_message(
        self, handler: OptionalEventCallable[WebviewConsoleMessageEvent]
    ):
        self.__on_console_message.handler = handler

    # on_javascript_alert_dialog
    @property
    def on_javascript_alert_dialog(
        self,
    ) -> OptionalEventCallable[WebviewJavaScriptEvent]:
        return self.__on_javascript_alert_dialog.handler

    @on_javascript_alert_dialog.setter
    def on_javascript_alert_dialog(
        self, handler: OptionalEventCallable[WebviewJavaScriptEvent]
    ):
        self.__on_javascript_alert_dialog.handler = handler
