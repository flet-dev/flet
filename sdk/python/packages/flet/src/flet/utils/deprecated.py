import functools
import warnings
from typing import TypeVar, Any, Type, Optional, Callable

def warn_deprecated(
    name: str,
    version: str,
    delete_version: Optional[str] = None,
    reason: Optional[str] = None
) -> None:
    delete_version_message = f" and will be removed in version {delete_version}" if delete_version else ""
    reason_message = " " + reason if reason else ""
    msg = f"{name} is deprecated since version {version}{delete_version_message}.{reason_message}"

    warnings.warn(
        msg,
        category=DeprecationWarning,
        stacklevel=2,
    )

F = TypeVar('F', bound=Callable[..., Any])
T = TypeVar('T')

def deprecated(
    reason: str,
    version: str,
    delete_version: Optional[str] = None,
    is_method: bool = True,
) -> Callable[[F], F]:
    """
    A decorator function that marks a function/method/property/event as deprecated.

    :param reason: The reason for deprecation.
    :param version: The version from which the function was deprecated.
    :param delete_version: The version in which the function will be removed from the API.
    :param is_method: if the deprecated item is a method (True) or property/function/event (False).
    :return: A decorator that wraps the function/method/property/event and emits a deprecation warning.
    """

    def decorator(func: F):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            warn_deprecated(
                name=f"{func.__name__}{'()' if is_method else ''}",
                version=version,
                delete_version=delete_version,
                reason=reason
            )
            return func(*args, **kwargs)

        return new_func

    return decorator


def deprecated_class(
    reason: str,
    version: str,
    delete_version: Optional[str] = None,
) -> Callable[[Type[T]], Type[T]]:
    """
    A decorator that marks a class as deprecated.

    :param reason: The reason for deprecation.
    :param version: The version from which the class was deprecated.
    :param delete_version: The version in which the class will be removed.
    :return: A decorator that wraps the class and emits a deprecation warning.
    """
    def decorator(cls):
        # Wrap the original __init__ method
        orig_init = cls.__init__

        @functools.wraps(orig_init)
        def new_init(self, *args, **kwargs):
            warn_deprecated(
                name=cls.__name__,
                version=version,
                delete_version=delete_version,
                reason=reason
            )
            orig_init(self, *args, **kwargs)

        cls.__init__ = new_init
        return cls

    return decorator


def deprecated_property(
    name: str,
    reason: str,
    version: str,
    delete_version: Optional[str] = None,
) -> None:
    warn_deprecated(
        name=f'{name} property',
        version=version,
        delete_version=delete_version,
        reason=reason
    )
