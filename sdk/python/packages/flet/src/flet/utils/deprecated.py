import functools
import warnings
from typing import Optional

__all__ = ["deprecated", "deprecated_class", "deprecated_warning"]


def deprecated(
    reason: str,
    version: Optional[str] = None,
    delete_version: Optional[str] = None,
    show_parentheses: bool = False,
):
    """
    Marks a function, method, or class as deprecated.

    Args:
        reason: The reason for deprecation.
        version: The version from which the function was deprecated.
        delete_version: The version in which the function will be removed.
        show_parentheses: Whether to show parentheses after the function/class name
            in the warning.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            msg = f"{func.__name__}{'()' if show_parentheses else ''} is deprecated"
            if version:
                msg += f" since version {version}"
            if delete_version:
                msg += f" and will be removed in version {delete_version}"
            msg += f". {reason}"

            warnings.warn(
                msg,
                category=DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def deprecated_class(reason: str, version: str, delete_version: str):
    def decorator(cls):
        msg = (
            f"{cls.__name__} is deprecated since version {version} and will be removed "
            f"in version {delete_version}. {reason}"
        )

        # Wrap the original __init__ method
        orig_init = cls.__init__

        @functools.wraps(orig_init)
        def new_init(self, *args, **kwargs):
            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
            orig_init(self, *args, **kwargs)

        cls.__init__ = new_init

        # Wrap the original __post_init__ method
        orig_post_init = cls.__post_init__

        @functools.wraps(orig_post_init)
        def new_post_init(self, *args, **kwargs):
            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
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
    warnings.warn(
        f"{name} {type} is deprecated since version {version}{delete_version_text}. "
        f"{reason}",
        category=DeprecationWarning,
        stacklevel=2,
    )
