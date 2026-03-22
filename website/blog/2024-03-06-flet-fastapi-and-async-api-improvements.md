---
slug: flet-fastapi-and-async-api-improvements
title: Flet FastAPI and async API improvements
authors: feodor
tags: [releases]
---

Flet makes writing dynamic, real-time web apps a real fun!

Flet 0.21.0 further improves web apps development experience as well as using asyncio APIs in your Flet apps.

Here's what's new in Flet 0.21.0:

<!-- truncate -->

## FastAPI with Uvicorn replaces built-in web server

From very beginning of Flet life to serve web apps there was a built-in web server written in Go
and called "Fletd". It's being started on the background when you run your app with `flet run --web`.
Fletd was part of Flet Python wheel contributing a few megabytes to its size.
Additionally, Python app was using WebSockets to talk to Fletd web server which was adding sometimes noticeable overhead.

Then, in [Flet 0.10.0](/blog/flet-for-fastapi) we have added FastAPI support to build "serious" web apps using AsyncIO API.

Now, in Flet 0.21.0 built-in web server has been completely removed and replaced with FastAPI and Uvicorn. Fletd is not
a part of Flet distribution anymore.

Using FastAPI means there is no more communication overhead as web server is a part of Flet app.
Also, you don't need to do any additional steps to host your app in production with FastAPI -
you just use the same `ft.run(main)` command to run your app.

:::warning Breaking change

`flet_fastapi` package has been deprecated and its contents moved to `flet` package as `flet.fastapi`
module. If you were using FastAPI in your Flet app replace:

```python
import flet_fastapi
```

with

```python
import flet.fastapi as flet_fastapi
```
:::

**Use any ASGI web server for hosting**

