from dataclasses import dataclass
from typing import Optional

import flet as ft

__all__ = ["CodeTheme", "GutterStyle", "TextEditingValue"]


@dataclass
class CodeTheme:
    """Defines syntax highlighting styles for code tokens."""

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


@dataclass
class TextEditingValue:
    """Represents the current text and selection."""

    text: str
    """The visible text."""

    selection: Optional[ft.TextSelection] = None
    """The current text selection."""
