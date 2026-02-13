---
title: Fly.io
---

[Fly.io](https://fly.io) works well for Flet apps: it supports WebSockets, deploys close to users via multiple [regions](https://fly.io/docs/reference/regions/), and has a [free tier](https://fly.io/docs/about/pricing/#free-allowances) suitable for small projects.

## Prerequisites

1. Install [flyctl](https://fly.io/docs/getting-started/installing-flyctl/).
2. Authenticate:

```bash
fly auth login
```

## Project files

Place the following files in your app directory.

### `requirements.txt`

At minimum:

```txt title="requirements.txt"
flet
```

### `fly.toml`

Fly app configuration:

```toml title="fly.toml"
app = "<your-app-name>"

kill_signal = "SIGINT"
kill_timeout = 5
processes = []

[env]
  FLET_SESSION_TIMEOUT = "60"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

  [http_service.concurrency]
    type = "connections"
    soft_limit = 200
    hard_limit = 250
```

- Replace `<your-app-name>` with the app name you want. It will also be used in the final
    URL of your app, in the form, `https://<your-app-name>.fly.dev`.
- `internal_port` must correspond to the [`FLET_SERVER_PORT`](../../../../reference/environment-variables.md#flet_server_port), which is `8000` by default.
- [`FLET_SESSION_TIMEOUT`](../../../../reference/environment-variables.md#flet_session_timeout) controls session lifetime (seconds).
- For other variables, see [environment variables reference](../../../../reference/environment-variables.md).

### `Dockerfile`

Create a `Dockerfile` containing the commands to build your application container,
for example:

```Dockerfile title="Dockerfile"
FROM python:3-alpine

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
```

`main.py` is the app's [entry point](../../../index.md#entry-point). If your file name differs, update accordingly.

/// admonition | Info
    type: info
Fly.io deploys apps as Docker containers and provides a free remote Docker builder,
so you don’t need Docker installed locally.
///

## Deploy

From your app directory:

1. Create the Fly app:
    ```bash
    fly apps create --name <your-app-name>
    ```

2. Deploy:
    ```bash
    fly deploy
    ```

3. Open app in browser:
    ```bash
    fly apps open
    ```
