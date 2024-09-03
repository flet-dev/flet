import json
import warnings
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Union, cast

from flet_core.box import BoxDecoration
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.control_event import ControlEvent
from flet_core.event_handler import EventHandler
from flet_core.ref import Ref
from flet_core.text import TextSelection
from flet_core.text_style import TextStyle
from flet_core.tooltip import TooltipValue
from flet_core.types import (
    AnimationValue,
    MainAxisAlignment,
    OffsetValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    TextAlign,
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


class MarkdownSelectionChangeCause(Enum):
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
        self.cause = MarkdownSelectionChangeCause(d.get("cause"))
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


@dataclass
class MarkdownStyleSheet:
    a_text_style: Optional[TextStyle] = None
    p_text_style: Optional[TextStyle] = None
    p_padding: PaddingValue = None
    code_text_style: Optional[TextStyle] = None
    h1_text_style: Optional[TextStyle] = None
    h1_padding: PaddingValue = None
    h2_text_style: Optional[TextStyle] = None
    h2_padding: PaddingValue = None
    h3_text_style: Optional[TextStyle] = None
    h3_padding: PaddingValue = None
    h4_text_style: Optional[TextStyle] = None
    h4_padding: PaddingValue = None
    h5_text_style: Optional[TextStyle] = None
    h5_padding: PaddingValue = None
    h6_text_style: Optional[TextStyle] = None
    h6_padding: PaddingValue = None
    em_text_style: Optional[TextStyle] = None
    strong_text_style: Optional[TextStyle] = None
    del_text_style: Optional[TextStyle] = None
    blockquote_text_style: Optional[TextStyle] = None
    img_text_style: Optional[TextStyle] = None
    checkbox_text_style: Optional[TextStyle] = None
    block_spacing: OptionalNumber = None
    list_indent: OptionalNumber = None
    list_bullet_text_style: Optional[TextStyle] = None
    list_bullet_padding: PaddingValue = None
    table_head_text_style: Optional[TextStyle] = None
    table_body_text_style: Optional[TextStyle] = None
    table_head_text_align: Optional[TextAlign] = None
    table_padding: PaddingValue = None
    table_cells_padding: PaddingValue = None
    blockquote_padding: PaddingValue = None
    table_cells_decoration: Optional[BoxDecoration] = None
    blockquote_decoration: Optional[BoxDecoration] = None
    codeblock_padding: PaddingValue = None
    codeblock_decoration: Optional[BoxDecoration] = None
    horizontal_rule_decoration: Optional[BoxDecoration] = None
    blockquote_alignment: Optional[MainAxisAlignment] = None
    codeblock_alignment: Optional[MainAxisAlignment] = None
    h1_alignment: Optional[MainAxisAlignment] = None
    h2_alignment: Optional[MainAxisAlignment] = None
    h3_alignment: Optional[MainAxisAlignment] = None
    h4_alignment: Optional[MainAxisAlignment] = None
    h5_alignment: Optional[MainAxisAlignment] = None
    h6_alignment: Optional[MainAxisAlignment] = None
    text_alignment: Optional[MainAxisAlignment] = None
    ordered_list_alignment: Optional[MainAxisAlignment] = None
    unordered_list_alignment: Optional[MainAxisAlignment] = None


class MarkdownCodeTheme(Enum):
    A11Y_DARK = "a11y-dark"
    A11Y_LIGHT = "a11y-light"
    AGATE = "agate"
    AN_OLD_HOPE = "an-old-hope"
    ANDROID_STUDIO = "androidstudio"
    ARDUINO_LIGHT = "arduino-light"
    ARTA = "arta"
    ASCETIC = "ascetic"
    ATELIER_CAVE_DARK = "atelier-cave-dark"
    ATELIER_CAVE_LIGHT = "atelier-cave-light"
    ATELIER_DUNE_DARK = "atelier-dune-dark"
    ATELIER_DUNE_LIGHT = "atelier-dune-light"
    ATELIER_ESTUARY_DARK = "atelier-estuary-dark"
    ATELIER_ESTUARY_LIGHT = "atelier-estuary-light"
    ATELIER_FOREST_DARK = "atelier-forest-dark"
    ATELIER_FOREST_LIGHT = "atelier-forest-light"
    ATELIER_HEATH_DARK = "atelier-heath-dark"
    ATELIER_HEATH_LIGHT = "atelier-heath-light"
    ATELIER_LAKESIDE_DARK = "atelier-lakeside-dark"
    ATELIER_LAKESIDE_LIGHT = "atelier-lakeside-light"
    ATELIER_PLATEAU_DARK = "atelier-plateau-dark"
    ATELIER_PLATEAU_LIGHT = "atelier-plateau-light"
    ATELIER_SAVANNA_DARK = "atelier-savanna-dark"
    ATELIER_SAVANNA_LIGHT = "atelier-savanna-light"
    ATELIER_SEASIDE_DARK = "atelier-seaside-dark"
    ATELIER_SEASIDE_LIGHT = "atelier-seaside-light"
    ATELIER_SULPHURPOOL_DARK = "atelier-sulphurpool-dark"
    ATELIER_SULPHURPOOL_LIGHT = "atelier-sulphurpool-light"
    ATOM_ONE_DARK_REASONABLE = "atom-one-dark-reasonable"
    ATOM_ONE_DARK = "atom-one-dark"
    ATOM_ONE_LIGHT = "atom-one-light"
    BROWN_PAPER = "brown-paper"
    CODEPEN_EMBED = "codepen-embed"
    COLOR_BREWER = "color-brewer"
    DARCULA = "darcula"
    DARK = "dark"
    DEFAULT = "default"
    DOCCO = "docco"
    DRAGULA = "dracula"
    FAR = "far"
    FOUNDATION = "foundation"
    GITHUB_GIST = "github-gist"
    GITHUB = "github"
    GML = "gml"
    GOOGLE_CODE = "googlecode"
    GRADIENT_DARK = "gradient-dark"
    GRAYSCALE = "grayscale"
    GRUVBOX_DARK = "gruvbox-dark"
    GRUVBOX_LIGHT = "gruvbox-light"
    HOPSCOTCH = "hopscotch"
    HYBRID = "hybrid"
    IDEA = "idea"
    IR_BLACK = "ir-black"
    ISBL_EDITOR_DARK = "isbl-editor-dark"
    ISBL_EDITOR_LIGHT = "isbl-editor-light"
    KIMBIE_DARK = "kimbie.dark"
    KIMBIE_LIGHT = "kimbie.light"
    LIGHTFAIR = "lightfair"
    MAGULA = "magula"
    MONO_BLUE = "mono-blue"
    MONOKAI_SUBLIME = "monokai-sublime"
    MONOKAI = "monokai"
    NIGHT_OWL = "night-owl"
    NORD = "nord"
    OBSIDIAN = "obsidian"
    OCEAN = "ocean"
    PARAISEO_DARK = "paraiso-dark"
    PARAISEO_LIGHT = "paraiso-light"
    POJOAQUE = "pojoaque"
    PURE_BASIC = "purebasic"
    QT_CREATOR_DARK = "qtcreator_dark"
    QT_CREATOR_LIGHT = "qtcreator_light"
    RAILSCASTS = "railscasts"
    RAINBOW = "rainbow"
    ROUTEROS = "routeros"
    SCHOOL_BOOK = "school-book"
    SHADES_OF_PURPLE = "shades-of-purple"
    SOLARIZED_DARK = "solarized-dark"
    SOLARIZED_LIGHT = "solarized-light"
    SUNBURST = "sunburst"
    TOMORROW_NIGHT_BLUE = "tomorrow-night-blue"
    TOMORROW_NIGHT_BRIGHT = "tomorrow-night-bright"
    TOMORROW_NIGHT_EIGHTIES = "tomorrow-night-eighties"
    TOMORROW_NIGHT = "tomorrow-night"
    TOMORROW = "tomorrow"
    VS = "vs"
    VS2015 = "vs2015"
    XCODE = "xcode"
    XT256 = "xt256"
    ZENBURN = "zenburn"


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
        code_theme: Optional[MarkdownCodeTheme] = None,
        code_style: Optional[TextStyle] = None,
        auto_follow_links: Optional[bool] = None,
        shrink_wrap: Optional[bool] = None,
        fit_content: Optional[bool] = None,
        soft_line_break: Optional[bool] = None,
        auto_follow_links_target: Optional[str] = None,
        img_error_content: Optional[Control] = None,
        code_style_sheet: Optional[MarkdownStyleSheet] = None,
        md_style_sheet: Optional[MarkdownStyleSheet] = None,
        on_tap_text: OptionalControlEventCallable = None,
        on_selection_change: OptionalControlEventCallable = None,
        on_tap_link: OptionalControlEventCallable = None,
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
        self.code_style_sheet = code_style_sheet
        self.md_style_sheet = md_style_sheet

    def _get_control_name(self):
        return "markdown"

    def before_update(self):
        super().before_update()
        self._set_attr_json("codeStyle", self.__code_style)
        self._set_attr_json("codeStyleSheet", self.__code_style_sheet)
        self._set_attr_json("mdStyleSheet", self.__md_style_sheet)

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

    # code_style_sheet
    @property
    def code_style_sheet(self) -> Optional[MarkdownStyleSheet]:
        return self.__code_style_sheet

    @code_style_sheet.setter
    def code_style_sheet(self, value: Optional[MarkdownStyleSheet]):
        self.__code_style_sheet = value

    # md_style_sheet
    @property
    def md_style_sheet(self) -> Optional[MarkdownStyleSheet]:
        return self.__md_style_sheet

    @md_style_sheet.setter
    def md_style_sheet(self, value: Optional[MarkdownStyleSheet]):
        self.__md_style_sheet = value

    # code_theme
    @property
    def code_theme(self) -> Optional[MarkdownCodeTheme]:
        return self.__code_theme

    @code_theme.setter
    def code_theme(self, value: Optional[MarkdownCodeTheme]):
        self.__code_theme = value
        self._set_enum_attr("codeTheme", value, MarkdownCodeTheme)

    # code_style
    @property
    def code_style(self) -> Optional[TextStyle]:
        warnings.warn(
            f"code_style is deprecated since version 0.24.0 "
            f"and will be removed in version 0.27.0. Use code_style_sheet.code_text_style instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self.__code_style

    @code_style.setter
    def code_style(self, value: Optional[TextStyle]):
        self.__code_style = value
        if value is not None:
            warnings.warn(
                f"code_style is deprecated since version 0.24.0 "
                f"and will be removed in version 0.27.0. Use code_style_sheet.code_text_style instead.",
                category=DeprecationWarning,
                stacklevel=2,
            )

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
    def on_selection_change(
        self,
    ) -> OptionalEventCallable[MarkdownSelectionChangeEvent]:
        return self.__on_selection_change.handler

    @on_selection_change.setter
    def on_selection_change(
        self, handler: OptionalEventCallable[MarkdownSelectionChangeEvent]
    ):
        self.__on_selection_change.handler = handler
