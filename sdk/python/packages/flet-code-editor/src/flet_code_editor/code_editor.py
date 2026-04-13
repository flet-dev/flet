from dataclasses import dataclass
from typing import Optional, TypeVar, Union

import flet as ft
from flet_code_editor.types import CodeLanguage, CodeTheme, CustomCodeTheme, GutterStyle

__all__ = ["CodeEditor", "CodeEditorAnalyzeEvent", "CodeEditorIssue"]

EventControlType = TypeVar("EventControlType")


@dataclass
class CodeEditorIssue:
    # ISSUE-6312: Python-side analyzer output rendered in the Flutter gutter.
    """Analysis issue rendered in the editor gutter."""

    line: int
    """Zero-based line number highlighted in the gutter."""

    message: str
    """Human-readable issue description."""

    type: str = "error"
    """Issue severity: ``error``, ``warning`` or ``info``."""

    suggestion: Optional[str] = None
    """Optional quick-fix suggestion shown in tooltips when supported."""

    url: Optional[str] = None
    """Optional URL with extra issue details."""


@dataclass
class CodeEditorAnalyzeEvent(ft.Event[EventControlType]):
    # ISSUE-6312: Generic analysis callback requested by maintainer review.
    """Payload emitted by :attr:`CodeEditor.on_analyze`."""

    value: str
    """Current editor contents to analyze."""

    language: Optional[str] = None
    """Active editor language identifier."""

    selection: Optional[ft.TextSelection] = None
    """Current editor selection when available."""


@ft.control("CodeEditor")
class CodeEditor(ft.LayoutControl):
    """Edit and highlight source code."""

    language: Optional[CodeLanguage] = None
    """
    Syntax highlighting language.
    """

    code_theme: Optional[Union[CodeTheme, CustomCodeTheme]] = None
    """
    Syntax highlighting theme.
    """

    text_style: Optional[ft.TextStyle] = None
    """Text style for the editor content."""

    padding: Optional[ft.PaddingValue] = None
    """Padding around the editor."""

    value: Optional[str] = None
    """Full text including folded sections and service comments."""

    selection: Optional[ft.TextSelection] = None
    """
    Represents the current text selection or caret position in the editor.

    Setting this property updates the editor selection and may trigger
    :attr:`on_selection_change` when the editor is focused.
    """

    gutter_style: Optional[GutterStyle] = None
    """Gutter styling."""

    autocomplete: Optional[bool] = False
    """Whether autocomplete is enabled."""

    autocomplete_words: Optional[list[str]] = None
    """Words offered by autocomplete."""

    read_only: Optional[bool] = False
    """Whether the editor is read-only."""

    autofocus: Optional[bool] = False
    """Whether this editor should focus itself if nothing else is focused."""

    issues: Optional[list[CodeEditorIssue]] = None
    """Issues rendered in the gutter, typically set from :attr:`on_analyze`."""

    on_change: Optional[ft.ControlEventHandler["CodeEditor"]] = None
    """Called when the editor text changes."""

    on_analyze: Optional[ft.EventHandler[CodeEditorAnalyzeEvent["CodeEditor"]]] = None
    """Called when the editor requests analysis from Python code."""

    on_selection_change: Optional[
        ft.EventHandler[ft.TextSelectionChangeEvent["CodeEditor"]]
    ] = None
    """Called when the text selection or caret position changes."""

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
