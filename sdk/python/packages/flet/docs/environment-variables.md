---
title: Environment variables
---

Below is the list of useful environment variables and their default values:

#### `FLET_APP_CONSOLE` 

The path to the application's console log file (`console.log`) in the temporary storage directory.

Its value is set in production mode.

#### `FLET_APP_STORAGE_DATA`

A directory for the storage of persistent application data that is preserved between app updates. 
It is already pre-created and its location depends on the platform the app is running on.

#### `FLET_APP_STORAGE_TEMP`

A directory for the storage of temporary application files, i.e. cache. 
It is already pre-created and its location depends on the platform the app is running on.

#### `FLET_ASSETS_DIR`

Absolute path to app "assets" directory.

Defaults to `assets`.

#### `FLET_CLI_NO_RICH_OUTPUT`

Whether to disable rich output in the console.

Default is `"false"`.

#### `FLET_PLATFORM` 

The platform on which the application is running. 
Its value is one of the following: `"android"`, `"ios"`, `"linux"`, `"macos"`, `"windows"` or `"fuchsia"`.

#### `FLET_CLI_SKIP_FLUTTER_DOCTOR`

Whether to skip running `flutter doctor` when a build fails. 

Default is `False`.

#### `FLET_FORCE_WEB_SERVER`

Set to `true` to force running app as a web app. Automatically set on headless Linux hosts.

#### `FLET_OAUTH_CALLBACK_HANDLER_ENDPOINT`

Custom path for OAuth handler.

Defaults to `/oauth_callback`.

#### `FLET_OAUTH_STATE_TIMEOUT`

Maximum allowed time (in seconds) to complete OAuth web flow.

Defaults to `600`.

#### `FLET_MAX_UPLOAD_SIZE`

Maximum allowed size (in bytes) of uploaded files.

Default is unlimited.

#### `FLET_SECRET_KEY`

A secret key to sign temporary upload URLs.

#### `FLET_SERVER_IP`

IP address to listen web app on, e.g. `127.0.0.1`.

Defaults to `0.0.0.0` - bound to all server IPs.

#### `FLET_SERVER_PORT`

TCP port to run app on. `8000` if the program is running on a Linux server or `FLET_FORCE_WEB_SERVER` is set; otherwise
random port.

#### `FLET_SERVER_UDS_PATH` 

The Unix Domain Socket (UDS) path for the Flet server. It enables inter-process communication on Unix-based systems, with its value being a socket file path in the format `flet_<pid>.sock`.

#### `FLET_SESSION_TIMEOUT`

Session lifetime in seconds. Default is `3600`.

#### `FLET_UPLOAD_DIR`

Absolute path to app "upload" directory.

#### `FLET_UPLOAD_HANDLER_ENDPOINT`

Custom path for upload handler. Default is `/upload`.

#### `FLET_WEB_APP_PATH`

A URL path after domain name to host web app under, e.g. `/apps/myapp`. Default is `/` - host app in the root.

#### `FLET_WEBSOCKET_HANDLER_ENDPOINT`

Custom path for WebSocket handler. Default is `/ws`.

#### `FLET_WEB_RENDERER`

Web rendering mode: `canvaskit` (default), `html` or `auto`.

#### `FLET_WEB_USE_COLOR_EMOJI`

Set to `True`, `true` or `1` to load web font with colorful emojis.

#### `FLET_WEB_ROUTE_URL_STRATEGY`

The URL strategy of the web application: `path` (default) or `hash`.

## Setting Boolean values

The boolean `True` is represented by one of the following string values: `"true"`, `"1"` or `"yes"`. 
Any other value will be interpreted as `False`.
