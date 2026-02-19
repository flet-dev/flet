from typing import Any

from flet.components.component import Component


def unwrap_component(c: Any):
    """
    Resolves a component wrapper chain to its rendered payload.

    If `c` is a [`Component`][flet.], this function repeatedly follows
    its rendered body (`_b`) until the value is no longer a `Component`.

    Args:
        c: A value that may be a component wrapper or an already unwrapped value.

    Returns:
        The first non-`Component` value in the chain (for example a control,
            list of controls/views, or `None`).
    """
    p = c
    while isinstance(p, Component):
        p = p._b
    return p
