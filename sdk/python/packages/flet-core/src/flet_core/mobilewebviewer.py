from enum import Enum
from typing import Any, List, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.text_span import TextSpan
from flet_core.types import (
    AnimationValue,
    FontWeight,
    FontWeightString,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    TextAlign,
    TextAlignString,
)

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

TextOverflowString = Literal[None, "clip", "ellipsis", "fade", "visible"]


class TextOverflow(Enum):
    NONE = None
    CLIP = "clip"
    ELLIPSIS = "ellipsis"
    FADE = "fade"
    VISIBLE = "visible"


TextThemeStyleString = Literal[
    "displayLarge",
    "displayMedium",
    "displaySmall",
    "headlineLarge",
    "headlineMedium",
    "headlineSmall",
    "titleLarge",
    "titleMedium",
    "titleSmall",
    "labelLarge",
    "labelMedium",
    "labelSmall",
    "bodyLarge",
    "bodyMedium",
    "bodySmall",
]


class TextThemeStyle(Enum):
    DISPLAY_LARGE = "displayLarge"
    DISPLAY_MEDIUM = "displayMedium"
    DISPLAY_SMALL = "displaySmall"
    HEADLINE_LARGE = "headlineLarge"
    HEADLINE_MEDIUM = "headlineMedium"
    HEADLINE_SMALL = "headlineSmall"
    TITLE_LARGE = "titleLarge"
    TITLE_MEDIUM = "titleMedium"
    TITLE_SMALL = "titleSmall"
    LABEL_LARGE = "labelLarge"
    LABEL_MEDIUM = "labelMedium"
    LABEL_SMALL = "labelSmall"
    BODY_LARGE = "bodyLarge"
    BODY_MEDIUM = "bodyMedium"
    BODY_SMALL = "bodySmall"


class MobileWebViewer(ConstrainedControl):
    """
    To be documented
    """

    def __init__(
        self,
        #
        # mobilewebviewer-specific
        #
        url: str,
        width: OptionalNumber,
        height: OptionalNumber,
        javascript_enabled: bool = True,
        prevent_link: str = "none",
        bgcolor: Optional[str] = None,

        #--THE REST--
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
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
        on_animation_end=None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        semantics_label: Optional[str] = None,
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

        self.url : str = url
        self.javascript_enabled: bool = javascript_enabled
        self.prevent_link: str = prevent_link
        self.bgcolor = bgcolor

        # events
        self.on_page_started = None
        self.on_page_ended = None
        self.on_web_resource_error = None

    def _get_control_name(self):
        return "mobilewebviewer"

    def _get_children(self):
        children = []
        print("Childrins are gettn")
        return children

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgcolor", value)

    # url
    @property
    def url (self):
        return self._get_attr("url")
    
    @url.setter
    def url (self, value):
        self._set_attr("url", value)
    

    # javascript_enabled
    @property
    def javascript_enabled(self):
        return self._get_attr("javascriptEnabled")
    
    @javascript_enabled.setter
    def javascript_enabled(self, value):
        self._set_attr("javascriptEnabled", value)
    

    # prevent_link
    @property
    def prevent_link (self):
        return self._get_attr("prevent_link")
    
    @prevent_link.setter
    def prevent_link(self, value):
        self._set_attr("prevent_link", value)
    

    ## EVENTS
    # on_page_started
    @property
    def on_page_started(self):
        return self._get_event_handler("page_started")
    
    @on_page_started.setter
    def on_page_started(self, handler):
        self._add_event_handler("page_started", handler)
    

    # on_page_ended
    @property
    def on_page_ended(self):
        return self._get_event_handler("page_ended")
    
    @on_page_ended.setter
    def on_page_ended(self, handler):
        self._add_event_handler("page_ended", handler)
    
    # on_web_resource_error
    @property
    def on_web_resource_error(self):
        return self._get_event_handler("web_resource_error")
    
    @on_web_resource_error.setter
    def on_web_resource_error(self, handler):
        self._add_event_handler("web_resource_error", handler)