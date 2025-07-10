---
title: publish
sidebar_label: publish
---

This command is used to publish a Flet application as a standalone static web app using Pyodide. You can find it's guide [here](/docs/publish/web/static-website).

```
usage: flet publish [-h] [-v] [--pre] [-a ASSETS_DIR] [--distpath DISTPATH] [--app-name APP_NAME] [--app-short-name APP_SHORT_NAME] [--app-description APP_DESCRIPTION] [--base-url BASE_URL]
                    [--web-renderer {canvaskit,html}] [--use-color-emoji] [--route-url-strategy {path,hash}]
                    script

Publish Flet app as a standalone web app.

positional arguments:
  script                path to a Python script

options:
  -h, --help            show this help message and exit
  -v, --verbose         -v for detailed output and -vv for more detailed
  --pre                 allow micropip to install pre-release Python packages
  -a ASSETS_DIR, --assets ASSETS_DIR
                        path to an assets directory
  --distpath DISTPATH   where to put the published app (default: ./dist)
  --app-name APP_NAME   application name
  --app-short-name APP_SHORT_NAME
                        application short name
  --app-description APP_DESCRIPTION
                        application description
  --base-url BASE_URL   base URL for the app
  --web-renderer {canvaskit,html}
                        web renderer to use
  --use-color-emoji     enables color emojis with CanvasKit renderer
  --route-url-strategy {path,hash}
                        URL routing strategy
```