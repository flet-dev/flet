---
title: "Subinterpreters"
---

import {CodeExample} from '@site/src/components/crocodocs';

In this cookbook recipe, you'll learn how to use Python 3.14's
[subinterpreters](https://peps.python.org/pep-0734/)
([`concurrent.interpreters`](https://docs.python.org/3/library/concurrent.interpreters.html)
and [`concurrent.futures.InterpreterPoolExecutor`](https://docs.python.org/3/library/concurrent.futures.html#interpreterpoolexecutor))
for true multi-core CPU parallelism in a Flet app.

A subinterpreter is a separate Python interpreter running **inside the same
process**. Since Python 3.12 each one has its
[own GIL](https://peps.python.org/pep-0684/), so several subinterpreters can run
pure-Python code on several CPU cores at once — without starting separate
processes.

## When to use which

| | runs on | true CPU parallelism | notes |
|---|---|---|---|
| [threads](async-apps.md#threading) | one interpreter, one GIL | ❌ (pure Python) | best for I/O, or C libraries that release the GIL |
| **subinterpreters** | one process, N interpreters | ✅ | in-process, works on mobile; restricted data sharing; can't force-cancel |
| [multiprocessing](multiprocessing.md) | N processes | ✅ | full isolation, can hard-cancel a worker; heavier, desktop-only in Flet |

Reach for subinterpreters when you need multiple cores for Python work and want
to stay in one process — especially on **mobile**, where `multiprocessing`
cannot spawn child processes at all.

:::important[Platform and version support]
Subinterpreters require **Python 3.14 or later**. When packaging your app using [`flet build`](../cli/flet-build.md),
ensure that the [bundled Python version](../publish/index.md#choosing-a-python-version) meets this requirement.
In development (e.g., when using [`flet run`](../cli/flet-run.md)), the Python interpreter in your virtual environment must also meet this requirement.

They work in Flet apps on **macOS, Windows, Linux, iOS, and Android**.

On the **web** it depends on where your Python actually runs:

- [Dynamic websites](../publish/web/dynamic-website/index.md) run your app
  server-side as an ordinary CPython process (FastAPI/Uvicorn), so
  subinterpreters work just like on desktop — as long as the **server** runs
  Python 3.14.
- [Static websites](../publish/web/static-website/index.md) run entirely in the
  browser on [Pyodide](https://pyodide.org/en/stable/index.html), a
  [single-threaded WebAssembly runtime](https://pyodide.org/en/stable/usage/wasm-constraints.html)
  with no per-interpreter GIL — so subinterpreters are **not** available there.
:::

## Rules

### Define workers at module top level

To run a worker in another interpreter, CPython **copies it there** — its code
plus the module-level functions and constants it references. Define workers at
the **top level** of a module (your `main.py`, as the examples below do, or a
separate file); both behave identically on macOS, Windows, Linux, iOS, and
Android.

A worker function **nested** inside `main()` or a button handler only works if it is
*stateless* — no captured variables and no module globals — so the moment it
references a helper or a constant it fails with `NotShareableError: only
stateless functions are shareable`. A top-level function has no such limit: it
can freely call other module-level helpers. (Also don't call a helper from inside
a generator expression — see [Caveats](#caveats).)

### Pass only picklable / shareable data

Arguments and return values are
[pickled](https://docs.python.org/3/library/pickle.html) to cross the interpreter
boundary, so they must be picklable. The low-level
[`Queue`](https://docs.python.org/3/library/concurrent.interpreters.html#concurrent.interpreters.Queue)
additionally accepts *shareable* objects directly — numbers, `str`, `bytes`,
`None`, tuples of those, and the queue itself. Don't pass Flet controls, `page`,
open files, or database connections.

### Don't touch the GUI from a subinterpreter

Workers run in an isolated interpreter with no access to your page. Return data
(or stream it through a `Queue`) and update the UI from the main interpreter.

## Examples

### Parallel map across cores

[`InterpreterPoolExecutor`](https://docs.python.org/3/library/concurrent.futures.html#interpreterpoolexecutor)
is a drop-in alternative to
[`ProcessPoolExecutor`](https://docs.python.org/3/library/concurrent.futures.html#processpoolexecutor):
it runs each task in a subinterpreter and, because each has its own GIL, uses
several cores at once — all in one process.

<CodeExample path="cookbook/subinterpreters/parallel_map.py" language="python" />

The example times the same work run sequentially and then across the pool, and
reports the speedup. Orchestration runs off the UI thread with
[`page.run_thread`](async-apps.md#threading), and parallel results are collected
as each task lands via
[`as_completed`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.as_completed).
The pool only wins when each task does enough work to outweigh the cost of
starting a subinterpreter — the speedup is largest on a multi-core desktop, and
smaller on mobile, where startup costs more and there are fewer cores.

### Stream progress from a subinterpreter

To show fine-grained progress from a single long job, share a
[`Queue`](https://docs.python.org/3/library/concurrent.interpreters.html#concurrent.interpreters.Queue)
with the subinterpreter. The worker `put`s progress values; a background thread
drains them into the UI:

<CodeExample path="cookbook/subinterpreters/streaming_queue.py" language="python" />

Two details worth noting: the worker runs on its own thread because
[`interp.call()`](https://docs.python.org/3/library/concurrent.interpreters.html#concurrent.interpreters.Interpreter.call)
blocks until the job finishes, and the interpreter is closed
only **after** the UI has drained every item — a subinterpreter `Queue`'s
pending items become invalid the moment its interpreter closes.

### Keep a persistent, stateful interpreter

Creating an interpreter with
[`interpreters.create()`](https://docs.python.org/3/library/concurrent.interpreters.html#concurrent.interpreters.create)
isn't free, so don't create one per task. Create it **once** and reuse it: the state a worker builds (here, the prime table cached in
a module global) persists in that interpreter between calls, so expensive setup
happens only on the first call.

<CodeExample path="cookbook/subinterpreters/persistent_interpreter.py" language="python" />

Click twice: the first query builds the prime table (slow), the second reuses it
from the live interpreter (instant). In a real app that table stands in for a
loaded model, an opened dataset, or a warmed cache.

Because this interpreter lives for the whole session, the example registers
[`atexit`](https://docs.python.org/3/library/atexit.html) to
[`close()`](https://docs.python.org/3/library/concurrent.interpreters.html#concurrent.interpreters.Interpreter.close)
it at shutdown — otherwise Python warns that a subinterpreter was left open.

## Caveats

- **You can't force-cancel a subinterpreter:** It runs on a thread, so — unlike
  a [`multiprocessing.Process`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Process)
  — there's no
  [`terminate()`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Process.terminate).
  If you need to abort a runaway task, use [multiprocessing](multiprocessing.md)
  instead.
- **Not every C extension supports subinterpreters:** An extension must opt in
  (multi-phase initialization with per-interpreter GIL support); some
  third-party native libraries don't yet and raise
  [`ImportError`](https://docs.python.org/3/library/exceptions.html#ImportError)
  when imported in a subinterpreter. Pure-Python code and the standard library work.
- **Reuse interpreters and pools:** Interpreter startup isn't free (each
  re-imports its modules); create a pool or a persistent interpreter once rather
  than per task.
- **Call module-level helpers from a loop or list comprehension, not a generator
  expression:** The names a generator expression looks up aren't carried into the
  subinterpreter, so `sum(f(x) for x in ...)` referencing a module-level `f`
  raises [`NameError`](https://docs.python.org/3/library/exceptions.html#NameError)
  — in a module just as much as in `main.py`. A plain `for`
  loop or a list comprehension (which Python inlines) works instead, as these
  examples do.
