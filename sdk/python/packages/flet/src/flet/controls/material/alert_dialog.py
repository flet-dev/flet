from dataclasses import field
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.control import Control
from flet.controls.dialog_control import DialogControl
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    MainAxisAlignment,
    Number,
    StrOrControl,
)

__all__ = ["AlertDialog"]


@control("AlertDialog")
class AlertDialog(DialogControl):
    """
    Can be used to inform the user about situations that require acknowledgement.

    It has an optional [`title`][(c).] and an optional list of [`actions`][(c).] . The
    `title` is displayed above the [`content`][(c).] and the `actions` are displayed
    below the `content`.

    ```python
    ft.AlertDialog(
        title=ft.Text("Session expired"),
        content=ft.Text("Please sign in again to continue."),
        actions=[ft.TextButton("Dismiss")],
        open=True,
    )
    ```
    """

    content: Optional[Control] = None
    """
    The content of this dialog is displayed in the center of this dialog in a
    lighter font.

    Typically this is a [`Column`][flet.]
    that contains this dialog's [`Text`][flet.] message.
    """

    modal: bool = False
    """
    Whether dialog can be dismissed/closed by clicking the area outside of it.
    """

    title: Optional[StrOrControl] = None
    """
    The title of this dialog is displayed in a large font at its top.

    Typically a [`Text`][flet.] control.
    """

    actions: list[Control] = field(default_factory=list)
    """
    A set of actions that are displayed at the bottom of this dialog.

    Typically this is a list of [`TextButton`][flet.] controls.

    Raises:
        ValueError: If none of [`title`][(c).], [`content`][(c).], or
            [`actions`][(c).] are provided, as the dialog would have nothing to display.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The background color of this dialog's surface.
    """

    elevation: Optional[Number] = None
    """
    Defines the elevation (z-coordinate) at which this dialog should appear.
    """

    icon: Optional[Control] = None
    """
    A control that is displayed at the top of this dialog.

    Typically a [`Icon`][flet.] control.
    """

    title_padding: Optional[PaddingValue] = None
    """
    Padding around the [`title`][(c).].

    If there is no title, no padding will be provided. Otherwise, this padding is used.

    Defaults to `24` pixels on the top, left, and right of the [`title`][(c).].
    If the [`content`][(c).] is not `None`, then no bottom padding
    is provided (see [`content_padding`][(c).]).
    If it is not set, then an extra `20` pixels of bottom padding is added to separate
    the [`title`][(c).] from the [`actions`][(c).].
    """

    content_padding: Optional[PaddingValue] = None
    """
    Padding around the [`content`][(c).].

    If there is no `content`, no padding will be provided. Otherwise, padding of `20`
    pixels is provided above the content to separate the [`content`][(c).] from
    the [`title`][(c).], and padding of `24` pixels is provided on the left, right,
    and bottom to separate the [`content`][(c).] from the other edges of this dialog.
    """

    actions_padding: Optional[PaddingValue] = None
    """
    Padding around the set of [`actions`][(c).] at the bottom of this dialog.

    Typically used to provide padding to the button bar between the button bar and the
    edges of this dialog.

    If are no actions, then no padding will be included. The padding around the button
    bar defaults to zero.
    """

    actions_alignment: Optional[MainAxisAlignment] = None
    """
    Defines the horizontal layout of the actions.

    Internally defaults to [`MainAxisAlignment.END`][flet.].
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of this dialog.

    If `None`, defaults to [`DialogTheme.shape`][flet.].
    If it is also `None`, it defaults to `RoundedRectangleBorder(radius=4.0)`.
    """

    inset_padding: Optional[PaddingValue] = None
    """
    Padding around this dialog itself.

    Defaults to `Padding.symmetric(vertical=40, horizontal=24)` - `40` pixels
    horizontally and `24` pixels vertically outside of this dialog box.
    """

    icon_padding: Optional[PaddingValue] = None
    """
    Padding around the [`icon`][(c).].
    """

    action_button_padding: Optional[PaddingValue] = None
    """
    The padding that surrounds each button in [`actions`][(c).].
    """

    shadow_color: Optional[ColorValue] = None
    """
    The color used to paint a drop shadow
    under this dialog, which reflects this dialog's [`elevation`][(c).].
    """

    icon_color: Optional[ColorValue] = None
    """
    The color for the Icon in the [`icon`][(c).] of this dialog.

    If `None`, [`DialogTheme.icon_color`][flet.] is used.
    If that is null, defaults to color scheme's [`ColorScheme.secondary`][flet.] if
    [`Theme.use_material3`][flet.] is `True`, `Colors.BLACK` otherwise.
    """

    scrollable: bool = False
    """
    Determines whether the [`title`][(c).] and
    [`content`][(c).] controls are wrapped in a scrollable.

    This configuration is used when the `title` and `content` are expected to overflow.
    Both `title` and `content` are wrapped in a scroll view, allowing all overflowed
    content to be visible while still showing the button bar.
    """

    actions_overflow_button_spacing: Optional[Number] = None
    """
    The spacing between [`actions`][(c).] when the `OverflowBar`
    switches to a column layout because the actions don't fit horizontally.

    If the controls in `actions` do not fit into a single row, they are arranged into a
    column. This parameter provides additional vertical space between buttons when it
    does overflow.
    """

    alignment: Optional[Alignment] = None
    """
    How to align this dialog.

    If `None`, then [`DialogTheme.alignment`][flet.] is used.
    If that is also `None`, the default is [`Alignment.CENTER`][flet.].
    """

    content_text_style: Optional[TextStyle] = None
    """
    The style for the text in the [`content`][(c).] of this dialog.

    If `None`, [`DialogTheme.content_text_style`][flet.] is used.
    If that's is also `None`, defaults to
    [`TextTheme.body_medium`][flet.] (if [`Theme.use_material3`][flet.] is `True`;
    [`TextTheme.title_medium`][flet.] otherwise) of
    [Theme.text_theme][flet.Theme.text_theme].
    """

    title_text_style: Optional[TextStyle] = None
    """
    TBD
    """

    clip_behavior: ClipBehavior = ClipBehavior.NONE
    """
    Defines how the contents of this dialog are clipped (or not)
    to the given [`shape`][(c).].
    """

    semantics_label: Optional[str] = None
    """
    The semantic label of this dialog used by accessibility frameworks to announce
    screen transitions when this dialog is opened and closed.

    On iOS, if this label is not provided, a semantic label will be inferred from the
    [`title`][(c).] if it is not `None`.
    """

    barrier_color: Optional[ColorValue] = None
    """
    The color of the modal barrier that
    darkens everything below this dialog.

    If `None`, then [`DialogTheme.barrier_color`][flet.] is used.
    If that is also `None`, the default is `Colors.BLACK_54`.
    """

    def before_update(self):
        super().before_update()
        if not (self.title or self.content or self.actions):
            raise ValueError(
                "AlertDialog has nothing to display. Provide at minimum one of the "
                "following: title, content, actions"
            )
