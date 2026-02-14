from dataclasses import dataclass
from typing import Optional

import flet as ft

__all__ = ["CodeTheme", "GutterStyle"]


@dataclass
class CodeTheme:
    """
    Defines syntax highlighting styles for code tokens.

    /// details | Supported style names
        type: note

    `addition`, `attr`, `attribute`, `built_in`, `builtin-name`, `bullet`, `class`,
    `code`, `comment`, `deletion`, `doctag`, `emphasis`, `formula`, `function`,
    `keyword`, `link`, `link_label`, `literal`, `meta`, `meta-keyword`,
    `meta-string`, `name`, `number`, `operator`, `params`, `pattern-match`, `quote`,
    `regexp`, `root`, `section`, `selector-attr`, `selector-class`, `selector-id`,
    `selector-pseudo`, `selector-tag`, `string`, `strong`, `stronge`, `subst`,
    `subtr`, `symbol`, `tag`, `template-tag`, `template-variable`, `title`, `type`,
    `variable`.
    ///
    """

    styles: dict[str, ft.TextStyle]
    """Map of token names to text styles."""


@dataclass
class GutterStyle:
    """Defines gutter appearance (line numbers) for the code editor."""

    text_style: Optional[ft.TextStyle] = None
    """Text style for line numbers."""

    background_color: Optional[ft.ColorValue] = None
    """Background color for the gutter."""

    width: Optional[ft.Number] = None
    """Fixed width of the gutter."""

    margin: Optional[ft.Number] = None
    """Margin outside the gutter."""

    show_errors: bool = True
    """Whether to show errors in the gutter."""

    show_folding_handles: bool = True
    """Whether to show folding handles in the gutter."""

    show_line_numbers: bool = True
    """Whether to show line numbers in the gutter."""
