from dataclasses import dataclass
from typing import Optional

import flet as ft

__all__ = ["ImageSourceAttribution", "SourceAttribution", "TextSourceAttribution"]


@dataclass
class SourceAttribution(ft.BaseControl):
    """
    Abstract class for source attribution controls:

    - [`ImageSourceAttribution`][(p).]
    - [`TextSourceAttribution`][(p).]
    """


@ft.control("ImageSourceAttribution")
class ImageSourceAttribution(SourceAttribution):
    """
    An image attribution permanently displayed adjacent to the
    open/close icon of a [`RichAttribution`][(p).] control.
    For it to be displayed, it should be part of a
    [`RichAttribution.attributions`][(p).] list.
    """

    image: ft.Image
    """
    The [`Image`][flet.] to be displayed.

    Raises:
        ValueError: If the image is not visible.
    """

    height: ft.Number = 24.0
    """
    The height of the image.
    Should be the same as [`RichAttribution.permanent_height`][(p).],
    otherwise layout issues may occur.
    """

    tooltip: Optional[str] = None
    """Tooltip text to be displayed when the image is hovered over."""

    on_click: Optional[ft.ControlEventHandler["ImageSourceAttribution"]] = None
    """Fired when this attribution is clicked/pressed."""

    def before_update(self):
        super().before_update()
        if not self.image.visible:
            raise ValueError("image must be visible")


@ft.control("TextSourceAttribution")
class TextSourceAttribution(SourceAttribution):
    """
    A text source attribution displayed on the Map.
    For it to be displayed, it should be part of a
    [`RichAttribution.attributions`][(p).] list.
    """

    text: str
    """The text to display as attribution, styled with [`text_style`][(c).]."""

    text_style: Optional[ft.TextStyle] = None
    """Style used to display the [`text`][(c).]."""

    prepend_copyright: bool = True
    """
    Whether to add the '©' character to the start of [`text`][(c).] automatically.
    """

    on_click: Optional[ft.ControlEventHandler["TextSourceAttribution"]] = None
    """Fired when this attribution is clicked/pressed."""
