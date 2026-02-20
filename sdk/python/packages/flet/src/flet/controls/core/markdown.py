from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from flet.controls.base_control import control
from flet.controls.box import BoxDecoration
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler, EventHandler
from flet.controls.core.text import TextSelectionChangeEvent
from flet.controls.layout_control import LayoutControl
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    MainAxisAlignment,
    Number,
    TextAlign,
    UrlTarget,
)

__all__ = [
    "Markdown",
    "MarkdownCodeTheme",
    "MarkdownCustomCodeTheme",
    "MarkdownExtensionSet",
    "MarkdownStyleSheet",
]


class MarkdownExtensionSet(Enum):
    """
    Preset markdown syntax extension bundles for [`Markdown`][flet.].

    The selected set controls which block/inline syntaxes are enabled while
    parsing [`Markdown.value`][flet.].
    """

    NONE = "none"
    """
    Basic markdown parsing without additional extension bundle.
    """

    COMMON_MARK = "commonMark"
    """
    CommonMark-compatible extension set.
    """

    GITHUB_WEB = "gitHubWeb"
    """
    GitHub web renderer style extension set.
    """

    GITHUB_FLAVORED = "gitHubFlavored"
    """
    GitHub Flavored Markdown (GFM) extension set.
    """


@dataclass
class MarkdownStyleSheet:
    """
    Style overrides for markdown element rendering.

    Each field customizes one element group (headings, paragraphs, tables,
    lists, block quotes, code blocks, etc.). Any `None` field keeps the
    control's default styling for that property.
    """

    a_text_style: Optional[TextStyle] = None
    """
    Text style for links (`<a>`).
    """

    p_text_style: Optional[TextStyle] = None
    """
    Text style for paragraph blocks.
    """

    p_padding: Optional[PaddingValue] = None
    """
    Padding around paragraph blocks.
    """

    code_text_style: Optional[TextStyle] = None
    """
    Text style for inline code spans.
    """

    h1_text_style: Optional[TextStyle] = None
    """
    Text style for level-1 headings.
    """

    h1_padding: Optional[PaddingValue] = None
    """
    Padding around level-1 headings.
    """

    h2_text_style: Optional[TextStyle] = None
    """
    Text style for level-2 headings.
    """

    h2_padding: Optional[PaddingValue] = None
    """
    Padding around level-2 headings.
    """

    h3_text_style: Optional[TextStyle] = None
    """
    Text style for level-3 headings.
    """

    h3_padding: Optional[PaddingValue] = None
    """
    Padding around level-3 headings.
    """

    h4_text_style: Optional[TextStyle] = None
    """
    Text style for level-4 headings.
    """

    h4_padding: Optional[PaddingValue] = None
    """
    Padding around level-4 headings.
    """

    h5_text_style: Optional[TextStyle] = None
    """
    Text style for level-5 headings.
    """

    h5_padding: Optional[PaddingValue] = None
    """
    Padding around level-5 headings.
    """

    h6_text_style: Optional[TextStyle] = None
    """
    Text style for level-6 headings.
    """

    h6_padding: Optional[PaddingValue] = None
    """
    Padding around level-6 headings.
    """

    em_text_style: Optional[TextStyle] = None
    """
    Text style for emphasized text.
    """

    strong_text_style: Optional[TextStyle] = None
    """
    Text style for strong (bold) text.
    """

    del_text_style: Optional[TextStyle] = None
    """
    Text style for deleted/strikethrough text.
    """

    blockquote_text_style: Optional[TextStyle] = None
    """
    Text style for blockquote content.
    """

    img_text_style: Optional[TextStyle] = None
    """
    Text style for image alt text / fallback labels.
    """

    checkbox_text_style: Optional[TextStyle] = None
    """
    Text style for task-list checkbox labels.
    """

    block_spacing: Optional[Number] = None
    """
    Vertical spacing between markdown block elements.
    """

    list_indent: Optional[Number] = None
    """
    Indentation width for list items.
    """

    list_bullet_text_style: Optional[TextStyle] = None
    """
    Text style for list bullets/markers.
    """

    list_bullet_padding: Optional[PaddingValue] = None
    """
    Padding around list bullet markers.
    """

    table_head_text_style: Optional[TextStyle] = None
    """
    Text style for table header cells.
    """

    table_body_text_style: Optional[TextStyle] = None
    """
    Text style for table body cells.
    """

    table_head_text_align: Optional[TextAlign] = None
    """
    Text alignment for table header cells.
    """

    table_padding: Optional[PaddingValue] = None
    """
    Outer padding around rendered table blocks.
    """

    table_cells_padding: Optional[PaddingValue] = None
    """
    Inner padding for each table cell.
    """

    blockquote_padding: Optional[PaddingValue] = None
    """
    Inner padding for blockquote container.
    """

    table_cells_decoration: Optional[BoxDecoration] = None
    """
    Decoration applied to table cells.
    """

    blockquote_decoration: Optional[BoxDecoration] = None
    """
    Decoration applied to blockquote container.
    """

    codeblock_padding: Optional[PaddingValue] = None
    """
    Inner padding for fenced code blocks.
    """

    codeblock_decoration: Optional[BoxDecoration] = None
    """
    Decoration applied to fenced code blocks.
    """

    horizontal_rule_decoration: Optional[BoxDecoration] = None
    """
    Decoration used to render horizontal rule separators.
    """

    blockquote_alignment: Optional[MainAxisAlignment] = None
    """
    Alignment for blockquote block content.
    """

    codeblock_alignment: Optional[MainAxisAlignment] = None
    """
    Alignment for code block content.
    """

    h1_alignment: Optional[MainAxisAlignment] = None
    """
    Alignment for level-1 heading blocks.
    """

    h2_alignment: Optional[MainAxisAlignment] = None
    """
    Alignment for level-2 heading blocks.
    """

    h3_alignment: Optional[MainAxisAlignment] = None
    """
    Alignment for level-3 heading blocks.
    """

    h4_alignment: Optional[MainAxisAlignment] = None
    """
    Alignment for level-4 heading blocks.
    """

    h5_alignment: Optional[MainAxisAlignment] = None
    """
    Alignment for level-5 heading blocks.
    """

    h6_alignment: Optional[MainAxisAlignment] = None
    """
    Alignment for level-6 heading blocks.
    """

    text_alignment: Optional[MainAxisAlignment] = None
    """
    Default alignment for regular text blocks.
    """

    ordered_list_alignment: Optional[MainAxisAlignment] = None
    """
    Alignment for ordered list blocks.
    """

    unordered_list_alignment: Optional[MainAxisAlignment] = None
    """
    Alignment for unordered list blocks.
    """


