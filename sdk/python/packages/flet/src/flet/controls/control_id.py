import itertools
import threading

from flet.utils.locks import NopeLock
from flet.utils.platform_utils import is_pyodide


class ControlId:
    """
    Generates unique, auto-incrementing integers safely across
    multiple threads and asyncio tasks using itertools.count.
    """

    _counter_iterator = itertools.count(3)  # Creates an iterator starting at 3
    _lock = threading.Lock() if not is_pyodide() else NopeLock()

    @classmethod
    def next(cls) -> int:
        """Returns the next unique integer identifier."""
        with cls._lock:
            # next() on the iterator is atomic *relative to the lock*
            return next(cls._counter_iterator)
