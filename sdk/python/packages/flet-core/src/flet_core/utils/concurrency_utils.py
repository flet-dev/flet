import asyncio
import inspect
import sys


def is_asyncio():
    try:
        return asyncio.current_task() is not None or sys.platform == "emscripten"
    except RuntimeError:
        return False


def is_coroutine(method):
    return inspect.iscoroutinefunction(method)
