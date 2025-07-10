---
title: run
sidebar_label: run
---

This command is used to run a Flet application in hot reload mode.

```
usage: flet run [-h] [-v] [-p PORT] [--host HOST] [--name APP_NAME] [-m] [-d] [-r] [-n] [-w] [--ios] [--android] [-a ASSETS_DIR] [--ignore-dirs IGNORE_DIRS] [script]

Run Flet app.

positional arguments:
  script                path to a Python script

options:
  -h, --help            show this help message and exit
  -v, --verbose         -v for detailed output and -vv for more detailed
  -p PORT, --port PORT  custom TCP port to run Flet app on
  --host HOST           host to run Flet web app on. Use "*" to listen on all IPs.
  --name APP_NAME       app name to distinguish it from other on the same port
  -m, --module          treat the script as a python module path as opposed to a file path
  -d, --directory       watch script directory
  -r, --recursive       watch script directory and all sub-directories recursively
  -n, --hidden          application window is hidden on startup
  -w, --web             open app in a web browser
  --ios                 open app on iOS device
  --android             open app on Android device
  -a ASSETS_DIR, --assets ASSETS_DIR
                        path to assets directory
  --ignore-dirs IGNORE_DIRS
                        directories to ignore during watch. If more than one, separate with a comma.
```
