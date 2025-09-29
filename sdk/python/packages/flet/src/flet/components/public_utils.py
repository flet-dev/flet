from typing import Any

from flet.components.component import Component


def unwrap_component(c: Any):
    p = c
    while isinstance(p, Component):
        p = p._b
    return p
