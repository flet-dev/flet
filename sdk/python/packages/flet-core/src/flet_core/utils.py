import asyncio
import inspect
import random
import string


def random_string(length):
    return "".join(random.choice(string.ascii_letters) for i in range(length))


def is_asyncio():
    try:
        return asyncio.current_task() is not None
    except RuntimeError:
        return False


def is_coroutine(method):
    return inspect.iscoroutinefunction(method)
