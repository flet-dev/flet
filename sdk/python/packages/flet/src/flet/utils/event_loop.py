import asyncio

running_loop = asyncio._get_running_loop
"""
Returns the event loop running in the calling thread, or `None` if there's none.

Unlike `asyncio.get_running_loop()`, it doesn't raise when there's none, which makes
it cheap enough for hot paths such as `set_state`.
"""
