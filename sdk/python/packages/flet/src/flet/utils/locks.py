class NopeLock:
    """
    No-op synchronous context manager used in place of a real lock.

    This class provides the same `with` interface as a lock but performs no
    synchronization.
    """

    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass


class AsyncNopeLock:
    """
    No-op asynchronous context manager used in place of a real async lock.

    This class provides the same `async with` interface as an async lock but
    performs no synchronization.
    """

    async def __aenter__(self):
        pass

    async def __aexit__(self, *args):
        pass