You can host your Flet web app with any ASGI-compatible server such as [Uvicorn](https://www.uvicorn.org/) (used by default), [Hypercorn](https://pgjones.gitlab.io/hypercorn/) or [Daphne](https://github.com/django/daphne).

Just tell Flet to export ASGI app:

```python title="main.py"
import flet as ft

def main(page: ft.Page):
    page.add(ft.Text("Hello ASGI!"))

app = ft.run(main, export_asgi_app=True)
```

and then run with Hypercorn as:

```
hypercorn main:app --bind 0.0.0.0:8000
```

**Web app environment variables**

Every aspect of web app hosting can be controlled with environment variables:

* `FLET_FORCE_WEB_SERVER` - `true` to force running app as a web app. Automatically set on headless Linux hosts.
* `FLET_SERVER_PORT` - TCP port to run app on. `8000` if the program is running on a Linux server or `FLET_FORCE_WEB_SERVER` is set; otherwise random port.
* `FLET_SERVER_IP` - IP address to listen web app on, e.g. `127.0.0.1`. Default is `0.0.0.0` - bound to all server IPs.
* `FLET_ASSETS_DIR` - absolute path to app "assets" directory.
* `FLET_UPLOAD_DIR` - absolute path to app "upload" directory.
* `FLET_MAX_UPLOAD_SIZE` - max allowed size of uploaded file, in bytes. Unlimited if not specified.
* `FLET_SECRET_KEY` - a secret key to sign temporary upload URLs.
* `FLET_WEB_APP_PATH` - a URL path after domain name to host web app under, e.g. `/apps/myapp`. Default is `/` - host app in the root.
* `FLET_SESSION_TIMEOUT` - session lifetime, in seconds. Default is `3600`.
* `FLET_OAUTH_STATE_TIMEOUT` - max allowed time to complete OAuth web flow, in seconds. Default is `600`.
* `FLET_WEB_RENDERER` - Flutter rendering mode: `canvaskit` (default), `html` or `auto`.
* `FLET_WEB_USE_COLOR_EMOJI` - `true`, or `True` or `1` to load web font with colorful emojis.
* `FLET_WEB_ROUTE_URL_STRATEGY` - `path` (default) or `hash`.
* `FLET_WEBSOCKET_HANDLER_ENDPOINT` - custom path for WebSocket handler. Default is `/ws`.
* `FLET_UPLOAD_HANDLER_ENDPOINT` - custom path for upload handler. Default is `/upload`.
* `FLET_OAUTH_CALLBACK_HANDLER_ENDPOINT` - custom path for OAuth handler. Default is `/oauth_callback`.

## Async-first framework

Flet is now async-first framework which means you don't have to decide whether your app is entirely sync or async, but you can mix both sync and async methods in the same app.

For example, in Flet 0.21.0 you can write an app like this:

```python
import flet as ft
import time
import asyncio

def main(page: ft.Page):

    def handler(e):
      time.sleep(3)
      page.add(ft.Text("Handler clicked"))

    async def handler_async(e):
      await asyncio.sleep(3)
      page.add(ft.Text("Async handler clicked"))

    page.add(
        ft.ElevatedButton("Call handler", on_click=handler),
        ft.ElevatedButton("Call async handler", on_click=handler_async)
    )

ft.run(main)
```

In the example above a click on one button is handled by a "blocking" handler while a click
on second button calls asynchronous handler. The first handler is run in a `threading.Thread` while second handler is run in `asyncio.Task`.

Also, notice in `async def` handler you are not required to use `await page.add_async()` anymore, but a regular `page.add()` works just fine.

:::info API changes
Most of `Page.<method>_async()` and `Control.<method>_async()` methods have been deprecated and their `Page.<method>()` and `Control.<method>()` counterparts should be used instead.

The only exception here is methods returning results, like those ones in `Audio` control: you still have to use async methods in async event handlers.
::: 

## Custom controls API normalized

In this Flet release we also re-visited API for writing custom controls in Python.

As a result `UserControl` class has been deprecated. You just inherit from a specific control with layout that works for your needs.

For example, `Countdown` custom control is just a `Text` and could be implemented as following:

```python
import asyncio

import flet as ft

class Countdown(ft.Text):
    def __init__(self, seconds):
        super().__init__()
        self.seconds = seconds

    def did_mount(self):
        self.running = True
        self.page.run_task(self.update_timer)

    def will_unmount(self):
        self.running = False

    async def update_timer(self):
        while self.seconds and self.running:
            mins, secs = divmod(self.seconds, 60)
            self.value = "{:02d}:{:02d}".format(mins, secs)
            self.update()
            await asyncio.sleep(1)
            self.seconds -= 1

def main(page: ft.Page):
    page.add(Countdown(120), Countdown(60))

ft.run(main)
```

Notice the usage of `self.page.run_task(self.update_timer)` to start a new task.
There is also `self.page.run_thread()` method that must be used by control developer to start a new background job in a thread.

If you want to spawn your own tasks or threads Flet provides the current event loop and thread executor via `Page.loop` and `Page.executor` properties respectively. 

:::info API changes
`Control._before_build_command()` replaced with `Control.before_update()`

`Control.build()` should not return any control now, but must update inherited control properties, for example:

```python
def build():
    self.controls.append(ft.Text("Something"))
```

`Control.did_mount_async()` and `Control.will_unmount_async()` are deprecated. Use `Control.did_mount()` and `Control.will_unmount()` instead.
:::

## New Cupertino controls

This Flet release adds more Cupertino controls to make your apps shine on iOS:

* `CupertinoActivityIndicator`
* `CupertinoActionSheet`
* `CupertinoSlidingSegmentedButton`
* `CupertinoSegmentedButton`
* `CupertinoTimerPicker`
* `CupertinoPicker`
* `CupertinoDatePicker`
* `CupertinoContextMenu`

## Accessibility improvements

Now Flet has complete implementation of `Semantics` control and new `SemanticsService` control.

## App lifecycle change event

There is a new `Page.on_app_lifecycle_state_change` event that allows listening for changes in the application lifecycle.

For example, you can now update UI with the latest information when the app becomes active (brought to the front). This event works on iOS, Android, all desktop platforms and web!

The following app lifecycle transitions are recognized:

* `SHOW`
* `RESUME`
* `HIDE`
* `INACTIVE`
* `PAUSE`
* `DETACH`
* `RESTART`

:::note
Read more about each [lifecycle state](https://docs.flet.dev/controls/page/#flet.Page.on_app_lifecycle_state_change).
:::

Here's a small example of how this event can be used: 

```python
import flet as ft

def main(page: ft.Page):

    def app_lifecycle_change(e: ft.AppLifecycleStateChangeEvent):
        if e.state == ft.AppLifecycleState.RESUME:
          print("Update UI with fresh data!")

    page.on_app_lifecycle_state_change = app_lifecycle_change
    page.add(ft.Text("Hello World"))

ft.run(main)
```

Flet 0.21.0 release has some breaking changes. Upgrade to it, test your apps and let us know how it worked for you.
Join [Flet Discord server](https://discord.gg/dzWXP8SHG8) or create a new thread
on [Flet GitHub discussions](https://github.com/flet-dev/flet/discussions).

Enjoy!