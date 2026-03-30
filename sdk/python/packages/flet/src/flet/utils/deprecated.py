"""
Utilities for runtime deprecation warnings in Flet.

This module provides:
- decorator-based warnings for functions/methods/classes;
- class-constructor warnings for deprecated classes;
- direct warning helper used by validation rules.
"""

import functools
import sys
import warnings
from typing import Any, Callable, Optional, TypeVar

__all__ = ["deprecated", "deprecated_class", "deprecated_warning"]

_FuncT = TypeVar("_FuncT", bound=Callable[..., Any])
_ClassT = TypeVar("_ClassT", bound=type[Any])


def _resolve_user_stacklevel(default: int = 2) -> int:
    """
    Return a `warnings.warn` stacklevel that points outside `flet.*` internals.

    This keeps deprecation warnings attributed to user code by default, so they
    are visible without requiring explicit warning filter configuration.
    """

    try:
        frame = sys._getframe(1)
    except Exception:
        return default

    stacklevel = 1
    while frame is not None:
        module_name = frame.f_globals.get("__name__", "")
        if module_name != "flet" and not module_name.startswith("flet."):
            return stacklevel
        frame = frame.f_back
        stacklevel += 1

    return default


def _warn_deprecation(message: str) -> None:
    """Emit a `DeprecationWarning` attributed to user code when possible."""
    warnings.warn(
        message,
        category=DeprecationWarning,
        stacklevel=_resolve_user_stacklevel(),
    )


def deprecated(
    reason: str,
    version: Optional[str] = None,
    delete_version: Optional[str] = None,
    show_parentheses: bool = False,
    docs_reason: Optional[str] = None,
) -> Callable[[_FuncT], _FuncT]:
    """
    Marks a function, method, or class as deprecated.

    Args:
        reason: The reason for deprecation.
        version: The version from which the function was deprecated.
        delete_version: The version in which the function will be removed.
        show_parentheses: Whether to show parentheses after the function/class name
            in the warning.
        docs_reason: Optional docs-only reason. This value is ignored at runtime
            and is consumed by docs tooling when available.
    """
    _ = docs_reason  # Consumed by docs tooling; runtime warnings use `reason`.

    def decorator(func: _FuncT) -> _FuncT:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            msg = f"{func.__name__}{'()' if show_parentheses else ''} is deprecated"
            if version:
                msg += f" since version {version}"
            if delete_version:
                msg += f" and will be removed in version {delete_version}"
            msg += f". {reason}"
            _warn_deprecation(msg)
            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator


def deprecated_class(
    reason: str,
    version: str,
    delete_version: str,
    docs_reason: Optional[str] = None,
) -> Callable[[_ClassT], _ClassT]:
    """
    Marks a class as deprecated.

    Args:
        reason: The reason for deprecation used in runtime warnings.
        version: The version from which the class is deprecated.
        delete_version: The version in which the class will be removed.
        docs_reason: Optional docs-only reason. This value is ignored at runtime
            and is consumed by docs tooling when available.
    """
    _ = docs_reason  # Consumed by docs tooling; runtime warnings use `reason`.

    def decorator(cls: _ClassT) -> _ClassT:
        msg = (
            f"{cls.__name__} is deprecated since version {version} and will be removed "
            f"in version {delete_version}. {reason}"
        )

        # Wrap the original __init__ method
        orig_init = cls.__init__

        @functools.wraps(orig_init)
        def new_init(self, *args, **kwargs):
            _warn_deprecation(msg)
            orig_init(self, *args, **kwargs)

        cls.__init__ = new_init

        # Wrap the original __post_init__ method
        orig_post_init = cls.__post_init__

        @functools.wraps(orig_post_init)
        def new_post_init(self, *args, **kwargs):
            _warn_deprecation(msg)
            orig_post_init(self, *args, **kwargs)

        cls.__post_init__ = new_post_init

        return cls

    return decorator


def deprecated_warning(
    name: str,
    reason: str,
    version: str,
    delete_version: Optional[str] = None,
    type: str = "property",
):
    """
    Helper function to issue a standardized deprecation warning message.

    Args:
        name: The name of the deprecated object.
        reason: A short explanation of why the object is deprecated and/or what to
            use instead.
        version: The version in which the object was marked as deprecated.
        delete_version: The version in which the object is scheduled to be
            removed (optional).
        type: The type of the object being deprecated (e.g., "property").
            Defaults to "property".
    """
    delete_version_text = (
        f" and will be removed in version {delete_version}" if delete_version else ""
    )
    _warn_deprecation(
        f"{name} {type} is deprecated since version {version}{delete_version_text}. "
        f"{reason}"
    )
