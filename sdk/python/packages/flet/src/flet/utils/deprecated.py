import functools
import warnings


def deprecated(reason: str, version: str, delete_version: str, is_method=True):
    """
    A decorator function that marks a function/method/property/event as deprecated.

    :param reason: The reason for deprecation.
    :param version: The version from which the function was deprecated.
    :param delete_version: The version in which the function will be removed from the API.
    :param is_method: if the deprecated item is a method (True) or property/function/event (False)
    """

    def decorator(func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            warnings.warn(
                f"{func.__name__}{'()' if is_method else ''} is deprecated in version {version} "
                f"and will be removed in version {delete_version}. {reason}",
                category=DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        return new_func

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
