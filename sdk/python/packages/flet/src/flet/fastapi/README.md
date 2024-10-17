# Flet - a better UI for FastAPI

Flet for FastAPI allows adding interactive real-time dashboards to your FastAPI app as well as host any Flet web app inside FastAPI with production-grade reliability.

## Installation

```
pip install flet-fastapi
```

## First app

Create `counter.py` with the following content:

```python
import flet as ft
import flet_fastapi

async def main(page: ft.Page):
    counter = ft.Text("0", size=50, data=0)

    async def add_click(e):
        counter.data += 1
        counter.value = str(counter.data)
        counter.update()

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.icons.ADD, on_click=add_click
    )
    await page.add_async(
        ft.Container(counter, alignment=ft.alignment.center, expand=True)
    )

app = flet_fastapi.app(main)
```

That's a simple app displaying a counter and a button at the right bottom to increment that counter.

`flet_fastapi.app()` configures a single Flet app at the root of FastAPI app with `main()` sessions handler and the following endpoints:

`/ws` (WS) - WebSocket handler for the Flet app.

`/upload` (PUT) - file uploads handler.

`/oauth_callback` (GET) - OAuth flow callback handler.

`/` (GET) - Flet app static files with SPA catch-all handler.

## Running the app locally

Install [Uvicorn](https://www.uvicorn.org/) web server:

```
pip install uvicorn
```

Start `uvicorn` with:

```
uvicorn counter:app
```

Open the browser and navigate to http://127.0.0.1:8000 to see the app running.

## Hosting multiple Flet apps under the same domain

```python
import flet as ft
import flet_fastapi


async def root_main(page: ft.Page):
    await page.add_async(ft.Text("This is root app!"))


async def sub_main(page: ft.Page):
    await page.add_async(ft.Text("This is sub app!"))


app = flet_fastapi.FastAPI()


app.mount("/sub-app", flet_fastapi.app(sub_main))
app.mount("/", flet_fastapi.app(root_main))
```

Sub-apps must be mapped before the root Flet app as it configures catch-all `index.html` for SPA.

Run the app with `uvicorn` and visit http://127.0.0.1:8000 and then http://127.0.0.1:8000/sub-app/ to see both Flet apps running. Notice the trailing slash in `/sub-app/` URL - without the slash the request will be routed to a root app.

## Adding Flet to the existing FastAPI app

```python
from contextlib import asynccontextmanager

import flet as ft
import flet_fastapi
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

## Running the app in production

It is recommended to run FastAPI in production with [Hypercorn](https://github.com/pgjones/hypercorn/) which is ASGI web server, but it is also possible to run FastAPI apps with [Gunicorn](https://gunicorn.org/) which is a WSGI server, but has more features, like passing proxy headers.

To install Gunicorn:

```
pip install gunicorn
```

Start `gunicorn` with:

```
gunicorn -k uvicorn.workers.UvicornWorker counter:app
```

## Reference

### Environment variables

`FLET_SECRET_KEY` - secret key to sign upload requests. Must be set if upload directory is configured.

`FLET_SESSION_TIMEOUT` - the number of seconds to keep session alive after user has disconnected. Default is 3,600 seconds.

`FLET_OAUTH_STATE_TIMEOUT` - OAuth state lifetime, in seconds, which is a maximum allowed time between starting OAuth flow and redirecting to OAuth callback URL. Default is 600 seconds.

`FLET_MAX_UPLOAD_SIZE` - max allowed size of an uploaded file, bytes.