class MarkdownCodeTheme(Enum):
    """
    Built-in code highlighting themes for markdown code blocks.

    Use with [`Markdown.code_theme`][flet.] to choose
    a predefined syntax highlighting palette by name.
    """

    A11Y_DARK = "a11y-dark"
    """
    Uses the `a11y-dark` syntax highlighting theme.
    """
    A11Y_LIGHT = "a11y-light"
    """
    Uses the `a11y-light` syntax highlighting theme.
    """
    AGATE = "agate"
    """
    Uses the `agate` syntax highlighting theme.
    """
    AN_OLD_HOPE = "an-old-hope"
    """
    Uses the `an-old-hope` syntax highlighting theme.
    """
    ANDROID_STUDIO = "androidstudio"
    """
    Uses the `androidstudio` syntax highlighting theme.
    """
    ARDUINO_LIGHT = "arduino-light"
    """
    Uses the `arduino-light` syntax highlighting theme.
    """
    ARTA = "arta"
    """
    Uses the `arta` syntax highlighting theme.
    """
    ASCETIC = "ascetic"
    """
    Uses the `ascetic` syntax highlighting theme.
    """
    ATELIER_CAVE_DARK = "atelier-cave-dark"
    """
    Uses the `atelier-cave-dark` syntax highlighting theme.
    """
    ATELIER_CAVE_LIGHT = "atelier-cave-light"
    """
    Uses the `atelier-cave-light` syntax highlighting theme.
    """
    ATELIER_DUNE_DARK = "atelier-dune-dark"
    """
    Uses the `atelier-dune-dark` syntax highlighting theme.
    """
    ATELIER_DUNE_LIGHT = "atelier-dune-light"
    """
    Uses the `atelier-dune-light` syntax highlighting theme.
    """
    ATELIER_ESTUARY_DARK = "atelier-estuary-dark"
    """
    Uses the `atelier-estuary-dark` syntax highlighting theme.
    """
    ATELIER_ESTUARY_LIGHT = "atelier-estuary-light"
    """
    Uses the `atelier-estuary-light` syntax highlighting theme.
    """
    ATELIER_FOREST_DARK = "atelier-forest-dark"
    """
    Uses the `atelier-forest-dark` syntax highlighting theme.
    """
    ATELIER_FOREST_LIGHT = "atelier-forest-light"
    """
    Uses the `atelier-forest-light` syntax highlighting theme.
    """
    ATELIER_HEATH_DARK = "atelier-heath-dark"
    """
    Uses the `atelier-heath-dark` syntax highlighting theme.
    """
    ATELIER_HEATH_LIGHT = "atelier-heath-light"
    """
    Uses the `atelier-heath-light` syntax highlighting theme.
    """
    ATELIER_LAKESIDE_DARK = "atelier-lakeside-dark"
    """
    Uses the `atelier-lakeside-dark` syntax highlighting theme.
    """
    ATELIER_LAKESIDE_LIGHT = "atelier-lakeside-light"
    """
    Uses the `atelier-lakeside-light` syntax highlighting theme.
    """
    ATELIER_PLATEAU_DARK = "atelier-plateau-dark"
    """
    Uses the `atelier-plateau-dark` syntax highlighting theme.
    """
    ATELIER_PLATEAU_LIGHT = "atelier-plateau-light"
    """
    Uses the `atelier-plateau-light` syntax highlighting theme.
    """
    ATELIER_SAVANNA_DARK = "atelier-savanna-dark"
    """
    Uses the `atelier-savanna-dark` syntax highlighting theme.
    """
    ATELIER_SAVANNA_LIGHT = "atelier-savanna-light"
    """
    Uses the `atelier-savanna-light` syntax highlighting theme.
    """
    ATELIER_SEASIDE_DARK = "atelier-seaside-dark"
    """
    Uses the `atelier-seaside-dark` syntax highlighting theme.
    """
    ATELIER_SEASIDE_LIGHT = "atelier-seaside-light"
    """
    Uses the `atelier-seaside-light` syntax highlighting theme.
    """
    ATELIER_SULPHURPOOL_DARK = "atelier-sulphurpool-dark"
    """
    Uses the `atelier-sulphurpool-dark` syntax highlighting theme.
    """
    ATELIER_SULPHURPOOL_LIGHT = "atelier-sulphurpool-light"
    """
    Uses the `atelier-sulphurpool-light` syntax highlighting theme.
    """
    ATOM_ONE_DARK_REASONABLE = "atom-one-dark-reasonable"
    """
    Uses the `atom-one-dark-reasonable` syntax highlighting theme.
    """
    ATOM_ONE_DARK = "atom-one-dark"
    """
    Uses the `atom-one-dark` syntax highlighting theme.
    """
    ATOM_ONE_LIGHT = "atom-one-light"
    """
    Uses the `atom-one-light` syntax highlighting theme.
    """
    BROWN_PAPER = "brown-paper"
    """
    Uses the `brown-paper` syntax highlighting theme.
    """
    CODEPEN_EMBED = "codepen-embed"
    """
    Uses the `codepen-embed` syntax highlighting theme.
    """
    COLOR_BREWER = "color-brewer"
    """
    Uses the `color-brewer` syntax highlighting theme.
    """
    DRACULA = "dracula"
    """
    Uses the `dracula` syntax highlighting theme.
    """
    DARK = "dark"
    """
    Uses the `dark` syntax highlighting theme.
    """
    DEFAULT = "default"
    """
    Uses the `default` syntax highlighting theme.
    """
    DOCCO = "docco"
    """
    Uses the `docco` syntax highlighting theme.
    """
    DRAGULA = "dracula"
    """
    Uses the `dracula` syntax highlighting theme.
    """
    FAR = "far"
    """
    Uses the `far` syntax highlighting theme.
    """
    FOUNDATION = "foundation"
    """
    Uses the `foundation` syntax highlighting theme.
    """
    GITHUB_GIST = "github-gist"
    """
    Uses the `github-gist` syntax highlighting theme.
    """
    GITHUB = "github"
    """
    Uses the `github` syntax highlighting theme.
    """
    GML = "gml"
    """
    Uses the `gml` syntax highlighting theme.
    """
    GOOGLE_CODE = "googlecode"
    """
    Uses the `googlecode` syntax highlighting theme.
    """
    GRADIENT_DARK = "gradient-dark"
    """
    Uses the `gradient-dark` syntax highlighting theme.
    """
    GRAYSCALE = "grayscale"
    """
    Uses the `grayscale` syntax highlighting theme.
    """
    GRUVBOX_DARK = "gruvbox-dark"
    """
    Uses the `gruvbox-dark` syntax highlighting theme.
    """
    GRUVBOX_LIGHT = "gruvbox-light"
    """
    Uses the `gruvbox-light` syntax highlighting theme.
    """
    HOPSCOTCH = "hopscotch"
    """
    Uses the `hopscotch` syntax highlighting theme.
    """
    HYBRID = "hybrid"
    """
    Uses the `hybrid` syntax highlighting theme.
    """
    IDEA = "idea"
    """
    Uses the `idea` syntax highlighting theme.
    """
    IR_BLACK = "ir-black"
    """
    Uses the `ir-black` syntax highlighting theme.
    """
    ISBL_EDITOR_DARK = "isbl-editor-dark"
    """
    Uses the `isbl-editor-dark` syntax highlighting theme.
    """
    ISBL_EDITOR_LIGHT = "isbl-editor-light"
    """
    Uses the `isbl-editor-light` syntax highlighting theme.
    """
    KIMBIE_DARK = "kimbie.dark"
    """
    Uses the `kimbie.dark` syntax highlighting theme.
    """
    KIMBIE_LIGHT = "kimbie.light"
    """
    Uses the `kimbie.light` syntax highlighting theme.
    """
    LIGHTFAIR = "lightfair"
    """
    Uses the `lightfair` syntax highlighting theme.
    """
    MAGULA = "magula"
    """
    Uses the `magula` syntax highlighting theme.
    """
    MONO_BLUE = "mono-blue"
    """
    Uses the `mono-blue` syntax highlighting theme.
    """
    MONOKAI_SUBLIME = "monokai-sublime"
    """
    Uses the `monokai-sublime` syntax highlighting theme.
    """
    MONOKAI = "monokai"
    """
    Uses the `monokai` syntax highlighting theme.
    """
    NIGHT_OWL = "night-owl"
    """
    Uses the `night-owl` syntax highlighting theme.
    """
    NORD = "nord"
    """
    Uses the `nord` syntax highlighting theme.
    """
    OBSIDIAN = "obsidian"
    """
    Uses the `obsidian` syntax highlighting theme.
    """
    OCEAN = "ocean"
    """
    Uses the `ocean` syntax highlighting theme.
    """
    PARAISEO_DARK = "paraiso-dark"
    """
    Uses the `paraiso-dark` syntax highlighting theme.
    """
    PARAISEO_LIGHT = "paraiso-light"
    """
    Uses the `paraiso-light` syntax highlighting theme.
    """
    POJOAQUE = "pojoaque"
    """
    Uses the `pojoaque` syntax highlighting theme.
    """
    PURE_BASIC = "purebasic"
    """
    Uses the `purebasic` syntax highlighting theme.
    """
    QT_CREATOR_DARK = "qtcreator_dark"
    """
    Uses the `qtcreator_dark` syntax highlighting theme.
    """
    QT_CREATOR_LIGHT = "qtcreator_light"
    """
    Uses the `qtcreator_light` syntax highlighting theme.
    """
    RAILSCASTS = "railscasts"
    """
    Uses the `railscasts` syntax highlighting theme.
    """
    RAINBOW = "rainbow"
    """
    Uses the `rainbow` syntax highlighting theme.
    """
    ROUTERS = "routers"
    """
    Uses the `routers` syntax highlighting theme.
    """
    SCHOOL_BOOK = "school-book"
    """
    Uses the `school-book` syntax highlighting theme.
    """
    SHADES_OF_PURPLE = "shades-of-purple"
    """
    Uses the `shades-of-purple` syntax highlighting theme.
    """
    SOLARIZED_DARK = "solarized-dark"
    """
    Uses the `solarized-dark` syntax highlighting theme.
    """
    SOLARIZED_LIGHT = "solarized-light"
    """
    Uses the `solarized-light` syntax highlighting theme.
    """
    SUNBURST = "sunburst"
    """
    Uses the `sunburst` syntax highlighting theme.
    """
    TOMORROW_NIGHT_BLUE = "tomorrow-night-blue"
    """
    Uses the `tomorrow-night-blue` syntax highlighting theme.
    """
    TOMORROW_NIGHT_BRIGHT = "tomorrow-night-bright"
    """
    Uses the `tomorrow-night-bright` syntax highlighting theme.
    """
    TOMORROW_NIGHT_EIGHTIES = "tomorrow-night-eighties"
    """
    Uses the `tomorrow-night-eighties` syntax highlighting theme.
    """
    TOMORROW_NIGHT = "tomorrow-night"
    """
    Uses the `tomorrow-night` syntax highlighting theme.
    """
    TOMORROW = "tomorrow"
    """
    Uses the `tomorrow` syntax highlighting theme.
    """
    VS = "vs"
    """
    Uses the `vs` syntax highlighting theme.
    """
    VS2015 = "vs2015"
    """
    Uses the `vs2015` syntax highlighting theme.
    """
    XCODE = "xcode"
    """
    Uses the `xcode` syntax highlighting theme.
    """
    XT256 = "xt256"
    """
    Uses the `xt256` syntax highlighting theme.
    """
    ZENBURN = "zenburn"
    """
    Uses the `zenburn` syntax highlighting theme.
    """


