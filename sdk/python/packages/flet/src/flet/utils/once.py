import asyncio


class Once:
    """
    Async helper that runs a coroutine function only once.

    Concurrent callers are synchronized with an [`asyncio.Lock`][asyncio.Lock] so the
    wrapped function executes at most one time per [`Once`][(c)] instance.
    """

    def __init__(self):
        self._lock = asyncio.Lock()
        self._done = False

    async def do(self, func, *args, **kwargs):
        """
        Executes `func` exactly once for this instance.

        If another coroutine has already completed the call, this method returns
        immediately without invoking `func`.

        Args:
            func: Async callable to run once.
            *args: Positional arguments passed to `func`.
            **kwargs: Keyword arguments passed to `func`.

        Raises:
            Exception: Propagates any exception raised by `func`.
        """
        if not self._done:
            async with self._lock:
                if not self._done:
                    await func(*args, **kwargs)
                    self._done = True
