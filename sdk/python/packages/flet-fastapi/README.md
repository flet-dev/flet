# Flet - a better UI for FastAPI

Flet for FastAPI allows adding interactive real-time dashboards for your FastAPI services as well as host any Flet web app inside FastAPI with production-grade reliability.

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
        await counter.update_async()

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.icons.ADD, on_click=add_click
    )
    await page.add_async(
        ft.Container(counter, alignment=ft.alignment.center, expand=True)
    )

app = flet_fastapi.app(main)
```

That's a simple app displaying a counter and a button at the right bottom to increment that counter.

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

`FLET_SECRET_KEY`

`FLET_SESSION_TIMEOUT` - seconds, defaulting to 3,600 seconds.

`FLET_OAUTH_STATE_TIMEOUT` - seconds, defaulting to 600 seconds.

`FLET_MAX_UPLOAD_SIZE` - max allowed size of an uploaded file, bytes.