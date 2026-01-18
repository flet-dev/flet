from dataclasses import dataclass
from typing import Optional, Union

from flet.controls.base_control import BaseControl
from flet.controls.material.badge import BadgeValue
from flet.controls.material.tooltip import TooltipValue
from flet.controls.types import Number, ResponsiveNumber

__all__ = ["Control"]


@dataclass(kw_only=True)
class Control(BaseControl):
    """
    Base class for controls.

    Not meant to be used directly.
    """

    expand: Optional[Union[bool, int]] = None
    """
    Specifies whether/how this control should expand to fill available space in its
    parent layout.

    More information
    [here](https://docs.flet.dev/cookbook/expanding-controls/#expand).

    Note:
        Has effect only if the direct parent of this control is one of the following
        controls, or their subclasses: [`Column`][flet.], [`Row`][flet.],
        [`View`][flet.], [`Page`][flet.].

    Raises:
        ValueError: If [`expand`][(c).] is not `None` and not of type `bool` or `int`.
    """

    expand_loose: bool = False
    """
    Allows the control to expand along the main axis if space is available,
    but does not require it to fill all available space.

    More information
    [here](https://docs.flet.dev/cookbook/expanding-controls/#expand_loose).

    Note:
        If `expand_loose` is `True`, it will have effect only if:

        - `expand` is not `None` and
        - the direct parent of this control is one of the following controls, or their
            subclasses: [`Column`][flet.], [`Row`][flet.], [`View`][flet.],
            [`Page`][flet.].
    """

    # todo: if dict, validate keys with those in parent (ResponsiveRow.breakpoints)
    col: ResponsiveNumber = 12
    """
    If a parent of this control is a [`ResponsiveRow`][flet.],
    this property is used to determine
    how many virtual columns of a screen this control will span.

    Can be a number or a dictionary configured to have a different value for specific
    breakpoints, for example `col={"sm": 6}`.

    This control spans the 12 virtual columns by default.

    /// details | Dimensions
        type: info
    | Breakpoint | Dimension |
    |---|---|
    | xs | <576px |
    | sm | ≥576px |
    | md | ≥768px |
    | lg | ≥992px |
    | xl | ≥1200px |
    | xxl | ≥1400px |
    ///
    """

    opacity: Number = 1.0
    """
    Defines the transparency of the control.

    Value ranges from `0.0` (completely transparent) to `1.0` (completely opaque
    without any transparency).

    Raises:
        ValueError: If [`opacity`][(c).] is not between `0.0` and `1.0` inclusive.
    """

    tooltip: Optional[TooltipValue] = None
    """
    The tooltip to show when this control is hovered over.
    """

    badge: Optional[BadgeValue] = None
    """
    A badge to show on top of this control.
    """

    visible: bool = True
    """
    Every control has `visible` property which is `True` by default - control is
    rendered on the page. Setting `visible` to `False` completely prevents control (and
    all its children if any) from rendering on a page canvas. Hidden controls cannot be
    focused or selected with a keyboard or mouse and they do not emit any events.
    """

    disabled: bool = False
    """
    Every control has `disabled` property which is `False` by default - control and all
    its children are enabled.

    Note:
        The value of this property will be propagated down to all children controls
        recursively.

    /// details | Example
        type: example
    For example, if you have a form with multiple entry controls you can disable them
    all together by disabling container:

    ```python
    ft.Column(
        disabled = True,
        controls=[
            ft.TextField(),
            ft.TextField()
        ]
    )
    ```
    ///
    """

    rtl: bool = False
    """
    Whether the text direction of the control should be right-to-left (RTL).
    """

    def before_update(self):
        super().before_update()
        if not (0.0 <= self.opacity <= 1.0):
            raise ValueError(
                f"opacity must be between 0.0 and 1.0 inclusive, got {self.opacity}"
            )
        if self.expand is not None and not isinstance(self.expand, (bool, int)):
            raise ValueError(
                f"expand must be of type bool or int, got {type(self.expand)}"
            )
