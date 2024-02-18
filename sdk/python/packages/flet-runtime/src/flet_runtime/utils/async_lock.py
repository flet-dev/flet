import asyncio
import concurrent.futures
import contextlib


@contextlib.asynccontextmanager
async def async_lock(lock):
    await asyncio.get_event_loop().run_in_executor(None, lock.acquire)
    try:
        yield  # the lock is held
    finally:
        lock.release()
