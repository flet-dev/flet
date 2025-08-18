import functools
import hashlib
import weakref
from typing import Callable, Optional, ParamSpec, TypeVar, overload

P = ParamSpec("P")
R = TypeVar("R")


def _hash_args(*args, **kwargs):
    try:
        # Convert args/kwargs to a string and hash it
        sig = repr((args, kwargs))
        return hashlib.sha256(sig.encode()).hexdigest()
    except Exception:
        # fallback to id-based hash if unhashable
        return str(id(args)) + str(id(kwargs))


def _freeze_controls(control):
    if isinstance(control, list):
        return [_freeze_controls(c) for c in control]
    elif isinstance(control, dict):
        return {k: _freeze_controls(v) for k, v in control.items()}
    elif hasattr(control, "__dict__"):  # assume it's a control
        object.__setattr__(control, "_frozen", True)
    return control


@overload
def cache(
    _fn: None = ..., *, freeze: bool = False
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...
@overload
def cache(_fn: Callable[P, R], *, freeze: bool = False) -> Callable[P, R]: ...


def cache(_fn: Optional[Callable[P, R]] = None, *, freeze: bool = False):
    """
    A decorator to cache the results of a function based on its arguments.
    Used with Flet controls to optimize comparisons in declarative apps.

    Args:
        _fn: The function to be decorated.
            If None, the decorator is used with arguments.
        freeze: If `True`, freezes the returned controls
            by setting a `_frozen` attribute.

    Returns:
        A decorated function that caches its results.
    """

    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        # Use a weak reference dictionary to store cached results
        cache_store = weakref.WeakValueDictionary()

        @functools.wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # Generate a unique hash key based on the function arguments
            key = _hash_args(*args, **kwargs)

            # Return cached result if it exists
            if key in cache_store:
                return cache_store[key]

            # Call the original function and cache the result
            result = fn(*args, **kwargs)
            if result is not None:
                if freeze:
                    # Freeze the controls if the freeze flag is set
                    _freeze_controls(result)
                cache_store[key] = result
            elif key in cache_store:
                # Remove the cache entry if the result is None
                del cache_store[key]
            return result

        return wrapper

    # If _fn is None, return the decorator itself for use with arguments
    if _fn is None:
        return decorator
    else:
        # Apply the decorator directly if _fn is provided
        return decorator(_fn)
