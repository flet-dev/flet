from functools import wraps
from typing import Callable, ParamSpec, TypeVar

from flet.components.utils import current_renderer

P = ParamSpec("P")
R = TypeVar("R")


def component(fn: Callable[P, R]) -> Callable[P, R]:
    """
    Marks a function as a component.
    """
    fn.__is_component__ = True

    @wraps(fn)
    def component_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        key = kwargs.pop("key", None)
        r = current_renderer()
        return r.render_component(fn, args, kwargs, key=key)

    component_wrapper.__is_component__ = True
    component_wrapper.__component_impl__ = fn
    return component_wrapper
