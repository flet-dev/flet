from dataclasses import field
from typing import Optional

import flet as ft

__all__ = ["PieChartSection"]


@ft.control("PieChartSection")
class PieChartSection(ft.BaseControl):
    """
    Configures a [PieChart][(p).] section.

    Raises:
        AssertionError: If [`title_position`][(c).] or
            [`badge_position`][(c).] is not between `0.0` and `1.0` inclusive.
    """

    value: ft.Number
    """
    Determines how much the section should occupy. This depends on sum of all sections,
    each section should occupy (`value` / sum of all values) * `360` degrees.
    """

    radius: Optional[ft.Number] = None
    """
    External radius of the section.
    """

    color: Optional[ft.ColorValue] = None
    """
    Background color of the section.
    """

    border_side: ft.BorderSide = field(default_factory=lambda: ft.BorderSide.none())
    """
    The border around section shape.
    """

    title: Optional[str] = None
    """
    A title drawn at the center of the section.
    """

    title_style: Optional[ft.TextStyle] = None
    """
    The style to draw `title` with.
    """

    title_position: Optional[ft.Number] = None
    """
    The position/offset of the title relative to the section's center.

    By default the title is drawn in the middle of the section.

    Note:
        Must be between `0.0` (near the center)
        and `1.0`(near the outside of the chart) inclusive.
    """

    badge: Optional[ft.Control] = None
    """
    An optional `Control` drawn in the middle of a section.
    """

    badge_position: Optional[ft.Number] = None
    """
    The position/offset of the badge relative to the section's center.

    By default the badge is drawn in the middle of the section.

    Note:
        Must be between `0.0` (near the center)
        and `1.0`(near the outside of the chart) inclusive.
    """

    gradient: Optional[ft.Gradient] = None
    """
    Defines the gradient of section. If specified, overrides the color setting.
    """

    def before_update(self):
        super().before_update()
        assert self.title_position is None or (0.0 <= self.title_position <= 1.0), (
            f"title_position must be between 0.0 and 1.0 inclusive, "
            f"got {self.title_position}"
        )
        assert self.badge_position is None or (0.0 <= self.badge_position <= 1.0), (
            f"badge_position must be between 0.0 and 1.0 inclusive, "
            f"got {self.badge_position}"
        )
