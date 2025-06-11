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


# --- Main decorator ---
def data_view(fn: Callable):
    cache = weakref.WeakValueDictionary()

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        key = _hash_args(*args, **kwargs)

        if key in cache:
            return cache[key]

        result = fn(*args, **kwargs)
        if result is not None:
            _freeze_controls(result)
            cache[key] = result
        elif key in cache:
            del cache[key]
        return result

    return wrapper
