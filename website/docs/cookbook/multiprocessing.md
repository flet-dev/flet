---
title: "Multiprocessing"
---

import {CodeExample} from '@site/src/components/crocodocs';

In this cookbook recipe, you'll learn how to use Python's built-in
[`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html) module —
including [`concurrent.futures.ProcessPoolExecutor`](https://docs.python.org/3/library/concurrent.futures.html#processpoolexecutor) —
from a Flet app, for true CPU parallelism across processes.

For I/O-bound work, or work that just needs to stay off the UI thread, prefer
[async or threads](async-apps.md) — they are lighter and work on every platform.
Reach for `multiprocessing` when you need multiple CPU cores doing Python work
at the same time (number crunching, batch processing, ML inference, etc.), or
when you need process isolation for work that may fail or need to be stopped.

:::important[Platform and Flet version support]
`multiprocessing` works in Flet desktop apps during development ([`flet run`](../cli/flet-run.md)) and
in packaged **desktop** apps built with [`flet build {macos,windows,linux}`](../cli/flet-build.md)
or [`flet debug {macos,windows,linux}`](../cli/flet-debug.md) when using [Flet v0.86.0](../updates/release-notes.md#086x) or newer.

It is **not supported on iOS and Android** (mobile operating systems don't
allow apps to spawn arbitrary child processes) or **in the browser**. On those
platforms, prefer threads or `asyncio` instead.
:::

## How does it work?

In a desktop app packaged with [`flet build`](../publish/index.md), there is no separate `python` executable —
the interpreter is embedded inside your app's binary. When `multiprocessing` spawns a
worker, it re-executes that binary with a CPython helper command line; the binary
recognizes that shape and services it as a plain, windowless Python interpreter.
This also covers multiprocessing's helper processes (the resource tracker and the `forkserver`).

## Guidelines

These are standard
[Python `multiprocessing` guidelines](https://docs.python.org/3/library/multiprocessing.html#programming-guidelines)
— but in a packaged Flet app they are **mandatory**, not just good style.

### Always guard your entry point

Start your app only under the `if __name__ == "__main__":` guard. For example:

```python
import flet as ft

def main(page: ft.Page):
    ...

if __name__ == "__main__":
    ft.run(main)
```

With the `spawn` and `forkserver` start methods, worker/helper processes need
to safely import your main module. `spawn` is the default on macOS and Windows;
`forkserver` is the default on Linux starting with Python 3.14. Without the
guard, a child process can try to start your whole app again.

### Use importable, picklable worker functions

Worker targets, arguments, and return values must be picklable so Python can
send them between processes. In practice:

* define worker functions at module top level, not inside `main()` or inside a
  button handler
* pass plain data such as numbers, strings, lists, dicts, or dataclasses
* do not pass Flet controls, `page`, database connections, open files, lambdas,
  or nested functions

Good:

```python
def sort_chunk(chunk):
    return sorted(chunk)
```

Avoid:

```python
def main(page: ft.Page):
    def sort_chunk(chunk):
        return sorted(chunk)
```

The nested version is not reliably picklable because worker processes need to
import the function by name from a module.

### Don't touch the GUI from workers

Worker processes run in a separate interpreter with no connection to your app's
page. Pass data back through [`multiprocessing.Queue`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue),
[`Pipe`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Pipe), or
[pool futures](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future),
and update the UI from the main process.

### Others

- [`sys.executable`](https://docs.python.org/3/library/sys.html#sys.executable) in a packaged app points at your app's binary, not a
  `python` executable. That is intentional — don't override it with
  [`multiprocessing.set_executable()`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.set_executable).
- You usually do not need [`multiprocessing.freeze_support()`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.freeze_support) in Flet apps.
  Calling it inside the `if __name__ == "__main__":` block is harmless, but Flet
  does not rely on PyInstaller-style frozen-executable bootstrapping.
- Worker `print()` output is not connected to your app's console log; use a
  [`Queue`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue) or file-based logging if you need worker diagnostics.
- On Linux, avoid forcing the `fork` [start method](https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods):
  your app's process runs the Flutter engine with many active threads, and forking it is unsafe.
  Prefer the platform default (usually `forkserver` or `spawn`), or request one explicitly with
  [`multiprocessing.set_start_method()`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.set_start_method)
  or [`multiprocessing.get_context()`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.get_context).
- Starting a worker costs more in a packaged app than in plain Python — each
  spawned child loads your app binary's libraries before Python takes over.
  Create pools and long-lived workers once and reuse them, rather than spawning
  per button click (see [Keep a persistent worker](#keep-a-persistent-worker) example).

## Examples

### Parallel sort with live progress

Sort chunks of data across all CPU cores and stream progress to the page:

<CodeExample path="cookbook/multiprocessing/parallel_sort.py" language="python" />

Note how the long-running orchestration is moved off the UI event handler with
[`page.run_thread`](async-apps.md#threading), while the CPU-heavy work runs in the
process pool. The worker function may live in your main module (as above) or in
a separate importable module — both work.

### Stream progress from a worker

To show fine-grained progress from inside a single long-running job, pass a
[`multiprocessing.Queue`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue)
to the worker and drain it on a background thread. The worker [`put()`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue.put)s progress
values and a `None` sentinel when it is done:

<CodeExample path="cookbook/multiprocessing/worker_progress.py" language="python" />

### Keep a persistent worker

Starting a process is not free — especially in a packaged app, where each child
loads your app binary's libraries first. For repeated jobs, start one worker
that stays alive and serves requests over a
[`Pipe`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Pipe),
paying the startup cost once. Expensive setup (loading a model, opening a
dataset) can then also happen once, in the worker:

<CodeExample path="cookbook/multiprocessing/persistent_worker.py" language="python" />

The worker is started with `daemon=True`, so it is terminated automatically
when your app exits.

### Cancel a runaway task

Threads cannot be forcefully stopped from the outside — a worker [`Process`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Process) can,
at any time, with [`terminate()`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Process.terminate).
This makes processes the right tool for jobs you may need to abort, such as
long calls into external libraries:

<CodeExample path="cookbook/multiprocessing/cancel_task.py" language="python" />

A background thread [`join()`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Process.join)s the worker and reports how it ended — normally
(exit code `0`) or via cancellation (a negative exit code).

:::info
[Python's multiprocessing guidelines](https://docs.python.org/3/library/multiprocessing.html#programming-guidelines)
recommend avoiding process termination or doing it only for processes which never use any shared resources.
:::
