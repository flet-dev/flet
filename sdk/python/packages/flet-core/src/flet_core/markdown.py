import json
from enum import Enum
from typing import Any, Optional, Union, cast

from flet_core import ControlEvent
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber, Control
from flet_core.event_handler import EventHandler
from flet_core.ref import Ref
from flet_core.text import TextSelection
from flet_core.text_style import TextStyle
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    OptionalEventCallable,
    OptionalControlEventCallable,
)

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class MarkdownExtensionSet(Enum):
    NONE = "none"
    COMMON_MARK = "commonMark"
    GITHUB_WEB = "gitHubWeb"
    GITHUB_FLAVORED = "gitHubFlavored"


class MarkdownSelectionChangedCause(Enum):
    UNKNOWN = "unknown"
    TAP = "tap"
    DOUBLE_TAP = "doubleTap"
    LONG_PRESS = "longPress"
    FORCE_PRESS = "forcePress"
    KEYBOARD = "keyboard"
    TOOLBAR = "toolbar"
    DRAG = "drag"
    SCRIBBLE = "scribble"


class MarkdownSelectionChangeEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.text: str = d.get("text")
        self.cause = MarkdownSelectionChangedCause(d.get("cause"))
        start = d.get("start")
        end = d.get("end")
        self.selection = TextSelection(
            start=start,
            end=end,
            selection=self.text[start:end] if start != -1 and end != -1 else "",
            base_offset=d.get("base_offset"),
            extent_offset=d.get("extent_offset"),
            affinity=d.get("affinity"),
            directional=d.get("directional"),
            collapsed=d.get("collapsed"),
            valid=d.get("valid"),
            normalized=d.get("normalized"),
        )


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
        shrink_wrap: Optional[bool] = None,
        fit_content: Optional[bool] = None,
        soft_line_break: Optional[bool] = None,
        auto_follow_links_target: Optional[str] = None,
        img_error_content: Optional[Control] = None,
        on_tap_text: OptionalEventCallable = None,
        on_selection_change: OptionalEventCallable = None,
        on_tap_link: OptionalEventCallable = None,
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
        on_animation_end: OptionalEventCallable = None,
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

        self.__on_selection_change = EventHandler(
            lambda e: MarkdownSelectionChangeEvent(e)
        )

        self._add_event_handler(
            "selection_change", self.__on_selection_change.get_handler()
        )

        self.value = value
        self.selectable = selectable
        self.extension_set = extension_set
        self.code_theme = code_theme
        self.code_style = code_style
        self.auto_follow_links = auto_follow_links
        self.auto_follow_links_target = auto_follow_links_target
        self.on_tap_link = on_tap_link
        self.shrink_wrap = shrink_wrap
        self.fit_content = fit_content
        self.soft_line_break = soft_line_break
        self.on_tap_text = on_tap_text
        self.on_selection_change = on_selection_change
        self.img_error_content = img_error_content

    def _get_control_name(self):
        return "markdown"

    def before_update(self):
        super().before_update()
        self._set_attr_json("codeStyle", self.__code_style)

    def _get_children(self):
        if self.__img_error_content is not None:
            self.__img_error_content._set_attr_internal("n", "error")
            return [self.__img_error_content]
        return []

    # value
    @property
    def value(self) -> Optional[str]:
        return self._get_attr("value")

    @value.setter
    def value(self, value: Optional[str]):
        self._set_attr("value", value)

    # selectable
    @property
    def selectable(self) -> bool:
        return self._get_attr("selectable", data_type="bool", def_value=False)

    @selectable.setter
    def selectable(self, value: Optional[bool]):
        self._set_attr("selectable", value)

    # shrink_wrap
    @property
    def shrink_wrap(self) -> bool:
        return self._get_attr("shrinkWrap", data_type="bool", def_value=True)

    @shrink_wrap.setter
    def shrink_wrap(self, value: Optional[bool]):
        self._set_attr("shrinkWrap", value)

    # fit_content
    @property
    def fit_content(self) -> bool:
        return self._get_attr("fitContent", data_type="bool", def_value=True)

    @fit_content.setter
    def fit_content(self, value: Optional[bool]):
        self._set_attr("fitContent", value)

    # soft_line_break
    @property
    def soft_line_break(self) -> bool:
        return self._get_attr("softLineBreak", data_type="bool", def_value=False)

    @soft_line_break.setter
    def soft_line_break(self, value: Optional[bool]):
        self._set_attr("softLineBreak", value)

    # extension_set
    @property
    def extension_set(self) -> Optional[MarkdownExtensionSet]:
        return self.__extension_set

    @extension_set.setter
    def extension_set(self, value: Optional[MarkdownExtensionSet]):
        self.__extension_set = value
        self._set_enum_attr("extensionSet", value, MarkdownExtensionSet)

    # code_theme
    @property
    def code_theme(self) -> Optional[str]:
        return self._get_attr("codeTheme")

    @code_theme.setter
    def code_theme(self, value: Optional[str]):
        self._set_attr("codeTheme", value)

    # code_style
    @property
    def code_style(self) -> Optional[TextStyle]:
        return self.__code_style

    @code_style.setter
    def code_style(self, value: Optional[TextStyle]):
        self.__code_style = value

    # auto_follow_links
    @property
    def auto_follow_links(self) -> bool:
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

    # img_error_content
    @property
    def img_error_content(self) -> Optional[Control]:
        return self.__img_error_content

    @img_error_content.setter
    def img_error_content(self, value: Optional[Control]):
        self.__img_error_content = value

    # on_tap_link
    @property
    def on_tap_link(self) -> OptionalControlEventCallable:
        return self._get_event_handler("tap_link")

    @on_tap_link.setter
    def on_tap_link(self, handler: OptionalControlEventCallable):
        self._add_event_handler("tap_link", handler)

    # on_tap_text
    @property
    def on_tap_text(self) -> OptionalControlEventCallable:
        return self._get_event_handler("tap_text")

    @on_tap_text.setter
    def on_tap_text(self, handler: OptionalControlEventCallable):
        self._add_event_handler("tap_text", handler)

    # on_selection_change
    @property
    def on_selection_change(self) -> OptionalControlEventCallable:
        return self._get_event_handler("selection_change")

    @on_selection_change.setter
    def on_selection_change(self, handler: OptionalControlEventCallable):
        self._add_event_handler("selection_change", handler)

    # on_selection_change
    @property
    def on_selection_change(self):
        return self._get_event_handler("selection_change")

    @on_selection_change.setter
    def on_selection_change(
        self, handler: OptionalEventCallable[MarkdownSelectionChangeEvent]
    ):
        self.__on_selection_change.subscribe(handler)
