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
    A decorator that marks a function, method, or class as deprecated.

    :param reason: The reason for deprecation.
    :param version: (Optional) The version from which the function was deprecated.
    :param delete_version: (Optional) The version in which the function will be removed.
    :param show_parentheses: Whether to show parentheses after the function/class name in the warning.
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
        msg = f"{cls.__name__} is deprecated since version {version} and will be removed in version {delete_version}. {reason}"

        # Wrap the original __init__ method
        orig_init = cls.__init__

        @functools.wraps(orig_init)
        def new_init(self, *args, **kwargs):
            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
            orig_init(self, *args, **kwargs)

        cls.__init__ = new_init
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

    :param name: The name of the deprecated object.
    :param reason: A short explanation of why the object is deprecated and/or what to use instead.
    :param version: The version in which the object was marked as deprecated.
    :param delete_version: Optional; the version in which the object is scheduled to be removed.
    :param type: The type of the object being deprecated (e.g., "property"). Defaults to "property".
    """
    warnings.warn(
        f"{name} {type} is deprecated since version {version}"
        f"{' and will be removed in version ' + delete_version if delete_version else ''}. {reason}",
        category=DeprecationWarning,
        stacklevel=2,
    )
