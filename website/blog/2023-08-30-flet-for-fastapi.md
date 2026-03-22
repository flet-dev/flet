---
slug: flet-for-fastapi
title: Flet for FastAPI
authors: feodor
tags: [releases]
---

We've just released Flet 0.10.0 with FastAPI support!

<img src="/img/blog/fastapi/fastapi-logo-teal.png" className="screenshot-60" />

[FastAPI](https://fastapi.tiangolo.com/) coupled with Uvicorn, Hypercorn, Gunicorn or other web server replaces built-in Flet web server (Fletd) to reliably run production Flet workloads.

On the other hand, seasoned FastAPI developers can use Flet to easily add interactive, real-time dashboards and admin UI to their existing or new FastAPI services.

<!-- truncate -->

## A minimal app example

```python
import flet as ft
import flet_fastapi

async def main(page: ft.Page):
    await page.add_async(
        ft.Text("Hello, Flet!")
    )

app = flet_fastapi.app(main)
```

It's a simple app that just outputs "Hello, Flet!" on a web page.

To run the app install Flet for FastAPI and Uvicorn:

```
pip install flet-fastapi
pip install uvicorn
```

Save the code above to `hello.py` and then start uvicorn as:

```
uvicorn hello:app
```

Open the browser and navigate to http://127.0.0.1:8000 to see the app running.

:::note
Flet app must be [async](https://docs.flet.dev/cookbook/async-apps/) in order to work with FastAPI WebSocket handler.
:::

## Features and benefits

* [Multiple Flet apps on a single domain](https://docs.flet.dev/publish/web/dynamic-website/#hosting-multiple-flet-apps-under-the-same-domain) - mapped to the root and/or sub-paths.
* Simple [one-line mappings](https://docs.flet.dev/publish/web/dynamic-website/#flet-fastapi-app) or [individual endpoint configurations](https://docs.flet.dev/publish/web/dynamic-website/#configuring-individual-flet-endpoints).
* Light-weight async wrapper around FastAPI WebSocket connection for greater concurrency.
* Serves Flet static files with user assets and app meta-information customization.
* Uploads handler for `FilePicker` control.
* OAuth callback handler for authentication flows.

Check [the guide](https://docs.flet.dev/publish/web/dynamic-website/) for complete information about Flet with FastAPI.

Let us know what you think by joining [Flet Discord server](https://discord.gg/dzWXP8SHG8) or creating a new thread on [Flet GitHub discussions](https://github.com/flet-dev/flet/discussions).