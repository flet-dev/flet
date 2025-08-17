import functools
import hashlib
import weakref
from typing import Callable


# --- Utility to create a hashable signature from args ---
def _hash_args(*args, **kwargs):
    try:
        # Convert args/kwargs to a string and hash it
        sig = repr((args, kwargs))
        return hashlib.sha256(sig.encode()).hexdigest()
    except Exception:
        # fallback to id-based hash if unhashable
        return str(id(args)) + str(id(kwargs))


# --- Freeze controls in the returned structure ---
def _freeze_controls(control):
    if isinstance(control, list):
        return [_freeze_controls(c) for c in control]
    elif isinstance(control, dict):
        return {k: _freeze_controls(v) for k, v in control.items()}
    elif hasattr(control, "__dict__"):  # assume it's a control
        object.__setattr__(control, "_frozen", True)
    return control


# --- Main decorator with `freeze` option ---
def cache(_fn=None, *, freeze: bool = False):
    def decorator(fn: Callable):
        cache_store = weakref.WeakValueDictionary()

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            key = _hash_args(*args, **kwargs)

            if key in cache_store:
                return cache_store[key]

            result = fn(*args, **kwargs)
            if result is not None:
                if freeze:
                    _freeze_controls(result)
                cache_store[key] = result
            elif key in cache_store:
                del cache_store[key]
            return result

        return wrapper

    if _fn is None:
        return decorator
    else:
        return decorator(_fn)
