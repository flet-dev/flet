from typing import Any, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.tooltip import TooltipValue
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    OptionalControlEventCallable,
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
        javascript_enabled: bool = True,
        prevent_link: str = "none",
        bgcolor: Optional[str] = None,
        on_page_started: OptionalControlEventCallable = None,
        on_page_ended: OptionalControlEventCallable = None,
        on_web_resource_error: OptionalControlEventCallable = None,
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
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: TooltipValue = None,
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
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.url = url
        self.javascript_enabled = javascript_enabled
        self.prevent_link = prevent_link
        self.bgcolor = bgcolor
        self.on_page_started = on_page_started
        self.on_page_ended = on_page_ended
        self.on_web_resource_error = on_web_resource_error

    def _get_control_name(self):
        return "webview"

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value: Optional[str]):
        self._set_attr("bgcolor", value)

    # url
    @property
    def url(self) -> str:
        return self._get_attr("url")

    @url.setter
    def url(self, value: str):
        self._set_attr("url", value)

    # javascript_enabled
    @property
    def javascript_enabled(self) -> bool:
        return self._get_attr("javascriptEnabled")

    @javascript_enabled.setter
    def javascript_enabled(self, value: bool):
        self._set_attr("javascriptEnabled", value)

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
