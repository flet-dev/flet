import asyncio


class Once:
    def __init__(self):
        self._lock = asyncio.Lock()
        self._done = False

    async def do(self, func, *args, **kwargs):
        if not self._done:
            async with self._lock:
                if not self._done:
                    await func(*args, **kwargs)
                    self._done = True
