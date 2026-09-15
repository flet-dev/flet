---
title: "Async apps"
---

A Flet app runs on a single [asyncio](https://docs.python.org/3/library/asyncio.html)
event loop. Coroutines are supported everywhere a handler is accepted, so you can
use `asyncio` and any async Python library without wrapping anything.

That single loop is also what sends UI updates to the client, which leads to the
one rule that matters most:

:::warning[Never block the event loop]
While your handler runs, nothing else does - no other events are dispatched, and
no updates reach the screen. A blocking call such as `time.sleep()` or
`requests.get()` freezes the UI for as long as it takes.

This applies on every platform, not just the web.
:::

If you are coming from Flet 0.28, where sync handlers ran on a thread pool, read
[Migrating from Flet 0.28 to 1.0](../updates/migrate-to-1-0.md#step-3-your-app-runs-on-one-thread-now)
first - this is the behavior that changed.

## Getting started with async

`main()` can be `async` and use any asyncio API:

```python
import asyncio

import flet as ft

async def main(page: ft.Page):
    await asyncio.sleep(1)
    page.add(ft.Text("Hello, async world!"))

ft.run(main)
```

Use `await ft.run_async(main)` when your Flet app is part of a larger app and
started from async code.

## Control event handlers

Handlers can be sync or async, and Flet picks the right calling convention for
each. A sync handler is fine when it does not block:

```python
def handle_resize(e):
    print("New page size:", page.window.width, page.window.height)

page.on_resize = handle_resize
```

Make it `async` when there is something to `await`:

```python
async def main(page: ft.Page):
    async def handle_click(e):
        await some_async_method()
        page.add(ft.Text("Hello!"))

    page.add(ft.Button(content="Say hello!", on_click=handle_click))

ft.run(main)
```

A handler can also take no arguments at all, which is convenient when you do not
need the event:

```python
def handle_click():
    counter.value += 1

ft.Button(content="Add", on_click=handle_click)
```

### Async lambdas

Python has no async lambdas. A lambda handler is fine for simple, non-blocking
work:

```python
page.on_error = lambda e: print("Page error:", e.data)
```

A lambda can still *start* async work. Handlers run on the event loop, so there is
always a running loop to schedule a task on - the lambda kicks the coroutine off
instead of awaiting it:

```python
ft.Button(content="Reload", on_click=lambda e: asyncio.create_task(reload(e)))
```

[`page.run_task()`][flet.Page.run_task] is usually the better version of this
trick. It takes the coroutine function and its arguments rather than a called
coroutine, keeps a reference to the task so it cannot be garbage-collected
mid-flight, and reports exceptions through Flet's error handling instead of
discarding them:

```python
ft.Button(content="Reload", on_click=lambda e: page.run_task(reload, e))
```

:::warning[The handler finishes before the task does]
Scheduling a task ends the handler immediately, so the automatic update happens
while your coroutine is still running and will not include anything it does. Call
`update()` yourself for UI changes made inside the task:

```python
async def reload(e):
    items.value = await fetch_items()
    items.update()  # the handler's automatic update already happened
```
:::

For anything longer than scheduling one call, use an `async def` handler.

### Sleeping

Use [`asyncio.sleep()`](https://docs.python.org/3/library/asyncio-task.html#asyncio.sleep)
rather than `time.sleep()`, which blocks the loop:

```python
import asyncio

import flet as ft

def main(page: ft.Page):
    async def handle_click(e):
        await asyncio.sleep(1)
        page.add(ft.Text("Hello!"))

    page.add(ft.Button(content="Say hello with delay!", on_click=handle_click))

ft.run(main)
```

### Yielding for intermediate updates

Updates are sent after a handler finishes. To show progress part-way through, make
the handler a generator - each `yield` flushes pending updates and gives the loop
a chance to run:

```python
def handle_click(e):
    for i in range(10):
        do_chunk(i)
        progress.value = (i + 1) / 10
        yield
```

The work still runs on the event loop, so keep each chunk short. For heavy chunks,
offload them instead (see below).

## Background tasks

Use [`page.run_task()`][flet.Page.run_task] to start a coroutine that outlives the
handler that created it. For example, a self-updating countdown control:

```python
import asyncio

import flet as ft

@ft.control
class Countdown(ft.Text):
    seconds: int = 60

    def did_mount(self):
        self._task = self.page.run_task(self.update_timer)

    def will_unmount(self):
        self._task.cancel()

    async def update_timer(self):
        while self.seconds:
            mins, secs = divmod(self.seconds, 60)
            self.value = f"{mins:02d}:{secs:02d}"
            self.update()
            await asyncio.sleep(1)
            self.seconds -= 1

def main(page: ft.Page):
    page.add(Countdown(seconds=120), Countdown(seconds=60))

ft.run(main)
```

Pass the coroutine **function**, not a called coroutine - `page.run_task(self.update_timer)`,
not `page.run_task(self.update_timer())`. It raises `TypeError` otherwise.

`run_task()` returns a future, so the control can cancel its own work in
`will_unmount()`, as above. `did_mount()` and `will_unmount()` are sync, which is
why background work is started with `run_task()` rather than awaited there.

## Threading

Some libraries have no async version. To keep a blocking call off the loop, run it
in a thread.

| Use | When |
|---|---|
| `await asyncio.to_thread(fn, *args)` | you need the result back |
| [`page.run_thread(fn, *args)`][flet.Page.run_thread] | fire-and-forget |
| `page.loop.run_in_executor(pool, fn)` | you want your own pool |

`asyncio.to_thread()` is the usual choice:

```python
async def handle_click(e):
    response = await asyncio.to_thread(requests.get, "https://api.example.com/items")
    output.value = response.text
```

[`page.run_thread()`][flet.Page.run_thread] does not return a result, but it
re-establishes the page context inside the thread and runs its callable inline on
the web, where there are no threads:

```python
def handle_click(e):
    page.run_thread(write_log_file, "clicked")
```

For your own pool - to bound how many operations run at once, for example - use
[`page.loop`][flet.Page.loop] with an executor you control:

```python
pool = ThreadPoolExecutor(max_workers=2)

async def handle_click(e):
    await page.loop.run_in_executor(pool, transcode, path)
```

Flet's own shared pool is available as [`page.executor`][flet.Page.executor].

## CPU-bound work

Threads keep the UI responsive but do not make pure-Python work faster: the GIL
lets only one thread run Python bytecode at a time. C extensions that release the
GIL - NumPy, Pillow, most database drivers - do parallelize in plain threads.

For pure Python that needs more than one core:

| | Runs on | Available on |
|---|---|---|
| [Subinterpreters](subinterpreters.md) | N interpreters, one process | desktop, mobile, dynamic web (Python 3.14+) |
| [Multiprocessing](multiprocessing.md) | N processes | desktop only |

Subinterpreters are the option that also works on iOS and Android, where an app
cannot spawn child processes. Multiprocessing gives full isolation and lets you
hard-cancel a worker.

To report progress from either, update the UI as futures complete:

```python
async def handle_click(e):
    done = 0
    with InterpreterPoolExecutor() as pool:
        futures = [page.loop.run_in_executor(pool, do_chunk, i) for i in range(100)]
        for future in asyncio.as_completed(futures):
            await future
            done += 1
            progress.value = done / 100
            progress.update()
```

Worker functions must be defined at module top level. See
[Subinterpreters](subinterpreters.md) for the rules and full examples.

## Platform differences

| | Threads | Subinterpreters | Multiprocessing |
|---|---|---|---|
| Desktop | ✅ | ✅ (3.14+) | ✅ |
| iOS, Android | ✅ | ✅ (3.14+) | ❌ |
| [Dynamic website](../publish/web/dynamic-website/index.md) | ✅ | ✅ (3.14+) | ✅ |
| [Static website](../publish/web/static-website/index.md) | ❌ | ❌ | ❌ |

A static website runs your app in the browser on
[Pyodide](https://pyodide.org/en/stable/), a
[single-threaded WebAssembly runtime](https://pyodide.org/en/stable/usage/wasm-constraints.html).
`asyncio.to_thread()` is not usable there and
[`page.run_thread()`][flet.Page.run_thread] runs its callable inline, so it offers
no relief from blocking.

:::warning[Long work in a static web app]
With no threads available, the only options are to chunk the work and `yield`
between chunks, use a real async library, or move the work to a server. A
[dynamic website](../publish/web/dynamic-website/index.md) runs your Python
server-side as an ordinary CPython process, so everything above applies there as
it does on desktop.
:::

:::note[PubSub subscribers]
Sync [PubSub](pub-sub.md) subscribers run on the thread pool rather than on the
event loop, so a blocking subscriber will not freeze the UI. Event handlers are
not treated this way.
:::
