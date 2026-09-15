---
title: "Migrating from Flet 0.28 to 1.0"
toc_max_heading_level: 3
---

# Migrating from Flet 0.28 to 1.0

Flet 1.0 is not a drop-in replacement for 0.28.x. This guide walks through the
changes an existing 0.28 app needs, in the order that gets it running fastest.

## Why this is a big jump

There is no 0.29 through 0.69. The 1.0 line branched off 0.28.3 and was developed
in the open as a pre-release series, so everything that changed across four
development releases arrives at once:

| Release | Name |
|---|---|
| 0.28.3 | last 0.x release (also called *v0*) |
| 0.70.0 | 1.0 Alpha - new architecture, controls as dataclasses, declarative UI |
| 0.80.0 | 1.0 Beta - replaced 0.28.3 as the current release on PyPI |
| 0.86.0 | packaging and storage rework, in-process dart-bridge |
| 1.0.0 | final release |

The [compatibility policy](compatibility-policy.md) - a deprecation period of at
least three minor releases - applies from 1.0 onward. It does not cover this jump:
the deprecation shims added during the pre-release series were all removed in 1.0.

:::tip[Migrate in this order]
1. **Get it running** - dependencies, entry point, renamed APIs, services.
2. **Then fix responsiveness** - the [single-threaded model](#step-3-your-app-runs-on-one-thread-now).
   This is the step people skip, and it is why an otherwise-working migrated app
   feels slow.
3. **Modernize only if you want to** - components, hooks and the declarative
   router are optional. Your imperative code keeps working.

Starting with step 3 is the most common way to get stuck.
:::

## Step 1: update dependencies

```bash
pip install 'flet[all]' --upgrade
```

Extension packages are versioned in lockstep with `flet` now, so upgrade them
together:

```bash
pip install --upgrade flet flet-audio flet-video
```

If your app used charts, they moved to a separate package:

```bash
pip install flet-charts
```

## Step 2: update the app entry point

`ft.app()` and `ft.app_async()` are gone, and the `target` parameter is now `main`:

```python
# 0.28
ft.app(target=main)
ft.app(target=main, view=ft.AppView.WEB_BROWSER)
```

```python
# 1.0
ft.run(main)
ft.run(main, view=ft.AppView.WEB_BROWSER)
```

Use `ft.run_async()` when your Flet app is started from existing async code.

:::note[`TypeError: 'module' object is not callable`]
That is what a leftover `ft.app(...)` call reports. `flet.app` is now the module
that defines `run()`, so the name still resolves - it is just not a function any
more.
:::

`main` can be sync or `async def` - both are supported. There is also a new
`before_main` argument for setup that must happen after the page exists but
before `main` runs.

## Step 3: your app runs on one thread now

This is the most important behavioral change in 1.0, and the one most likely to
make a working migrated app feel broken.

### What changed

In 0.28, Flet dispatched every **sync** event handler onto a thread pool:

```python
# what 0.28 did internally
if asyncio.iscoroutinefunction(handler):
    await handler(ce)
else:
    self.run_thread(handler, ce)   # <- a pool thread
```

So blocking code in a handler never froze the UI. It occupied a pool thread while
the rest of the app carried on.

In 1.0 a sync handler is called **directly on the app's event loop**:

```python
# what 1.0 does internally
if get_param_count(event_handler) == 0:
    event_handler()
else:
    event_handler(e)
```

There is one event loop per app, and that same loop also sends UI updates to the
client. While your handler runs, nothing else does: no other events are
dispatched, and no updates reach the screen. A sync `main()` runs inline for the
same reason.

### Symptoms

If any of these appeared after upgrading, this step is the cause:

- the window stops repainting while an operation runs
- the progress ring or spinner you set never appears
- every update appears at once, after the work finishes
- clicking other controls does nothing until the operation completes
- on desktop, the OS marks the window as not responding

### Do I have to make everything async?

No. Sync handlers still work and are the right choice for fast, non-blocking work
like setting properties or appending controls. You need `async def` only when you
have something to `await`.

Handlers can also take no arguments at all in 1.0, which is handy when you do not
need the event:

```python
def handle_click():
    counter.value += 1

ft.Button(content="Add", on_click=handle_click)
```

### What to do instead

| Work | 0.28 | 1.0 |
|---|---|---|
| Delay | `time.sleep(1)` | `await asyncio.sleep(1)` |
| HTTP request | `requests.get(url)` | async client, or offload |
| Database query | `sqlite3`, `psycopg2` | async driver, or offload |
| Reading a large file | `open(path).read()` | `aiofiles`, or offload |
| CPU-bound work | inside the sync handler on a pool thread | offload (see below) |
| Background loop | `threading.Thread` | `page.run_task()` |
| Shelling out | `subprocess.run()` | `asyncio.create_subprocess_exec()` |

### Switching to async libraries

Most popular blocking libraries have an async counterpart:

| Blocking | Async |
|---|---|
| `requests` | [`httpx`](https://www.python-httpx.org/async/), [`aiohttp`](https://docs.aiohttp.org/) |
| `sqlite3` | [`aiosqlite`](https://aiosqlite.omnilib.dev/) |
| `psycopg2` | [`asyncpg`](https://magicstack.github.io/asyncpg/), `psycopg` 3 async |
| `pymongo` | [`motor`](https://www.mongodb.com/docs/drivers/motor/) |
| `redis` | `redis.asyncio` |
| `boto3` | [`aioboto3`](https://aioboto3.readthedocs.io/) |
| `paramiko` | [`asyncssh`](https://asyncssh.readthedocs.io/) |
| `open()` | [`aiofiles`](https://github.com/Tinche/aiofiles) |
| `subprocess` | [`asyncio` subprocesses](../cookbook/subprocess.md) |

A blocking HTTP call becomes:

```python
# 0.28 - fine, because this ran on a pool thread
def load_data(e):
    response = requests.get("https://api.example.com/items")
    items.value = response.text
    page.update()
```

```python
# 1.0 - async library
async def load_data(e):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/items")
    items.value = response.text
```

### When there is no async version

Offload the blocking call to a thread. In order of preference:

**1. `asyncio.to_thread()`** - when you need the result back. This is the default
answer:

```python
async def load_data(e):
    response = await asyncio.to_thread(requests.get, "https://api.example.com/items")
    items.value = response.text
```

**2. [`page.run_thread()`][flet.Page.run_thread]** - fire-and-forget work on
Flet's shared thread pool. It also re-establishes the page context inside the
thread, and degrades gracefully on the web, where it runs inline instead of
failing:

```python
def save_log(e):
    page.run_thread(write_log_file, "clicked")
```

**3. `page.loop.run_in_executor()`** - when you want your own pool, for example to
bound how many of these run at once:

```python
pool = ThreadPoolExecutor(max_workers=2)

async def convert(e):
    await page.loop.run_in_executor(pool, transcode, path)
```

### CPU-bound work

Threads do not give you parallelism for pure-Python code, because the GIL lets
only one thread execute Python bytecode at a time. A thread does keep the UI
responsive - the interpreter switches between threads often enough that the loop
keeps running - but the work itself will not go faster, and it competes with the
loop for the interpreter.

For work that genuinely needs CPU:

- [Subinterpreters](../cookbook/subinterpreters.md) (Python 3.14+) run Python on
  several cores inside one process. This is the option that also works on
  **iOS and Android**.
- [Multiprocessing](../cookbook/multiprocessing.md) gives full isolation and lets
  you hard-cancel a worker, but is **desktop only** - mobile operating systems do
  not let an app spawn child processes.
- C extensions that release the GIL (NumPy, Pillow, database drivers) parallelize
  fine in plain threads.

### Reporting progress from long work

In 0.28 you called `page.update()` from inside a loop running on a pool thread.
That no longer works, because the loop never gets a chance to send the update:

```python
# 1.0 - broken: the UI is frozen and the bar only appears at 100%
def process(e):
    for i in range(100):
        do_chunk(i)
        progress.value = (i + 1) / 100
        progress.update()      # queued, but nothing is sent until we return
```

**If each chunk is short**, make the handler a generator. Every `yield` flushes
pending updates and lets the loop breathe:

```python
def process(e):
    for i in range(100):
        do_chunk(i)
        progress.value = (i + 1) / 100
        yield                  # update reaches the screen here
```

This is the smallest change that works, but the work still runs on the event
loop, so keep each chunk to a few milliseconds.

**If the chunks are heavy**, offload them and yield between chunks to trigger
an intermediate update. An `await` alone does not trigger auto-update:

```python
async def process(e):
    for i in range(100):
        await asyncio.to_thread(do_chunk, i)
        progress.value = (i + 1) / 100
        yield
```

**If you need real parallelism**, hand the whole job to an executor and report
progress as futures complete:

```python
async def process(e):
    done = 0
    with InterpreterPoolExecutor() as pool:
        futures = [page.loop.run_in_executor(pool, do_chunk, i) for i in range(100)]
        for future in asyncio.as_completed(futures):
            await future
            done += 1
            progress.value = done / 100
            progress.update()
```

`do_chunk` must be defined at module top level for this to work - see
[Subinterpreters](../cookbook/subinterpreters.md) for the rules.

### Background tasks and timers

Replace background threads with [`page.run_task()`][flet.Page.run_task]:

```python
# 0.28
def main(page: ft.Page):
    def clock():
        while True:
            time_text.value = datetime.now().strftime("%H:%M:%S")
            page.update()
            time.sleep(1)

    threading.Thread(target=clock, daemon=True).start()
```

```python
# 1.0
def main(page: ft.Page):
    async def clock():
        while True:
            time_text.value = datetime.now().strftime("%H:%M:%S")
            time_text.update()
            await asyncio.sleep(1)

    page.add(time_text)
    page.run_task(clock)
```

Pass the coroutine **function**, not a called coroutine: `page.run_task(clock)`,
not `page.run_task(clock())`. It raises `TypeError` otherwise.

`run_task()` returns a future, so a control that starts background work can stop
it again on the way out:

```python
@ft.control
class Clock(ft.Text):
    def did_mount(self):
        self._task = self.page.run_task(self.tick)

    def will_unmount(self):
        self._task.cancel()

    async def tick(self):
        while True:
            self.value = datetime.now().strftime("%H:%M:%S")
            self.update()
            await asyncio.sleep(1)
```

### Platform differences

:::warning[There are no threads on the web]
Apps [published as a static website](../publish/web/static-website/index.md) run
in the browser on Pyodide, a single-threaded WebAssembly runtime.
`asyncio.to_thread()` is not usable there, `page.run_thread()` runs its callable
inline, and neither subinterpreters nor multiprocessing are available.

For a static web target the only options for long work are to chunk it and
`yield`, use a real async library, or move the work to a server. A
[dynamic website](../publish/web/dynamic-website/index.md) runs your Python
server-side as an ordinary CPython process, so threads work there as they do on
desktop.
:::

For a fuller treatment of the concurrency model, including which offloading
primitive to reach for, see [Async apps](../cookbook/async-apps.md).

:::note[PubSub is different]
Sync [PubSub](../cookbook/pub-sub.md) subscribers are still run on the thread
pool rather than on the loop, so a blocking subscriber will not freeze the UI.
Event handlers are the ones that changed.
:::

## Step 4: services are no longer added to the page

Non-visual features - file pickers, shared preferences, the clipboard, sensors -
are *services* in 1.0. You create one and use it; nothing needs to be added to
the page:

```python
# 0.28
def main(page: ft.Page):
    file_picker = ft.FilePicker(on_result=handle_result)
    page.overlay.append(file_picker)
    page.update()

    page.add(ft.ElevatedButton("Pick files", on_click=lambda _: file_picker.pick_files()))
```

```python
# 1.0
def main(page: ft.Page):
    file_picker = ft.FilePicker()
    selection = ft.Text()

    async def pick_files(e):
        files = await file_picker.pick_files(allow_multiple=True)
        if files:
            selection.value = ", ".join(f.name for f in files)

    page.add(selection, ft.Button(content="Pick files", on_click=pick_files))
```

Two things changed at once. The service registers itself when you construct it,
and the dialog methods are awaitable and return their result directly - there is
no `on_result` round trip to wire up.

:::note[If you followed the 0.8x docs]
The pre-release series required `page.services.append(service)`. That still works
for explicit lifecycle control, but is no longer necessary.
:::

:::note[Keep a reference when reusing a service]
Keep a service in a control field or a variable captured by your event handlers
when you need to reuse it. Flet unregisters services that no longer have live
Python references.

A temporary service is fine for a single awaited call, such as
`await ft.SharedPreferences().get("key")`: the call keeps the service alive until
it finishes.
:::

These page members were replaced by services, and were removed in 1.0:

| 0.28 | 1.0 |
|---|---|
| `page.client_storage.set(k, v)` | `await ft.SharedPreferences().set(k, v)` |
| `page.set_clipboard(v)` | `await ft.Clipboard().set(v)` |
| `page.get_clipboard()` | `await ft.Clipboard().get()` |
| `page.launch_url(url)` | `await ft.UrlLauncher().launch_url(url)` |
| `page.can_launch_url(url)` | `await ft.UrlLauncher().can_launch_url(url)` |
| `page.close_in_app_web_view()` | `await ft.UrlLauncher().close_in_app_web_view()` |
| `page.browser_context_menu` | `ft.BrowserContextMenu()` |
| `page.storage_paths` | `ft.StoragePaths()` |

All service methods are `async`, so `await` them:

```python
prefs = ft.SharedPreferences()

async def save(e):
    await prefs.set("theme", "dark")
    value = await prefs.get("theme")
```

These controls became services too, and are no longer added to `page.overlay`:
`Audio`, `AudioRecorder`, `Flashlight`, `Geolocator`, `HapticFeedback`,
`InterstitialAd`, `PermissionHandler`, `SemanticsService`, `ShakeDetector`.

:::tip[Opening a picker in a web app]
A browser only opens a file picker while it is handling a click, which is already
over by the time your handler runs. On the web, attach a
[client action](../cookbook/client-actions.md) instead. See
[FilePicker](../services/filepicker.md).
:::

## Step 5: updates are automatic

Flet calls `update()` for you after every event handler and after `main()`
returns, so most of the `page.update()` calls in a 0.28 app are now redundant:

```python
# 0.28
def add_item(e):
    page.controls.append(ft.Text("New item"))
    page.update()
```

```python
# 1.0 - the update happens on its own
def add_item(e):
    page.controls.append(ft.Text("New item"))
```

Existing calls are harmless: an explicit `update()` suppresses the automatic one,
so you get a single update either way. You can migrate them away gradually.

Three related changes:

- `yield` inside a handler flushes an update mid-handler. This replaces calling
  `page.update()` from inside a loop.
- `ft.context.disable_auto_update()` turns the automatic update off for the
  current handler, for when you want to batch a large number of mutations into
  one update yourself.
- `control.update()` now **raises** if the control is not on the page yet. In
  0.28 it silently did nothing. Set initial values through constructor arguments
  rather than calling `update()` during construction.

See [Auto-update](../cookbook/auto-update.md) for details.

## Step 6: `UserControl` is gone

Controls are dataclasses in 1.0, and `ft.UserControl` no longer exists. A custom
control subclasses the control it is built from:

```python
# 0.28
class Task(ft.UserControl):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def build(self):
        return ft.Row([ft.Checkbox(), ft.Text(self.text)])
```

```python
# 1.0
@ft.control
class Task(ft.Row):
    text: str = ""

    def init(self):
        self.controls = [ft.Checkbox(), ft.Text(self.text)]
```

Things to watch for when porting:

- A field needs a **type annotation** to be a field. `text: str = ""` works;
  `text = ""` does not. If you are unsure of the type, `Any` is fine.
- Use `field(default_factory=...)` for mutable or class defaults, and plain
  literals for `int`, `str`, `bool`.
- `__init__` becomes `init()`, and you do not call `super().__init__()`.
- `build()` still exists as a hook for defining child controls, and
  `did_mount()` / `will_unmount()` are unchanged.
- Do not assign `self.page` - `page` is a read-only property on every control.

See [Custom controls](../cookbook/custom-controls.md) for the full rules.

## Step 7: renamed and moved APIs

### Controls and base classes

| 0.28 | 1.0 |
|---|---|
| `ft.ElevatedButton(...)` | `ft.Button(...)` |
| `ft.Button(text="Save")`, and all buttons | `ft.Button(content="Save")` |
| `ft.ConstrainedControl` | `ft.LayoutControl` |
| `ft.UserControl` | subclass a control - see [step 6](#step-6-usercontrol-is-gone) |
| chart controls | the `flet-charts` package |

### Constants and helpers

The lowercase module aliases are gone; reach constants through the capitalized
class.

| 0.28 | 1.0 |
|---|---|
| `ft.colors.RED` | `ft.Colors.RED` |
| `ft.icons.ADD` | `ft.Icons.ADD` |
| `ft.alignment.center` | `ft.Alignment.CENTER` |
| `ft.animation.Animation(...)` | `ft.Animation(...)` |
| `ft.padding.all(10)` | `ft.Padding.all(10)` |
| `ft.padding.symmetric(0, 10)` | `ft.Padding.symmetric(vertical=0, horizontal=10)` |
| `ft.margin.all(5)` | `ft.Margin.all(5)` |
| `ft.border.all(1)` | `ft.Border.all(1)` |
| `ft.border_radius.all(8)` | `ft.BorderRadius.all(8)` |
| `ft.Colors.BLACK54` | `ft.Colors.BLACK_54` |

The module-level `all()` / `symmetric()` / `only()` helpers became classmethods on
`Padding`, `Margin`, `Border` and `BorderRadius`, and `symmetric()` takes keyword
arguments only.

### Dialogs, drawers and navigation

| 0.28 | 1.0 |
|---|---|
| `page.open(dialog)` | `page.show_dialog(dialog)` |
| `page.close(dialog)` | `page.pop_dialog()` |
| `page.dialog = d; d.open = True` | `page.show_dialog(d)` |
| `page.go(route)` | `await page.push_route(route)` |
| `page.on_resized` | `page.on_resize` |

Drawers still live on the page, but you open them with a method:

```python
# 1.0
page.drawer = ft.NavigationDrawer(controls=[...])

async def open_drawer(e):
    await page.show_drawer()       # or page.close_drawer()
```

`page.end_drawer` works the same way, with `show_end_drawer()` and
`close_end_drawer()`.

### Events

- `e.target` is an `int` now, not a string.
- Handlers may take zero or one argument.
- `DragTarget.on_will_accept` receives a `DragWillAcceptEvent` - use `e.accept`
  instead of `e.data`.
- `DragTarget.on_leave` receives a `DragTargetLeaveEvent` - use `e.src_id`
  instead of `e.data`.
- Typed events are written `ft.Event[ft.Button]`.

### Property renames

| 0.28 | 1.0 |
|---|---|
| `Icon.name` | `Icon.icon` |
| `Card.color` | `Card.bgcolor` |
| `Card.is_semantic_container` | `Card.semantic_container` |
| `Checkbox.is_error` | `Checkbox.error` |
| `Chip.click_elevation` | `Chip.elevation_on_click` |
| `Switch.label_style` | `Switch.label_text_style` |
| `Tabs.is_secondary` | `TabBar.secondary` - see below |
| `Tab.text` / `Tab.tab_content` | `Tab.label` |
| `Badge.text` | `Badge.label` |
| `Markdown.img_error_content` | `Markdown.image_error_content` |
| `BoxDecoration.shadow` | `BoxDecoration.shadows` |
| `canvas.Text.text` | `canvas.Text.value` |
| `NavigationRailDestination.label_content` | `NavigationRailDestination.label` |
| `Pagelet.bottom_app_bar` | `Pagelet.bottom_appbar` |
| `on_scroll_interval` | `scroll_interval` |
| `scroll_to(key=...)` | `scroll_to(scroll_key=...)`, with `key=ft.ScrollKey(v)` on the control |
| `SegmentedButton(selected={"1"})` | `SegmentedButton(selected=["1"])` - a list, not a set |
| `CupertinoDialogAction.is_default_action` | `.default` |
| `CupertinoDialogAction.is_destructive_action` | `.destructive` |

The same `is_default_action` / `is_destructive_action` rename applies to
`CupertinoActionSheetAction` and `CupertinoContextMenuAction`.

:::danger[`SafeArea` edges changed meaning, silently]
In 0.28, `SafeArea(left=False)` meant "do not pad the left edge". In 1.0 those flags
are `avoid_intrusions_left` / `_top` / `_right` / `_bottom`, and `left`, `top`,
`right` and `bottom` are the ordinary positioning properties every control has for
use inside a `Stack`.

Old code still runs, but it now positions the control instead of configuring the
safe area. This is the one rename in this guide that fails silently rather than
raising, so grep for it:

```python
# 0.28
ft.SafeArea(content=body, left=False, right=False)

# 1.0
ft.SafeArea(content=body, avoid_intrusions_left=False, avoid_intrusions_right=False)
```
:::

### Tabs

`Tabs` was split into three controls. `Tabs` now supplies the shared state, with a
`TabBar` for the headers and a `TabBarView` for the content:

```python
# 0.28
ft.Tabs(
    selected_index=0,
    tabs=[
        ft.Tab(text="Overview", content=ft.Text("Overview content")),
        ft.Tab(text="Settings", content=ft.Text("Settings content")),
    ],
)
```

```python
# 1.0
ft.Tabs(
    length=2,
    content=ft.Column(
        controls=[
            ft.TabBar(tabs=[ft.Tab(label="Overview"), ft.Tab(label="Settings")]),
            ft.TabBarView(
                controls=[ft.Text("Overview content"), ft.Text("Settings content")],
            ),
        ],
    ),
)
```

`length` must match the number of tabs. `is_secondary` moved to `TabBar.secondary`.

### Theme

`Theme.primary_swatch`, `primary_color`, `primary_color_dark`,
`primary_color_light` and `shadow_color` were removed. Use
`Theme.color_scheme_seed` for the seed color, and `ColorScheme.primary` /
`ColorScheme.shadow` for the individual colors.

### Methods

Methods no longer carry an `_async` suffix; the plain name is the async one.
`Dropdown.on_change` now also fires when text is typed in editable mode, and a
new `on_select` fires when an item is picked from the list.

:::note[Something missing?]
[All deprecated APIs removed](breaking-changes/v1-0-0/removed-deprecated-apis.md)
covers what 1.0 dropped from the pre-release series, and
[breaking changes and deprecations](breaking-changes/index.md) is organized by
release. For anything not listed here, open a
[discussion](https://github.com/flet-dev/flet/discussions) so this guide can be
corrected.
:::

## Step 8: packaging, files and storage

If you package your app with `flet build`, a few things changed in 0.86 that
affect 0.28 apps in particular:

- **Your app bundle is read-only, and the working directory moved** to a writable
  app-private directory. Relative reads of bundled files - `open("seed.json")` -
  need to go through `__file__`, `importlib.resources`, or `assets/`.
  `FLET_APP_STORAGE_DATA` now maps to the OS application-support directory, and
  there is a new `FLET_APP_STORAGE_CACHE`. See
  [App files ship unpacked in a read-only bundle](breaking-changes/v0-86-0/app-files-unpacked-read-only-bundle.md).
- **Python 3.14 is bundled by default.** If you depend on native wheels without
  3.14 binaries, pin with `--python-version 3.12`. See
  [Default bundled Python version is now 3.14](breaking-changes/v0-86-0/default-bundled-python-3-14.md).
- **Your app is compiled to `.pyc` by default**, which speeds up cold start. Pass
  `--no-compile-app` to opt out. See
  [App and packages are compiled to .pyc by default](breaking-changes/v0-86-0/compile-on-by-default.md).
- On Android, site-packages ship zipped and some packages need `extract_packages`.
  See [Android: site-packages ship zipped](breaking-changes/v0-86-0/android-extract-packages.md).

Assets are referenced by filename only - `ft.Image(src="bear.svg")`, not
`src="assets/bear.svg"`.

## What is new, and entirely optional

None of this is required to migrate. Your imperative 0.28-style code keeps
working in 1.0.

- [Declarative UI](../cookbook/declarative-vs-imperative.md) - `@ft.component`,
  `use_state` and hooks, for state-heavy screens.
- [Router](../cookbook/router.md) - declarative routing with a view stack.
- [Client actions](../cookbook/client-actions.md) - gesture-gated work such as
  opening a picker or writing to the clipboard, performed without a round trip to
  Python. This is what makes those features reliable in a browser.
- [Subinterpreters](../cookbook/subinterpreters.md) - multi-core Python in one
  process, including on mobile.

## Staying on 0.28.x

If you are not migrating yet, pin the version:

```toml
dependencies = ["flet==0.28.3"]
```

0.28.x continues to receive bug and security fixes, but no new features.
