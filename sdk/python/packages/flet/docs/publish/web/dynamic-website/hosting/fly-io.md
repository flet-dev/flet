---
title: Fly.io
---

[Fly.io](https://fly.io) has robust WebSocket support and can deploy your app to a [data center](https://fly.io/docs/reference/regions/) that is close to your users. They have very attractive pricing with a [generous free tier](https://fly.io/docs/about/pricing/#free-allowances) which allows you to host up to 3 applications for free.

To get started with Fly install [flyctl](https://fly.io/docs/getting-started/installing-flyctl/) and then authenticate:

    fly auth login

To deploy the app with `flyctl` you have to add the following 3 files into the folder with your Python app.

Create `requirements.txt` with a list of application dependencies. At minimum it should contain `flet` module:

```txt title="requirements.txt"
flet
```

Create `fly.toml` describing Fly application:

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

Replace `<your-app-name>` with desired application name which will be also used in application URL, such as `https://<your-app-name>.fly.dev`.

By default, Flet web app will be running on port `8000`, but you can change that by setting up `FLET_SERVER_PORT` environment variable.

`FLET_SESSION_TIMEOUT` is a user session lifetime, in seconds.

[Complete list of environment variables](../../../../publish/web/dynamic-website/index.md#environment-variables) supported by a web app.

Create `Dockerfile` containing the commands to build your application container:

```Dockerfile title="Dockerfile"
FROM python:3-alpine

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
```

`main.py` is a file with your Python program.

::note
Fly.io deploys every app as a Docker container, but a great thing about Fly is that it provides a free remote Docker builder, so you don't need Docker installed on your machine.
::

Next, switch command line to a folder with your app and run the following command to create and initialize a new Fly app:

```
fly apps create --name <your-app-name>
```

Deploy the app by running:

```
fly deploy
```

That's it! Open your app in the browser by running:

```
fly apps open
```