from enum import Enum
from typing import Any, Optional, Union, cast

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

MarkdownExtensionSetString = Literal[
    None, "none", "commonMark", "gitHubWeb", "gitHubFlavored"
]


class MarkdownExtensionSet(Enum):
    NONE = "none"
    COMMON_MARK = "commonMark"
    GITHUB_WEB = "gitHubWeb"
    GITHUB_FLAVORED = "gitHubFlavored"


class Markdown(ConstrainedControl):
    """
    Control for rendering text in markdown format.

    -----

    Online docs: https://flet.dev/docs/controls/markdown
    """

    def __init__(
        self,
        value: Optional[str] = None,
        selectable: Optional[bool] = None,
        extension_set: Optional[MarkdownExtensionSet] = None,
        code_theme: Optional[str] = None,
        code_style: Optional[TextStyle] = None,
        auto_follow_links: Optional[bool] = None,
        auto_follow_links_target: Optional[str] = None,
        on_tap_link=None,
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
        on_animation_end=None,
        tooltip: Optional[str] = None,
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

        self.value = value
        self.selectable = selectable
        self.extension_set = extension_set
        self.code_theme = code_theme
        self.code_style = code_style
        self.auto_follow_links = auto_follow_links
        self.auto_follow_links_target = auto_follow_links_target
        self.on_tap_link = on_tap_link

    def _get_control_name(self):
        return "markdown"

    def before_update(self):
        super().before_update()
        self._set_attr_json("codeStyle", self.__code_style)

    # value
    @property
    def value(self) -> Optional[str]:
        return self._get_attr("value")

    @value.setter
    def value(self, value: Optional[str]):
        self._set_attr("value", value)

    # selectable
    @property
    def selectable(self) -> Optional[bool]:
        return self._get_attr("selectable", data_type="bool", def_value=False)

    @selectable.setter
    def selectable(self, value: Optional[bool]):
        self._set_attr("selectable", value)

    # extension_set
    @property
    def extension_set(self) -> Optional[MarkdownExtensionSet]:
        return self.__extension_set

    @extension_set.setter
    def extension_set(self, value: Optional[MarkdownExtensionSet]):
        self.__extension_set = value
        self._set_attr(
            "extensionSet",
            value.value if isinstance(value, MarkdownExtensionSet) else value,
        )

    # code_theme
    @property
    def code_theme(self):
        return self._get_attr("codeTheme")

    @code_theme.setter
    def code_theme(self, value):
        self._set_attr("codeTheme", value)

    # code_style
    @property
    def code_style(self):
        return self.__code_style

    @code_style.setter
    def code_style(self, value: Optional[TextStyle]):
        self.__code_style = value

    # auto_follow_links
    @property
    def auto_follow_links(self) -> Optional[bool]:
        return cast(
            Optional[bool],
            self._get_attr("autoFollowLinks", data_type="bool", def_value=False),
        )

    @auto_follow_links.setter
    def auto_follow_links(self, value: Optional[bool]):
        self._set_attr("autoFollowLinks", value)

    # auto_follow_links_target
    @property
    def auto_follow_links_target(self) -> Optional[str]:
        return self._get_attr("autoFollowLinksTarget")

    @auto_follow_links_target.setter
    def auto_follow_links_target(self, value: Optional[str]):
        self._set_attr("autoFollowLinksTarget", value)

    # on_tap_link
    @property
    def on_tap_link(self):
        return self._get_event_handler("tap_link")

    @on_tap_link.setter
    def on_tap_link(self, handler):
        self._add_event_handler("tap_link", handler)
