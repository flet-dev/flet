from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Union, cast

from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.box import BoxDecoration
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, OptionalNumber
from flet.core.event_handler import EventHandler
from flet.core.ref import Ref
from flet.core.text import TextSelectionChangeEvent
from flet.core.text_style import TextStyle
from flet.core.tooltip import TooltipValue
from flet.core.types import (
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


@dataclass
class MarkdownStyleSheet:
    a_text_style: Optional[TextStyle] = None
    p_text_style: Optional[TextStyle] = None
    p_padding: Optional[PaddingValue] = None
    code_text_style: Optional[TextStyle] = None
    h1_text_style: Optional[TextStyle] = None
    h1_padding: Optional[PaddingValue] = None
    h2_text_style: Optional[TextStyle] = None
    h2_padding: Optional[PaddingValue] = None
    h3_text_style: Optional[TextStyle] = None
    h3_padding: Optional[PaddingValue] = None
    h4_text_style: Optional[TextStyle] = None
    h4_padding: Optional[PaddingValue] = None
    h5_text_style: Optional[TextStyle] = None
    h5_padding: Optional[PaddingValue] = None
    h6_text_style: Optional[TextStyle] = None
    h6_padding: Optional[PaddingValue] = None
    em_text_style: Optional[TextStyle] = None
    strong_text_style: Optional[TextStyle] = None
    del_text_style: Optional[TextStyle] = None
    blockquote_text_style: Optional[TextStyle] = None
    img_text_style: Optional[TextStyle] = None
    checkbox_text_style: Optional[TextStyle] = None
    block_spacing: OptionalNumber = None
    list_indent: OptionalNumber = None
    list_bullet_text_style: Optional[TextStyle] = None
    list_bullet_padding: Optional[PaddingValue] = None
    table_head_text_style: Optional[TextStyle] = None
    table_body_text_style: Optional[TextStyle] = None
    table_head_text_align: Optional[TextAlign] = None
    table_padding: Optional[PaddingValue] = None
    table_cells_padding: Optional[PaddingValue] = None
    blockquote_padding: Optional[PaddingValue] = None
    table_cells_decoration: Optional[BoxDecoration] = None
    blockquote_decoration: Optional[BoxDecoration] = None
    codeblock_padding: Optional[PaddingValue] = None
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


@dataclass
class MarkdownCustomCodeTheme:
    addition: Optional[TextStyle] = None
    attr: Optional[TextStyle] = None
    attribute: Optional[TextStyle] = None
    built_in: Optional[TextStyle] = None
    builtin_name: Optional[TextStyle] = None
    bullet: Optional[TextStyle] = None
    class_name: Optional[TextStyle] = None
    code: Optional[TextStyle] = None
    comment: Optional[TextStyle] = None
    deletion: Optional[TextStyle] = None
    doctag: Optional[TextStyle] = None
    emphasis: Optional[TextStyle] = None
    formula: Optional[TextStyle] = None
    function: Optional[TextStyle] = None
    keyword: Optional[TextStyle] = None
    link: Optional[TextStyle] = None
    link_label: Optional[TextStyle] = None
    literal: Optional[TextStyle] = None
    meta: Optional[TextStyle] = None
    meta_keyword: Optional[TextStyle] = None
    meta_string: Optional[TextStyle] = None
    name: Optional[TextStyle] = None
    number: Optional[TextStyle] = None
    operator: Optional[TextStyle] = None
    params: Optional[TextStyle] = None
    pattern_match: Optional[TextStyle] = None
    quote: Optional[TextStyle] = None
    regexp: Optional[TextStyle] = None
    root: Optional[TextStyle] = None
    section: Optional[TextStyle] = None
    selector_attr: Optional[TextStyle] = None
    selector_class: Optional[TextStyle] = None
    selector_id: Optional[TextStyle] = None
    selector_pseudo: Optional[TextStyle] = None
    selector_tag: Optional[TextStyle] = None
    string: Optional[TextStyle] = None
    strong: Optional[TextStyle] = None
    stronge: Optional[TextStyle] = None
    subst: Optional[TextStyle] = None
    subtr: Optional[TextStyle] = None
    symbol: Optional[TextStyle] = None
    tag: Optional[TextStyle] = None
    template_tag: Optional[TextStyle] = None
    template_variable: Optional[TextStyle] = None
    title: Optional[TextStyle] = None
    type: Optional[TextStyle] = None
    variable: Optional[TextStyle] = None


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
        code_theme: Optional[Union[MarkdownCodeTheme, MarkdownCustomCodeTheme]] = None,
        auto_follow_links: Optional[bool] = None,
        shrink_wrap: Optional[bool] = None,
        fit_content: Optional[bool] = None,
        soft_line_break: Optional[bool] = None,
        auto_follow_links_target: Optional[str] = None,
        img_error_content: Optional[Control] = None,
        code_style_sheet: Optional[MarkdownStyleSheet] = None,
        md_style_sheet: Optional[MarkdownStyleSheet] = None,
        on_tap_text: OptionalControlEventCallable = None,
        on_selection_change: OptionalEventCallable[TextSelectionChangeEvent] = None,
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

        self.__on_selection_change = EventHandler(lambda e: TextSelectionChangeEvent(e))

        self._add_event_handler(
            "selection_change", self.__on_selection_change.get_handler()
        )

        self.value = value
        self.selectable = selectable
        self.extension_set = extension_set
        self.code_theme = code_theme
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
        self._set_attr_json("codeStyleSheet", self.__code_style_sheet)
        self._set_attr_json("mdStyleSheet", self.__md_style_sheet)
        self._set_attr_json(
            "codeTheme",
            self.__code_theme.value
            if isinstance(self.__code_theme, MarkdownCodeTheme)
            else self.__code_theme,
        )

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
    def code_theme(self) -> Optional[Union[MarkdownCodeTheme, MarkdownCustomCodeTheme]]:
        return self.__code_theme

    @code_theme.setter
    def code_theme(
        self, value: Optional[Union[MarkdownCodeTheme, MarkdownCustomCodeTheme]]
    ):
        self.__code_theme = value

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
    ) -> OptionalEventCallable[TextSelectionChangeEvent]:
        return self.__on_selection_change.handler

    @on_selection_change.setter
    def on_selection_change(
        self,
        handler: OptionalEventCallable[TextSelectionChangeEvent],
    ):
        self.__on_selection_change.handler = handler
