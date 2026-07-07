---
title: "Multiprocessing"
---

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
in packaged desktop apps [built](../publish/index.md) with `flet build macos`, `flet build windows`, or
`flet build linux` when using [Flet v0.86.0](https://github.com/flet-dev/flet/releases/tag/v0.86.0) or newer.

It is **not supported on iOS and Android** (mobile operating systems don't
allow apps to spawn arbitrary child processes) or **in the browser**. On those
platforms, prefer threads or `asyncio` instead.
:::

## Rules

These are standard Python `multiprocessing` rules — but in a packaged Flet app
they are **mandatory**, not just good style.

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

## How does it work?

In a desktop app packaged with `flet build`, there is no separate `python` executable —
the interpreter is embedded inside your app's binary. When `multiprocessing` spawns a
worker, it re-executes that binary with a CPython helper command line; the binary
recognizes that shape and services it as a plain, windowless Python interpreter.
This also covers multiprocessing's helper processes (the resource tracker and the `forkserver`).

A few practical consequences and notes:

- [`sys.executable`](https://docs.python.org/3/library/sys.html#sys.executable) in a packaged app points at your app's binary, not a
  `python` executable. That is intentional — don't override it with
  [`multiprocessing.set_executable()`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.set_executable).
- You usually do not need [`multiprocessing.freeze_support()`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.freeze_support) in Flet apps.
  Calling it inside the `if __name__ == "__main__":` block is harmless, but Flet
  does not rely on PyInstaller-style frozen-executable bootstrapping.
- Worker `print()` output is not connected to your app's console log; use a
  [`Queue`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue) or file-based logging if you need worker diagnostics.
- On Linux, avoid forcing the `fork` start method: your app's process runs the
  Flutter engine with many active threads, and forking it is unsafe. Prefer the
  platform default (`forkserver`/`spawn`), or request one explicitly with
  `multiprocessing.get_context("spawn")`.

## Examples

### Parallel sort with live progress

Sort chunks of data across all CPU cores and stream progress to the page:

```python
from concurrent.futures import ProcessPoolExecutor, as_completed

import flet as ft
import random

def sort_chunk(chunk: list[float]) -> list[float]:
    return sorted(chunk)


def main(page: ft.Page):
    def run_sort():
        chunks = [
            [random.random() for _ in range(250_000)]
            for _ in range(8)
        ]
        completed = 0
        with ProcessPoolExecutor() as pool:
            futures = [pool.submit(sort_chunk, c) for c in chunks]
            for _ in as_completed(futures):
                completed += 1
                progress.value = completed / len(futures)
                status.value = f"Sorted {completed}/{len(futures)} chunks"
                page.update()
        status.value = "Done!"
        page.update()

    page.add(
        ft.Button("Start sorting", on_click=lambda _: page.run_thread(run_sort)),
        status := ft.Text("Idle"),
        progress := ft.ProgressBar(value=0, width=300),
    )


if __name__ == "__main__":
    ft.run(main)
```

Note how the long-running orchestration is moved off the UI event handler with
[`page.run_thread`](async-apps.md#threading), while the CPU-heavy work runs in the
process pool. The worker function may live in your main module (as above) or in
a separate importable module — both work.
