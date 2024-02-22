import asyncio


class blocking(object):
    def __init__(self, fn=None, pool=None):
        self.fn = fn
        self.pool = pool

    async def __call__(self, *args, **kwargs):
        assert self.fn
        return asyncio.get_running_loop().run_in_executor(self.pool, self.fn, *args)
