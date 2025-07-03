Host a Flet app on your own server with NGINX.

There are free and inexpensive cloud server tiers available at [AWS](https://aws.amazon.com/free/), [Oracle](https://www.oracle.com/cloud/free/), [Linode](https://www.linode.com/pricing/), and more.

## Setup Flet Environment

### `requirements.txt` and virtualenv

Create `requirements.txt` with a list of application dependencies. At minimum it should contain `flet` module:

```txt
flet
```

Create a virtualenv and install requirements:

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Sample Flet app

```python
import flet as ft

def main(page: ft.Page):
    page.title = "My Flet app"
    page.add(ft.Text("Hello, world!"))

if __name__ == "__main__":
    ft.run(main)
```

Flet app will be served from the root URL, but you can configure `FLET_WEB_APP_PATH` environment variable
to serve beneath the root e.g. `/apps/myapp`.

By default, Flet web app will be running on port `8000`, but you can change that by setting up `FLET_SERVER_PORT` environment variable.

[Complete list of environment variables](../../../../publish/web/dynamic-website/index.md#environment-variables) supported by a web app.

## Automatically start Flet app

### Create `systemd` unit file

Automatically start the Flet app using a `systemd` service unit file `flet.service`.

Setup below assumes your Flet app script is defined in `$HOME/flet-app/main.py`. Replace `User`, `Group`, `WorkingDirectory`, etc. as per your setup.

```ini
[Unit]
Description=Flet App
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/flet-app
Environment="PATH=/home/ubuntu/flet-app/.venv/bin"
ExecStart=/home/ubuntu/flet-app/.venv/bin/python /home/ubuntu/flet-app/main.py

[Install]
WantedBy=multi-user.target
```

### Enable Flet app service

```
cd /etc/systemd/system
sudo ln -s /home/ubuntu/flet-app/flet.service
sudo systemctl start flet
sudo systemctl enable flet
sudo systemctl status flet
```

## NGINX Proxy Setup

NGINX will proxy the Flet app and the websocket.

In your `/etc/nginx/sites-available/*` config file, updating path and port as needed:

```txt
    location / {
        proxy_pass         http://127.0.0.1:8000/;
        proxy_http_version 1.1;
        proxy_set_header   Upgrade $http_upgrade;
        proxy_set_header   Connection keep-alive;
        proxy_set_header   Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
    }
  
    location /ws {
        proxy_pass         http://127.0.0.1:8000/ws;
        proxy_http_version 1.1;
        proxy_set_header   Upgrade $http_upgrade;
        proxy_set_header   Connection "upgrade";
        proxy_set_header   Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
    }
```

That's it! Restart NGINX, and open your app in a browser.
