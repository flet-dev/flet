from typing import Optional, Union

import flet as ft
from flet_code_editor.types import CodeTheme, GutterStyle, TextEditingValue

__all__ = ["CodeEditor"]


@ft.control("CodeEditor")
class CodeEditor(ft.LayoutControl):
    """Edit and highlight source code."""

    language: Optional[str] = None
    """Syntax highlighting language."""

    code_theme: Optional[Union[str, CodeTheme]] = None
    """Highlighting theme or a named theme (e.g. "atom-one-light")."""

    text_style: Optional[ft.TextStyle] = None
    """Text style for the editor content."""

    padding: Optional[ft.PaddingValue] = None
    """Padding around the editor."""

    text: Optional[str] = None
    """Visible text (excludes folded sections)."""

    value: Optional[TextEditingValue] = None
    """Visible text with selection (excludes folded sections)."""

    full_text: Optional[str] = None
    """Full text including folded sections and service comments."""

    gutter_style: Optional[GutterStyle] = None
    """Gutter styling."""

    autocompletion_enabled: Optional[bool] = False
    """Whether autocompletion is enabled."""

    autocompletion_words: Optional[list[str]] = None
    """Words offered by autocompletion."""

    read_only: Optional[bool] = False
    """Whether the editor is read-only."""

    on_change: Optional[ft.ControlEventHandler["CodeEditor"]] = None
    """Called when the editor text changes."""

    on_selection_change: Optional[
        ft.EventHandler[ft.TextSelectionChangeEvent["CodeEditor"]]
    ] = None
    """Called when the text selection changes."""

    on_focus: Optional[ft.ControlEventHandler["CodeEditor"]] = None
    """Called when the editor receives focus."""

    on_blur: Optional[ft.ControlEventHandler["CodeEditor"]] = None
    """Called when the editor loses focus."""

    async def focus(self):
        """Request focus for this editor."""
        await self._invoke_method("focus")

    async def fold_comment_at_line_zero(self):
        """Fold the comment block at line 0."""
        await self._invoke_method("fold_comment_at_line_zero")

    async def fold_imports(self):
        """Fold import sections."""
        await self._invoke_method("fold_imports")

    async def fold_at(self, line_number: int):
        """Fold the block starting at the given line number."""
        await self._invoke_method("fold_at", arguments={"line_number": line_number})
