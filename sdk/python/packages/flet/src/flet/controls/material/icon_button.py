from dataclasses import field
from typing import Optional, Union

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.box import BoxConstraints
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import ControlEventHandler
from flet.controls.padding import PaddingValue
from flet.controls.types import (
    ColorValue,
    IconDataOrControl,
    MouseCursor,
    Number,
    Url,
    VisualDensity,
)

__all__ = [
    "FilledIconButton",
    "FilledTonalIconButton",
    "IconButton",
    "OutlinedIconButton",
]


@control("IconButton")
class IconButton(ConstrainedControl, AdaptiveControl):
    """
    An icon button is a round button with an icon in the middle that reacts to touches
    by filling with color (ink).

    Icon buttons are commonly used in the toolbars, but they can be used in many other
    places as well.
    """

    icon: Optional[IconDataOrControl] = None
    """
    Icon shown in the button.
    """

    icon_color: Optional[ColorValue] = None
    """
    The foreground color of the icon.
    """

    icon_size: Optional[Number] = None
    """
    The [`icon`][flet.IconButton.icon]'s size in virtual pixels.

    Defaults to `24`.
    """

    selected: Optional[bool] = None
    """
    The optional selection state of the icon button.

    If this property is not set, the button will behave as a normal push button,
    otherwise, the button will toggle between showing [`icon`][flet.IconButton.icon]
    (when `False`), and [`selected_icon`][flet.IconButton.selected_icon] (when `True`).
    """

    selected_icon: Optional[IconDataOrControl] = None
    """
    The icon to be shown in this button for the 'selected' state.
    """

    selected_icon_color: Optional[ColorValue] = None
    """
    The icon color for the 'selected' state of this button.

    An example of icon toggle button:

    <img src="/img/blog/gradients/toggle-icon-button.gif" className="screenshot-10" />

    ```python
    import flet as ft

    def main(page: ft.Page):

        def toggle_icon_button(e):
            e.control.selected = not e.control.selected

        page.add(
            ft.IconButton(
                icon=ft.Icons.BATTERY_1_BAR,
                selected_icon=ft.Icons.BATTERY_FULL,
                on_click=toggle_icon_button,
                selected=False,
                style=ft.ButtonStyle(
                    color={
                        ft.ControlState.SELECTED: ft.Colors.GREEN,
                        ft.ControlState.DEFAULT: ft.Colors.RED
                    },
                ),
            )
        )

    ft.run(main)
    ```
    """

    bgcolor: Optional[ColorValue] = field(default=None, metadata={"skip": True})
    """
    The button's background color.
    """

    highlight_color: Optional[ColorValue] = None
    """
    The button's color when the button is
    pressed. The highlight fades in quickly as the button is held down.
    """

    style: Optional[ButtonStyle] = None
    """
    Customizes this button's appearance.

    Note:
        - Only honoured in Material 3 design
            ([`Theme.use_material3`][flet.Theme.use_material3] is `True` - default).
        - If [`Theme.use_material3`][flet.Theme.use_material3] is `True`,
            any parameters defined in style will be overridden by the
            corresponding parameters in this `IconButton`.
            For example, if icon button
            [`visual_density`][flet.IconButton.visual_density]
            is set to [`VisualDensity.STANDARD`][flet.VisualDensity.STANDARD] and
            style's [`visual_density`][flet.ButtonStyle.visual_density] is
            set to [`VisualDensity.COMPACT`][flet.VisualDensity.COMPACT], the icon
            button will have [`VisualDensity.STANDARD`][flet.VisualDensity.STANDARD]
            to define the button's layout.
    """

    autofocus: bool = False
    """
    Whether this control will be provided initial focus. If there is more than
    one control on a page with autofocus set, then the first one added to the page will
    get focus.
    """

    disabled_color: Optional[ColorValue] = None
    """
    The color to use for the icon inside the
    button when disabled.
    """

    hover_color: Optional[ColorValue] = None
    """
    The color of this button when hovered.
    """

    focus_color: Optional[ColorValue] = None
    """
    The color of this button when in focus.
    """

    splash_color: Optional[ColorValue] = None
    """
    The primary color of the button when the
    button is in the down (pressed) state.
    """

    splash_radius: Optional[Number] = None
    """
    The splash radius.

    Note:
        This value is honoured only when in Material 2
        ([`Theme.use_material3`][flet.Theme.use_material3] is `False`).
    """

    alignment: Optional[Alignment] = None
    """
    Defines how the icon is positioned within the IconButton. Alignment is an instance
    of [`Alignment`][flet.Alignment] class.

    Defaults to [`Alignment.CENTER`][flet.Alignment.CENTER].
    """

    padding: Optional[PaddingValue] = None
    """
    Defines the padding around this button. The entire padded icon will react to input
    gestures.

    Defaults to `Padding.all(8)`.
    """

    enable_feedback: Optional[bool] = None
    """
    Whether detected gestures should provide acoustic and/or haptic feedback.
    On Android, for example, setting this to `True` produce a click sound and a
    long-press will produce a short vibration.
    """

    url: Optional[Union[str, Url]] = None
    """
    The URL to open when this button is clicked.

    Additionally, if [`on_click`][flet.IconButton.on_click] event callback is provided,
    it is fired after that.
    """

    mouse_cursor: Optional[MouseCursor] = field(default=None, metadata={"skip": True})
    """
    The cursor to be displayed when a mouse pointer enters or is hovering over this
    control.
    """

    visual_density: Optional[VisualDensity] = field(
        default=None, metadata={"skip": True}
    )
    """
    Defines how compact the control's layout will be.
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    Size constraints for this button.
    """

    on_click: Optional[ControlEventHandler["IconButton"]] = None
    """
    Called when a user clicks this button.
    """

    on_focus: Optional[ControlEventHandler["IconButton"]] = None
    """
    Called when the control has received focus.
    """

    on_blur: Optional[ControlEventHandler["IconButton"]] = None
    """
    Called when the control has lost focus.
    """

    def before_update(self):
        super().before_update()
        assert self.splash_radius is None or self.splash_radius > 0, (
            f"splash_radius must be greater than 0, got {self.splash_radius}"
        )
        if (
            self.style is not None
            or self.bgcolor is not None
            or self.visual_density is not None
            or self.mouse_cursor is not None
        ):
            self._internals["style"] = (self.style or ButtonStyle()).copy(
                bgcolor=self.bgcolor,
                visual_density=self.visual_density,
                mouse_cursor=self.mouse_cursor,
            )

    async def focus(self):
        """
        Moves focus to this button.
        """
        await self._invoke_method("focus")


@control("FilledIconButton")
class FilledIconButton(IconButton):
    """
    A filled variant of [`IconButton`][flet.IconButton].

    Filled icon buttons have higher visual impact and should be used for high emphasis
    actions, such as turning off a microphone or camera.
    """


@control("FilledTonalIconButton")
class FilledTonalIconButton(IconButton):
    """
    A filled tonal variant of [`IconButton`][flet.IconButton].

    Filled tonal icon buttons are a middle ground between filled and
    outlined icon buttons. They're useful in contexts where the button requires
    slightly more emphasis than an outline would give, such as a secondary action
    paired with a high emphasis action.
    """


@control("OutlinedIconButton")
class OutlinedIconButton(IconButton):
    """
    An outlined variant of [`IconButton`][flet.IconButton].

    Outlined icon buttons are medium-emphasis buttons.
    They're useful when an icon button needs more emphasis than a
    standard icon button but less than a filled or filled tonal icon button.
    """
