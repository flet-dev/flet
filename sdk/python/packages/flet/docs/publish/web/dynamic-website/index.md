Flet implements [FastAPI](https://fastapi.tiangolo.com/) app to run your app as a dynamic website.

It uses [Uvicorn](https://www.uvicorn.org/) web server, by default, to run the app, but any ASGI-compatible server can be used instead.

### Sync and async handlers

In Flet web app you can mix both sync and async methods in the same app.

For example, you can write an app like this:

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

In the example a click on one button is handled by a "blocking" handler while a click
on second button calls asynchronous handler. The first handler is run in a `threading.Thread` while second handler is run as `asyncio.Task`.

In web apps, using threads is one of the considerations for app scalability as threads is a finite resource. Usually, a thread pool is used and it could become a bottleneck with a growing number of users.

Anyway, if your app is mostly doing I/O (database, web API) and/or you are able to use async-ready libraries we recommend implementing async handlers.

Check [FastAPI's article about async/await](https://fastapi.tiangolo.com/async/) to better understand the differences between concurrency and parallelism.

## Running the app locally

Use `--web` (`-w`) option to start a Flet app as a web app:

```
flet run --web app.py
```

A new browser window/tab will be opened and the app will be using a random TCP port.

To run on a fixed port use `--port` (`-p`) option:

```
flet run --web --port 8000 app.py
```

## Running the app in production

You can run your program with `python` command directly:

```
python app.py
```

[Uvicorn](https://www.uvicorn.org/) web server is used by default to host the web app.

If Flet detects the app is running in headless Linux environment (such as Docker container
or EC2 VM):
1. Port `8000` will be used to run the app.
2. A new browser window with an app won't be opened.

If, for some reason, Flet is unable to detect headless environment you can force that behavior
by defining the following environment variable:

```
FLET_FORCE_WEB_SERVER=true
```

### ASGI web server

You can host your Flet web app with any ASGI-compatible server such as [Uvicorn](https://www.uvicorn.org/) (used by default), [Hypercorn](https://pgjones.gitlab.io/hypercorn/) or [Daphne](https://github.com/django/daphne).

Just tell Flet to export ASGI app:

```python title="main.py"
import flet as ft

def main(page: ft.Page):
    page.add(ft.Text("Hello ASGI!"))

app = ft.run(main, export_asgi_app=True)
```

#### Hypercorn

[Hypercorn](https://github.com/pgjones/hypercorn/) is another ASGI web server inspired by Gunicorn.

To run the app with Hypercorn:

```
hypercorn main:app --bind 0.0.0.0:8000
```

#### Daphne

[Daphne](https://github.com/django/daphne) is a HTTP, HTTP2 and WebSocket protocol server for ASGI and ASGI-HTTP, developed to power Django Channels.

To run the app with Daphne:

```
daphne -b 0.0.0.0 -p 8000 main:app
```

#### Gunicorn

[Gunicorn](https://gunicorn.org/) is popular web server to run Python web applications. While it implements WSGI specification it's possible to run ASGI FastAPI apps with a [worker process class](https://fastapi.tiangolo.com/deployment/server-workers/) provided by Uvicorn:

```
gunicorn --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker counter:app
```

## Assets

When you open Flet app in the browser its `index.html`, Flutter engine, favicon, images and
other web app resources are served by a web server.
These resources are bundled with `flet` Python package.
However, there are situations when you need to modify the contents of certain files to customize
appearance of your app or its behavior, for example:

* Favicon.
* App loading animation.
* `manifest.json` with PWA details.

You can specify `assets_dir` in `flet.app()` call to set the location of assets that should be available to the application.
`assets_dir` should be a relative to your `main.py` directory or an absolute path.
Default value for `assets_dir` argument is `assets`.

For example, consider the following program structure:

```
/assets
   /images/my-image.png
main.py
```

You can access your images in the application as following:

```python
import flet as ft

def main(page: ft.Page):
    page.add(ft.Image(src=f"/images/my-image.png"))

ft.run(main, assets_dir="assets")
```

### Customizing web app

#### Favicon

To override favicon with your own put `favicon.png` file into the root of assets directory.
It should be a PNG image with the size of at least 32x32 pixels.

#### Loading animation

To override Flet animation image put `icons/loading-animation.png` image with your own app logo
into the the root of assets directory.

#### PWA

Progressive Web Apps, or PWAs, offer a way to turn app-like websites into website-like apps.

Check [PWAs Turn Websites Into Apps: Here's How](https://www.pcmag.com/how-to/how-to-use-progressive-web-apps) for the PWA introduction.

Browsers that support PWA ([installation instructions](#pwa)):

* **Chrome** on all platforms
* **Edge** on all platforms
* **Firefox** on Android
* **Safari** on iOS and iPadOS

::info
The information in this section is based on the following sources (check them out for more details):

* [General information about PWAs](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)
* [PWA manifests](https://developer.mozilla.org/en-US/docs/Web/Manifest)
::

##### Manifest

You can change PWA's name, description, colors and other information in `manifest.json` that must be put
in the root of `assets` directory.

Here are the links to the most common manifest items that you'd like to customize:

* [`name`](https://developer.mozilla.org/en-US/docs/Web/Manifest/name) - the name of the web application as it is usually displayed to the user.
* [`short_name`](https://developer.mozilla.org/en-US/docs/Web/Manifest/short_name) - the name of the web application displayed to the user if there is not enough space to display `name`.
* [`description`](https://developer.mozilla.org/en-US/docs/Web/Manifest/description) - explains what the application does.
* [`theme_color`](https://developer.mozilla.org/en-US/docs/Web/Manifest/theme_color) - defines the default theme color for the application.
* [`background_color`](https://developer.mozilla.org/en-US/docs/Web/Manifest/background_color) - defines a placeholder background color for the application page to display before its stylesheet is loaded.

##### Icons

Custom icons should be placed in `assets/icons` directory:

* `icon-192.png`, `icon-512.png` - app icons displayed in Windows taskbar.
* `icon-maskable-192.png`, `icon-maskable-512.png` - app icons displayed in Android.
* `apple-touch-icon-192.png` - app icon displayed in iOS.

## Environment variables

Every aspect of web app hosting can be additionally controlled with environment variables:

* `FLET_FORCE_WEB_SERVER` - `true` to force running app as a web app. Automatically set on headless Linux hosts.
* `FLET_SERVER_PORT` - TCP port to run app on. `8000` if the program is running on a Linux server or `FLET_FORCE_WEB_SERVER` is set; otherwise random port.
* `FLET_SERVER_IP` - IP address to listen web app on, e.g. `127.0.0.1`. Defaults to `0.0.0.0` - bound to all server IPs.
* `FLET_ASSETS_DIR` - absolute path to app "assets" directory.
* `FLET_UPLOAD_DIR` - absolute path to app "upload" directory.
* `FLET_MAX_UPLOAD_SIZE` - max allowed size of uploaded file, in bytes. Unlimited if not specified.
* `FLET_SECRET_KEY` - a secret key to sign temporary upload URLs.
* `FLET_WEB_APP_PATH` - a URL path after domain name to host web app under, e.g. `/apps/myapp`. Defaults to `/` - host
  app in the root.
* `FLET_SESSION_TIMEOUT` - session lifetime, in seconds. Defaults to `3600`.
* `FLET_OAUTH_STATE_TIMEOUT` - max allowed time to complete OAuth web flow, in seconds. Defaults to `600`.
* `FLET_WEB_RENDERER` - Flutter rendering mode: `canvaskit` (default), `html` or `auto`.
* `FLET_WEB_USE_COLOR_EMOJI` - `true`, or `True` or `1` to load web font with colorful emojis.
* `FLET_WEB_ROUTE_URL_STRATEGY` - `path` (default) or `hash`.
* `FLET_WEBSOCKET_HANDLER_ENDPOINT` - custom path for WebSocket handler. Defaults to `/ws`.
* `FLET_UPLOAD_HANDLER_ENDPOINT` - custom path for upload handler. Defaults to `/upload`.
* `FLET_OAUTH_CALLBACK_HANDLER_ENDPOINT` - custom path for OAuth handler. Defaults to `/oauth_callback`.

## Advanced FastAPI scenarios

### Flet FastAPI app

`flet.fastapi.app()` function creates a new FastAPI application to handle sessions with `session_handler`
and mounts the following endpoints in the root of the app:

`/ws` (WS) - WebSocket handler for the Flet app. It calls `main()` function when a new WebSocket connection established and a new app session created.

`/upload` (PUT) - file uploads handler.

`/oauth_callback` (GET) - OAuth flow callback handler.

`/` (GET) - Flet app static files with SPA catch-all handler.

`flet.fastapi.app()` parameters:

* `session_handler` (function or coroutine) - application entry point - a method called for newly connected user. Handler must have 1 parameter: `page` - `Page` instance.
* `assets_dir` (str, optional) - an absolute path to app's assets directory.
* `app_name` (str, optional) - PWA application name.
* `app_short_name` (str, optional) - PWA application short name.
* `app_description` (str, optional) - PWA application description.
* `web_renderer` (WebRenderer) - web renderer defaulting to `WebRenderer.CANVAS_KIT`.
* `use_color_emoji` (bool) - whether to load a font with color emoji. Default is `False`.
* `route_url_strategy` (str) - routing URL strategy: `path` (default) or `hash`.
* `upload_dir` (str) - an absolute path to a directory with uploaded files.
* `max_upload_size` (str, int) - maximum size of a single upload, bytes. Unlimited if `None`.
* `secret_key` (str, optional) - secret key to sign and verify upload requests.
* `session_timeout_seconds` (int, optional)- session lifetime, in seconds, after user disconnected.
* `oauth_state_timeout_seconds` (int, optional) - OAuth state lifetime, in seconds, which is a maximum allowed time between starting OAuth flow and redirecting to OAuth callback URL.

### Hosting multiple Flet apps under the same domain

```python
import flet as ft
import flet.fastapi as flet_fastapi


async def root_main(page: ft.Page):
    await page.add_async(ft.Text("This is root app!"))


async def sub_main(page: ft.Page):
    await page.add_async(ft.Text("This is sub app!"))


app = flet_fastapi.FastAPI()


app.mount("/sub-app", flet_fastapi.app(sub_main))
app.mount("/", flet_fastapi.app(root_main))
```

Sub-apps must be mapped before the root Flet app as it configures catch-all `index.html` for SPA.

Run the app with `uvicorn` and visit http://127.0.0.1:8000 and then http://127.0.0.1:8000/sub-app/ to see both Flet apps running.

::warning
Notice the trailing slash in `/sub-app/` URL - without the slash the request will be routed to a root app.
::

### Adding Flet to the existing FastAPI app

```python
from contextlib import asynccontextmanager

import flet as ft
import flet.fastapi as flet_fastapi
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    await flet_fastapi.app_manager.start()
    yield
    await flet_fastapi.app_manager.shutdown()

app = FastAPI(lifespan=lifespan)

async def main(page: ft.Page):
    await page.add_async(ft.Text("Hello, Flet!"))

app.mount("/flet-app", flet_fastapi.app(main))
```

When adding Flet app to the existing FastAPI app you need to call `flet_fastapi.app_manager.start()` on app start and `flet_fastapi.app_manager.shutdown()` on shutdown. Use the way that best suites you: lifespan (in the example above) or app events.

`app_manager.start()` method starts background tasks cleaning up expired sessions and OAuth flow states.

`app_manager.shutdown()` method removes any temporary files created by a Flet app.

### Configuring individual Flet endpoints

#### Static files

A FastAPI app to serve static Flet app files (index.html, manifest.json, Flutter JS app, etc.) and user assets.

```python
from flet.fastapi import FastAPI, FletStaticFiles

app = FastAPI()

# mount to the root of web app
app.mount(path="/", app=FletStaticFiles())
```

Parameters of `FletStaticFiles` constructor:

* `app_mount_path` (str) - absolute URL of Flet app. Default is `/`.
* `assets_dir` (str, optional) - an absolute path to app's assets directory.
* `app_name` (str, optional) - PWA application name.
* `app_short_name` (str, optional) - PWA application short name.
* `app_description` (str, optional) - PWA application description.
* `web_renderer` (WebRenderer) - web renderer defaulting to `WebRenderer.CANVAS_KIT`.
* `use_color_emoji` (bool) - whether to load a font with color emoji. Default is `False`.
* `route_url_strategy` (str) - routing URL strategy: `path` (default) or `hash`.
* `websocket_endpoint_path` (str, optional) - absolute URL of Flet app WebSocket handler. Default is `{app_mount_path}/ws`.

#### WebSocket handler

Handles WebSocket connections from Flet client app running in the browser. WebSocket channel is used to send events from a browser to a Flet backend code and receive page real-time incremential updates.

```python
from flet.fastapi import FletApp

async def main(page: ft.Page):
    await page.add_async(ft.Text("Hello, Flet!"))

@app.websocket("/app1/ws")
async def flet_app(websocket: WebSocket):
    await FletApp(main).handle(websocket)
```

* `session_handler` (Coroutine) - application entry point - an async method called for newly connected user. Handler coroutine must have 1 parameter: `page` - `Page` instance.
* `session_timeout_seconds` (int, optional) - session lifetime, in seconds, after user disconnected.
* `oauth_state_timeout_seconds` (int, optional) - OAuth state lifetime, in seconds, which is a maximum allowed time between starting OAuth flow and redirecting to OAuth callback URL.
* `upload_endpoint_path` (str, optional) - absolute URL of upload endpoint, e.g. `/upload`.
* `secret_key` (str, optional) - secret key to sign upload requests.

#### Uploads handler

Handles file uploads by [`FilePicker`][flet.FilePicker] control.
This endpoint is optional - if your app doesn't use [`FilePicker`][flet.FilePicker] then it's not needed.

```python
from flet.fastapi import FletUpload

@app.put("/upload")
async def flet_uploads(request: Request):
    await FletUpload("/Users/feodor/Downloads/123").handle(request)
```

#### OAuth callback handler

Handles OAuth flow callback requests. If your app doesn't use [authentication](../../../cookbook/authentication.md) then
this endpoint is not needed.

```python
from flet.fastapi import FletOAuth

@app.get("/oauth_callback")
async def flet_oauth(request: Request):
    return await FletOAuth().handle(request)
```