@dataclass
class MarkdownCustomCodeTheme:
    """
    Custom text-style mapping for code token highlighting.

    Use this as [`Markdown.code_theme`][flet.] when you
    need per-token styling instead of a built-in
    [`MarkdownCodeTheme`][flet.].

    Field names correspond to code token kinds (for example `keyword`,
    `string`, `comment`). Unspecified fields keep default token styling.
    """

    addition: Optional[TextStyle] = None
    """
    Style for inserted/added diff tokens.
    """

    attr: Optional[TextStyle] = None
    """
    Style for attribute tokens.
    """

    attribute: Optional[TextStyle] = None
    """
    Style for alternative attribute token name.
    """

    built_in: Optional[TextStyle] = None
    """
    Style for built-in symbol tokens.
    """

    builtin_name: Optional[TextStyle] = None
    """
    Style for built-in name tokens.
    """

    bullet: Optional[TextStyle] = None
    """
    Style for bullet/list marker tokens.
    """

    class_name: Optional[TextStyle] = None
    """
    Style for class name tokens.
    """

    code: Optional[TextStyle] = None
    """
    Base style for code text.
    """

    comment: Optional[TextStyle] = None
    """
    Style for comment tokens.
    """

    deletion: Optional[TextStyle] = None
    """
    Style for removed/deleted diff tokens.
    """

    doctag: Optional[TextStyle] = None
    """
    Style for documentation tag tokens.
    """

    emphasis: Optional[TextStyle] = None
    """
    Style for emphasized tokens.
    """

    formula: Optional[TextStyle] = None
    """
    Style for formula/math tokens.
    """

    function: Optional[TextStyle] = None
    """
    Style for function identifier tokens.
    """

    keyword: Optional[TextStyle] = None
    """
    Style for keyword tokens.
    """

    link: Optional[TextStyle] = None
    """
    Style for link tokens.
    """

    link_label: Optional[TextStyle] = None
    """
    Style for link label tokens.
    """

    literal: Optional[TextStyle] = None
    """
    Style for literal constant tokens.
    """

    meta: Optional[TextStyle] = None
    """
    Style for metadata tokens.
    """

    meta_keyword: Optional[TextStyle] = None
    """
    Style for metadata keyword tokens.
    """

    meta_string: Optional[TextStyle] = None
    """
    Style for metadata string tokens.
    """

    name: Optional[TextStyle] = None
    """
    Style for generic name/identifier tokens.
    """

    number: Optional[TextStyle] = None
    """
    Style for numeric literal tokens.
    """

    operator: Optional[TextStyle] = None
    """
    Style for operator tokens.
    """

    params: Optional[TextStyle] = None
    """
    Style for parameter list tokens.
    """

    pattern_match: Optional[TextStyle] = None
    """
    Style for pattern matching tokens.
    """

    quote: Optional[TextStyle] = None
    """
    Style for quote/blockquote tokens.
    """

    regexp: Optional[TextStyle] = None
    """
    Style for regular expression tokens.
    """

    root: Optional[TextStyle] = None
    """
    Base style for root code container.
    """

    section: Optional[TextStyle] = None
    """
    Style for section heading tokens.
    """

    selector_attr: Optional[TextStyle] = None
    """
    Style for CSS selector attribute tokens.
    """

    selector_class: Optional[TextStyle] = None
    """
    Style for CSS selector class tokens.
    """

    selector_id: Optional[TextStyle] = None
    """
    Style for CSS selector id tokens.
    """

    selector_pseudo: Optional[TextStyle] = None
    """
    Style for CSS selector pseudo-class tokens.
    """

    selector_tag: Optional[TextStyle] = None
    """
    Style for CSS selector tag tokens.
    """

    string: Optional[TextStyle] = None
    """
    Style for string literal tokens.
    """

    strong: Optional[TextStyle] = None
    """
    Style for strong/bold tokens.
    """

    stronge: Optional[TextStyle] = None
    """
    Legacy/alternate token key style for strong text.
    """

    subst: Optional[TextStyle] = None
    """
    Style for substitution/interpolation tokens.
    """

    subtr: Optional[TextStyle] = None
    """
    Legacy/alternate token key style for substitution tokens.
    """

    symbol: Optional[TextStyle] = None
    """
    Style for symbol tokens.
    """

    tag: Optional[TextStyle] = None
    """
    Style for markup tag tokens.
    """

    template_tag: Optional[TextStyle] = None
    """
    Style for template tag tokens.
    """

    template_variable: Optional[TextStyle] = None
    """
    Style for template variable tokens.
    """

    title: Optional[TextStyle] = None
    """
    Style for title/name tokens.
    """

    type: Optional[TextStyle] = None
    """
    Style for type annotation tokens.
    """

    variable: Optional[TextStyle] = None
    """
    Style for variable identifier tokens.
    """


