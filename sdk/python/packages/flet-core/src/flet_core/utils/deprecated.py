import functools
import warnings


def deprecated(reason, version, delete_version):
    """
    A decorator function that marks a function as deprecated.

    :param reason: The reason for deprecation.
    :param version: The version from which the function was deprecated.
    :param delete_version: The version in which the function will be removed from the API.
    """

    def decorator(func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            warnings.warn(
                f"Call to {func.__name__}() is deprecated since version {version} "
                f"and will be removed in version {delete_version}. {reason}",
                category=DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        return new_func

    return decorator
