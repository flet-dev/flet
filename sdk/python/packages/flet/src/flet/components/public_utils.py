from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from flet.components.component import Component

# Cached lazily on first call so merely importing this helper (done by Page /
# BasePage) doesn't pull the whole components subsystem into the cold-start
# import graph for apps that don't use components.
_Component: "Optional[type[Component]]" = None


def unwrap_component(c: Any):
    """
    Resolves a component wrapper chain to its rendered payload.

    If `c` is a `Component`, this function repeatedly follows
    its rendered body (`_b`) until the value is no longer a `Component`.

    Args:
        c: A value that may be a component wrapper or an already unwrapped value.

    Returns:
        The first non-`Component` value in the chain (for example a control,
            list of controls/views, or `None`).
    """
    global _Component
    if _Component is None:
        from flet.components.component import Component

        _Component = Component
    p = c
    while isinstance(p, _Component):
        p = p._b
    return p
