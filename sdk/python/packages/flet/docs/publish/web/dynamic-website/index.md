Flet runs your app as a [FastAPI](https://fastapi.tiangolo.com/) (ASGI) app
to serve a dynamic website.

It uses [Uvicorn](https://www.uvicorn.org/) by default, but any ASGI-compatible server can be used instead.

### Sync and async handlers

In a Flet web app you can mix sync and async handlers.

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
        ft.Button("Call handler", on_click=handler),
        ft.Button("Call async handler", on_click=handler_async)
    )

ft.run(main)
```

In the example, a click on one button is handled by a blocking handler while a click
on the second button calls an async handler. The first handler runs in a
`threading.Thread`, while the second runs as an `asyncio.Task`.

In web apps, threads are a finite resource. A thread pool is usually used and can
become a bottleneck as the number of users grows.

If your app is mostly doing I/O (database, web API) and you can use async-ready
libraries, prefer async handlers.

Check [FastAPI's article about async/await](https://fastapi.tiangolo.com/async/) to better understand the differences between concurrency and parallelism.

## Running the app locally

Use `--web` (`-w`) option to start a Flet app as a web app:

```bash
flet run --web app.py
```

A new browser window/tab will be opened and the app will use a random TCP port.

To run on a fixed port use `--port` (`-p`):

```bash
flet run --web --port 8000 app.py
```

## Running the app in production

You can run your program directly with `python`:

```bash
python app.py
```

[Uvicorn](https://www.uvicorn.org/) web server is used by default to host the web app.

If Flet detects a headless Linux environment (such as a Docker container
or EC2 VM):
1. Port `8000` will be used to run the app.
2. A browser window will not be opened.

If Flet cannot detect a headless environment, you can force that behavior
by defining the following environment variable:

```bash
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

```bash
hypercorn main:app --bind 0.0.0.0:8000
```

#### Daphne

[Daphne](https://github.com/django/daphne) is a HTTP, HTTP2 and WebSocket protocol server for ASGI and ASGI-HTTP, developed to power Django Channels.

To run the app with Daphne:

```bash
daphne -b 0.0.0.0 -p 8000 main:app
```

#### Gunicorn

[Gunicorn](https://gunicorn.org/) is popular web server to run Python web applications. While it implements WSGI specification it's possible to run ASGI FastAPI apps with a [worker process class](https://fastapi.tiangolo.com/deployment/server-workers/) provided by Uvicorn:

```bash
gunicorn --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker counter:app
```

## Assets

When you open a Flet app in the browser, its `index.html`, Flutter engine,
favicon, images and other web app resources are served by a web server.
These resources are bundled with `flet` Python package. However, there are
situations when you need to modify the contents of certain files to customize
the appearance of your app or its behavior, for example:

* Favicon.
* App loading animation.
* `manifest.json` with PWA details.

You can specify `assets_dir` in `flet.run()` to set the location of assets that
should be available to the application. `assets_dir` should be relative to
your `main.py` directory or an absolute path.
Default value for `assets_dir` argument is `assets`.

For example, consider the following program structure:

```
/assets
   /images/my-image.png
main.py
```

You can access your images in the application as follows:

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

To override the Flet animation image, put `icons/loading-animation.png` with your own app logo
in the root of the assets directory.

#### PWA

Progressive Web Apps, or PWAs, offer a way to turn app-like websites into website-like apps.

Check [PWAs Turn Websites Into Apps: Here's How](https://www.pcmag.com/how-to/how-to-use-progressive-web-apps) for the PWA introduction.

Browsers that support PWA ([installation instructions](#pwa)):

* **Chrome** on all platforms
* **Edge** on all platforms
* **Firefox** on Android
* **Safari** on iOS and iPadOS

/// admonition | Info
  type: info
The information in this section is based on the following sources (check them out for more details):

* [General information about PWAs](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)
* [PWA manifests](https://developer.mozilla.org/en-US/docs/Web/Manifest)
///

#### Manifest

You can change PWA's name, description, colors and other information in `manifest.json` that must be put
in the root of `assets` directory.

Here are the links to the most common manifest items that you'd like to customize:

* [`name`](https://developer.mozilla.org/en-US/docs/Web/Manifest/name) - the name of the web application as it is usually displayed to the user.
* [`short_name`](https://developer.mozilla.org/en-US/docs/Web/Manifest/short_name) - the name of the web application displayed to the user if there is not enough space to display `name`.
* [`description`](https://developer.mozilla.org/en-US/docs/Web/Manifest/description) - explains what the application does.
* [`theme_color`](https://developer.mozilla.org/en-US/docs/Web/Manifest/theme_color) - defines the default theme color for the application.
* [`background_color`](https://developer.mozilla.org/en-US/docs/Web/Manifest/background_color) - defines a placeholder background color for the application page to display before its stylesheet is loaded.

#### Icons

Custom icons should be placed in `assets/icons` directory:

* `icon-192.png`, `icon-512.png` - app icons displayed in Windows taskbar.
* `icon-maskable-192.png`, `icon-maskable-512.png` - app icons displayed in Android.
* `apple-touch-icon-192.png` - app icon displayed in iOS.

## Environment variables

Every aspect of web app hosting can be additionally controlled
with [environment variables](../../../reference/environment-variables.md).

## Advanced FastAPI scenarios

### Flet FastAPI app

- `flet.fastapi.app()` creates a FastAPI application to handle Flet sessions and
  mounts the following endpoints at the app root:
  - `/ws` (WS) - WebSocket handler for the Flet app. It calls `main()` when a new
  WebSocket connection is established and a new app session is created.
- `/upload` (PUT) - file uploads handler.
- `/oauth_callback` (GET) - OAuth flow callback handler.
- `/` (GET) - Flet app static files with SPA catch-all handler.

### Hosting multiple Flet apps under the same domain

```python
import flet as ft
import flet.fastapi as flet_fastapi

async def root_main(page: ft.Page):
    page.add(ft.Text("This is root app!"))

async def sub_main(page: ft.Page):
    page.add(ft.Text("This is sub app!"))

app = flet_fastapi.FastAPI()

app.mount("/sub-app", flet_fastapi.app(sub_main))
app.mount("/", flet_fastapi.app(root_main))
```

Sub-apps must be mapped before the root Flet app as it configures catch-all `index.html` for SPA.

Run the app with `uvicorn` and visit http://127.0.0.1:8000 and
then http://127.0.0.1:8000/sub-app/ to see both Flet apps running.

Notice the trailing slash in `/sub-app/` - without it the request will be routed to the root app.

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
    page.add(ft.Text("Hello, Flet!"))

app.mount("/flet-app", flet_fastapi.app(main))
```

When adding a Flet app to an existing FastAPI app you need to call
`flet_fastapi.app_manager.start()` on app start and
`flet_fastapi.app_manager.shutdown()` on shutdown. Use the way that best suits you:
lifespan (in the example above) or app events.

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

#### WebSocket handler

Handles WebSocket connections from the Flet client running in the browser. The WebSocket
channel is used to send events from the browser to the backend and receive page updates.

```python
import asyncio
import flet as ft
from flet.fastapi import FletApp, app_manager

async def main(page: ft.Page):
    page.add(ft.Text("Hello, Flet!"))

@app.websocket("/app1/ws")
async def flet_app(websocket: WebSocket):
    await FletApp(
        loop=asyncio.get_running_loop(),
        executor=app_manager.executor,
        main=main,
        before_main=None,
    ).handle(websocket)
```

#### Uploads handler

Handles file uploads by [`FilePicker`][flet.FilePicker] control.
This endpoint is optional - if your app doesn't use
[`FilePicker`][flet.FilePicker], then it's unnecessary.

```python
from flet.fastapi import FletUpload

@app.put("/upload")
async def flet_uploads(request: Request):
    await FletUpload("/Users/feodor/Downloads/123").handle(request)
```

#### OAuth callback handler

Handles OAuth flow callback requests. If your app doesn't use
[authentication](../../../cookbook/authentication.md), then this endpoint is unnecessary.

```python
from flet.fastapi import FletOAuth

@app.get("/oauth_callback")
async def flet_oauth(request: Request):
    return await FletOAuth().handle(request)
```