@control("Markdown")
class Markdown(LayoutControl):
    """
    Renders text in markdown format.

    ```python
    ft.Markdown(
        value="# Welcome\\n\\nThis is **Markdown** rendered in Flet.",
        width=260,
    )
    ```
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
    """

    code_theme: Optional[Union[MarkdownCodeTheme, MarkdownCustomCodeTheme]] = None
    """
    A syntax highlighting theme for code blocks.

    Defaults to `MarkdownCodeTheme.GITHUB`.
    """

    auto_follow_links: bool = False
    """
    Automatically open URLs in the document.

    If registered, `on_tap_link` event is fired after that.
    """

    shrink_wrap: bool = True
    """
    Whether the extent of the scroll view in the scroll direction should be determined \
    by the contents being viewed.
    """

    fit_content: bool = True
    """
    Whether to allow the widget to fit the child content.
    """

    soft_line_break: bool = False
    """
    The soft line break is used to identify the spaces at the end of a line of text \
    and the leading spaces in the immediately following the line of text.
    """

    auto_follow_links_target: Optional[UrlTarget] = None
    """
    Where to open URL in the web mode.
    """

    image_error_content: Optional[Control] = None
    """
    The control to display when an image fails to load.
    """

    code_style_sheet: Optional[MarkdownStyleSheet] = None
    """
    The styles to use when displaying the code blocks.
    """

    md_style_sheet: Optional[MarkdownStyleSheet] = None
    """
    The styles to use when displaying the markdown.
    """

    latex_scale_factor: Optional[float] = None
    """
    The scale factor for LaTeX formulas rendering.
    Controls the size of rendered mathematical expressions.
    """

    latex_style: Optional[TextStyle] = None
    """
    The text style to apply to LaTeX formulas.
    Allows customization of font, color, and other text properties
    for mathematical expressions.
    """

    on_tap_text: Optional[ControlEventHandler["Markdown"]] = None
    """
    Called when some text is clicked/tapped.
    """

    on_selection_change: Optional[
        EventHandler[TextSelectionChangeEvent["Markdown"]]
    ] = None
    """
    Called when the text selection changes.
    """

    on_tap_link: Optional[ControlEventHandler["Markdown"]] = None
    """
    Called when a link within Markdown document is clicked/tapped.

    The [`data`][flet.Event.] property of the event handler argument
    contains the clickedURL.

    Example:
    https://github.com/flet-dev/examples/blob/main/python/controls/information-displays/markdown/markdown-event-example.py
    """  # noqa: E501
