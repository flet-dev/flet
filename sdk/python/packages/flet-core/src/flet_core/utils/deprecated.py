import functools
import warnings


def deprecated(reason, version, delete_version):
    def decorator(func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            warnings.warn(
                f"Call to {func.__name__}() is deprecated in version {version}. {reason} "
                f"It will be removed in version {delete_version}.",
                category=DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        return new_func

    return decorator
