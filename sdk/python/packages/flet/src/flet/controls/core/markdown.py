from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from flet.controls.base_control import control
from flet.controls.box import BoxDecoration
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import (
    OptionalControlEventHandler,
    OptionalEventHandler,
)
from flet.controls.core.text import TextSelectionChangeEvent
from flet.controls.padding import OptionalPaddingValue
from flet.controls.text_style import OptionalTextStyle
from flet.controls.types import (
    MainAxisAlignment,
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
    a_text_style: OptionalTextStyle = None
    p_text_style: OptionalTextStyle = None
    p_padding: OptionalPaddingValue = None
    code_text_style: OptionalTextStyle = None
    h1_text_style: OptionalTextStyle = None
    h1_padding: OptionalPaddingValue = None
    h2_text_style: OptionalTextStyle = None
    h2_padding: OptionalPaddingValue = None
    h3_text_style: OptionalTextStyle = None
    h3_padding: OptionalPaddingValue = None
    h4_text_style: OptionalTextStyle = None
    h4_padding: OptionalPaddingValue = None
    h5_text_style: OptionalTextStyle = None
    h5_padding: OptionalPaddingValue = None
    h6_text_style: OptionalTextStyle = None
    h6_padding: OptionalPaddingValue = None
    em_text_style: OptionalTextStyle = None
    strong_text_style: OptionalTextStyle = None
    del_text_style: OptionalTextStyle = None
    blockquote_text_style: OptionalTextStyle = None
    img_text_style: OptionalTextStyle = None
    checkbox_text_style: OptionalTextStyle = None
    block_spacing: OptionalNumber = None
    list_indent: OptionalNumber = None
    list_bullet_text_style: OptionalTextStyle = None
    list_bullet_padding: OptionalPaddingValue = None
    table_head_text_style: OptionalTextStyle = None
    table_body_text_style: OptionalTextStyle = None
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
    addition: OptionalTextStyle = None
    attr: OptionalTextStyle = None
    attribute: OptionalTextStyle = None
    built_in: OptionalTextStyle = None
    builtin_name: OptionalTextStyle = None
    bullet: OptionalTextStyle = None
    class_name: OptionalTextStyle = None
    code: OptionalTextStyle = None
    comment: OptionalTextStyle = None
    deletion: OptionalTextStyle = None
    doctag: OptionalTextStyle = None
    emphasis: OptionalTextStyle = None
    formula: OptionalTextStyle = None
    function: OptionalTextStyle = None
    keyword: OptionalTextStyle = None
    link: OptionalTextStyle = None
    link_label: OptionalTextStyle = None
    literal: OptionalTextStyle = None
    meta: OptionalTextStyle = None
    meta_keyword: OptionalTextStyle = None
    meta_string: OptionalTextStyle = None
    name: OptionalTextStyle = None
    number: OptionalTextStyle = None
    operator: OptionalTextStyle = None
    params: OptionalTextStyle = None
    pattern_match: OptionalTextStyle = None
    quote: OptionalTextStyle = None
    regexp: OptionalTextStyle = None
    root: OptionalTextStyle = None
    section: OptionalTextStyle = None
    selector_attr: OptionalTextStyle = None
    selector_class: OptionalTextStyle = None
    selector_id: OptionalTextStyle = None
    selector_pseudo: OptionalTextStyle = None
    selector_tag: OptionalTextStyle = None
    string: OptionalTextStyle = None
    strong: OptionalTextStyle = None
    stronge: OptionalTextStyle = None
    subst: OptionalTextStyle = None
    subtr: OptionalTextStyle = None
    symbol: OptionalTextStyle = None
    tag: OptionalTextStyle = None
    template_tag: OptionalTextStyle = None
    template_variable: OptionalTextStyle = None
    title: OptionalTextStyle = None
    type: OptionalTextStyle = None
    variable: OptionalTextStyle = None


@control("Markdown")
class Markdown(ConstrainedControl):
    """
    Control for rendering text in markdown format.

    Online docs: https://flet.dev/docs/controls/markdown
    """

    value: str = ""
    """
    Markdown content to render.
    """

    selectable: bool = False
    """
    Whether rendered text is selectable or not.
    """

    extension_set: MarkdownExtensionSet = MarkdownExtensionSet.NONE
    """
    The extensions to use when rendering the markdown content.

    Value is of type
    [`MarkdownExtensionSet`](https://flet.dev/docs/reference/types/markdownextensionset)
    and defaults to `MarkdownExtensionSet.NONE`.
    """

    code_theme: Optional[Union[MarkdownCodeTheme, MarkdownCustomCodeTheme]] = None
    """
    A syntax highlighting theme for code blocks.

    Value is of type
    [`MarkdownCodeTheme`](https://flet.dev/docs/reference/types/markdowncodetheme)
    and defaults to `MarkdownCodeTheme.GITHUB`.
    """

    auto_follow_links: bool = False
    """
    Automatically open URLs in the document.

    Default is `False`. If registered, `on_tap_link` event is fired after that.
    """

    shrink_wrap: bool = True
    """
    Whether the extent of the scroll view in the scroll direction should be determined
    by the contents being viewed.

    Value is of type `bool` and defaults to `True`.
    """

    fit_content: bool = True
    """
    Whether to allow the widget to fit the child content.

    Value is of type `bool` and defaults to `True`.
    """

    soft_line_break: bool = False
    """
    The soft line break is used to identify the spaces at the end of a line of text
    and the leading spaces in the immediately following the line of text.

    Value is of type `bool` and defaults to `False`.
    """

    auto_follow_links_target: Optional[UrlTarget] = None
    """
    Where to open URL in the web mode.

    Value is of type
    [`UrlTarget`](https://flet.dev/docs/reference/types/urltarget)
    and defaults to `UrlTarget.SELF`.
    """

    img_error_content: Optional[Control] = None
    """
    The `Control` to display when an image fails to load.
    """

    code_style_sheet: Optional[MarkdownStyleSheet] = None
    """
    The styles to use when displaying the code blocks.

    Value is of type
    [`MarkdownStyleSheet`](https://flet.dev/docs/reference/types/markdownstylesheet).
    """

    md_style_sheet: Optional[MarkdownStyleSheet] = None
    """
    The styles to use when displaying the markdown.

    Value is of type
    [`MarkdownStyleSheet`](https://flet.dev/docs/reference/types/markdownstylesheet).
    """

    on_tap_text: OptionalControlEventHandler["Markdown"] = None
    """
    Fires when some text is clicked/tapped.
    """

    on_selection_change: OptionalEventHandler[TextSelectionChangeEvent[
        "Markdown"]] = None
    """
    Fires when the text selection changes.

    Event handler argument is of type
    [`MarkdownSelectionChangeEvent`](https://flet.dev/docs/reference/types/markdownselectionchangeevent).
    """

    on_tap_link: OptionalControlEventHandler["Markdown"] = None
    """
    Fires when a link within Markdown document is clicked/tapped.

    `data` property of event contains URL.

    Example:
    https://github.com/flet-dev/examples/blob/main/python/controls/information-displays/markdown/markdown-event-example.py
    """
