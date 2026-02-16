from typing import Optional, Union

import flet as ft
from flet_code_editor.types import CodeLanguage, CodeTheme, GutterStyle

__all__ = ["CodeEditor"]


@ft.control("CodeEditor")
class CodeEditor(ft.LayoutControl):
    """Edit and highlight source code."""

    language: Optional[CodeLanguage] = None
    """
    Syntax highlighting language.
    """

    code_theme: Optional[Union[str, CodeTheme]] = None
    """
    Highlighting theme or a named theme.

    /// details | Supported named themes
        type: note

    `a11y-dark`, `a11y-light`, `agate`, `an-old-hope`, `androidstudio`, `arduino-light`,
    `arta`, `ascetic`, `atelier-cave-dark`, `atelier-cave-light`, `atelier-dune-dark`,
    `atelier-dune-light`, `atelier-estuary-dark`, `atelier-estuary-light`,
    `atelier-forest-dark`, `atelier-forest-light`, `atelier-heath-dark`,
    `atelier-heath-light`, `atelier-lakeside-dark`, `atelier-lakeside-light`,
    `atelier-plateau-dark`, `atelier-plateau-light`, `atelier-savanna-dark`,
    `atelier-savanna-light`, `atelier-seaside-dark`, `atelier-seaside-light`,
    `atelier-sulphurpool-dark`, `atelier-sulphurpool-light`, `atom-one-dark`,
    `atom-one-dark-reasonable`, `atom-one-light`, `brown-paper`, `codepen-embed`,
    `color-brewer`, `darcula`, `dark`, `default`, `docco`, `dracula`, `far`,
    `foundation`, `github`, `github-gist`, `gml`, `googlecode`, `gradient-dark`,
    `grayscale`, `gruvbox-dark`, `gruvbox-light`, `hopscotch`, `hybrid`, `idea`,
    `ir-black`, `isbl-editor-dark`, `isbl-editor-light`, `kimbie.dark`, `kimbie.light`,
    `lightfair`, `magula`, `mono-blue`, `monokai`, `monokai-sublime`, `night-owl`,
    `nord`, `obsidian`, `ocean`, `paraiso-dark`, `paraiso-light`, `pojoaque`,
    `purebasic`, `qtcreator_dark`, `qtcreator_light`, `railscasts`, `rainbow`,
    `routeros`, `school-book`, `shades-of-purple`, `solarized-dark`, `solarized-light`,
    `sunburst`, `tomorrow`, `tomorrow-night`, `tomorrow-night-blue`,
    `tomorrow-night-bright`, `tomorrow-night-eighties`, `vs`, `vs2015`, `xcode`,
    `xt256`, `zenburn`.
    ///
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
    [`on_selection_change`][(c).] when the editor is focused.
    """

    gutter_style: Optional[GutterStyle] = None
    """Gutter styling."""

    autocompletion_enabled: Optional[bool] = False
    """Whether autocompletion is enabled."""

    autocompletion_words: Optional[list[str]] = None
    """Words offered by autocompletion."""

    read_only: Optional[bool] = False
    """Whether the editor is read-only."""

    autofocus: Optional[bool] = False
    """Whether this editor should focus itself if nothing else is focused."""

    on_change: Optional[ft.ControlEventHandler["CodeEditor"]] = None
    """Called when the editor text changes."""

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
