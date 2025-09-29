import itertools
import threading
from typing import Optional

from flet.utils.locks import NopeLock
from flet.utils.platform_utils import is_pyodide


class IdCounter:
    def __init__(
        self, start: int = 1, step: int = 1, lock: Optional[threading.Lock] = None
    ):
        self._counter = itertools.count(start, step)
        self._lock = lock or (NopeLock() if is_pyodide() else threading.Lock())

    def next(self) -> int:
        with self._lock:
            return next(self._counter)

    def __call__(self) -> int:  # for dataclass default_factory
        return self.next()


ControlId = IdCounter(start=3)
