class NopeLock:
    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass


class AsyncNopeLock:
    async def __aenter__(self):
        pass

    async def __aexit__(self, *args):
        pass
