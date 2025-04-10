from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from flet.controls.box import BoxDecoration
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, control
from flet.controls.core.text import TextSelectionChangeEvent
from flet.controls.padding import OptionalPaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    MainAxisAlignment,
    OptionalControlEventCallable,
    OptionalEventCallable,
    OptionalNumber,
    TextAlign,
    UrlTarget,
)

__all__ = [
    "Markdown",
    "MarkdownExtensionSet",
    "MarkdownStyleSheet",
    "MarkdownCodeTheme",
    "MarkdownCustomCodeTheme",
]


class MarkdownExtensionSet(Enum):
    NONE = "none"
    COMMON_MARK = "commonMark"
    GITHUB_WEB = "gitHubWeb"
    GITHUB_FLAVORED = "gitHubFlavored"


@dataclass
class MarkdownStyleSheet:
    a_text_style: Optional[TextStyle] = None
    p_text_style: Optional[TextStyle] = None
    p_padding: OptionalPaddingValue = None
    code_text_style: Optional[TextStyle] = None
    h1_text_style: Optional[TextStyle] = None
    h1_padding: OptionalPaddingValue = None
    h2_text_style: Optional[TextStyle] = None
    h2_padding: OptionalPaddingValue = None
    h3_text_style: Optional[TextStyle] = None
    h3_padding: OptionalPaddingValue = None
    h4_text_style: Optional[TextStyle] = None
    h4_padding: OptionalPaddingValue = None
    h5_text_style: Optional[TextStyle] = None
    h5_padding: OptionalPaddingValue = None
    h6_text_style: Optional[TextStyle] = None
    h6_padding: OptionalPaddingValue = None
    em_text_style: Optional[TextStyle] = None
    strong_text_style: Optional[TextStyle] = None
    del_text_style: Optional[TextStyle] = None
    blockquote_text_style: Optional[TextStyle] = None
    img_text_style: Optional[TextStyle] = None
    checkbox_text_style: Optional[TextStyle] = None
    block_spacing: OptionalNumber = None
    list_indent: OptionalNumber = None
    list_bullet_text_style: Optional[TextStyle] = None
    list_bullet_padding: OptionalPaddingValue = None
    table_head_text_style: Optional[TextStyle] = None
    table_body_text_style: Optional[TextStyle] = None
    table_head_text_align: Optional[TextAlign] = None
    table_padding: OptionalPaddingValue = None
    table_cells_padding: OptionalPaddingValue = None
    blockquote_padding: OptionalPaddingValue = None
    table_cells_decoration: Optional[BoxDecoration] = None
    blockquote_decoration: Optional[BoxDecoration] = None
    codeblock_padding: OptionalPaddingValue = None
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


@control("Markdown")
class Markdown(ConstrainedControl):
    """
    Control for rendering text in markdown format.

    -----

    Online docs: https://flet.dev/docs/controls/markdown
    """

    value: str = ""
    selectable: bool = False
    extension_set: MarkdownExtensionSet = MarkdownExtensionSet.NONE
    code_theme: Optional[Union[MarkdownCodeTheme, MarkdownCustomCodeTheme]] = None
    auto_follow_links: bool = False
    shrink_wrap: bool = True
    fit_content: bool = True
    soft_line_break: bool = False
    auto_follow_links_target: Optional[UrlTarget] = None
    img_error_content: Optional[Control] = None
    code_style_sheet: Optional[MarkdownStyleSheet] = None
    md_style_sheet: Optional[MarkdownStyleSheet] = None
    on_tap_text: OptionalControlEventCallable = None
    on_selection_change: OptionalEventCallable[TextSelectionChangeEvent] = None
    on_tap_link: OptionalControlEventCallable = None
