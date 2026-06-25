---
title: "Environment Variables"
---

:::tip[Setting boolean values]
To set a boolean `True`, use one of the following string values: `"true"`, `"1"` or `"yes"`.
Any other value will be interpreted as `False`.
:::

### `FLET_APP_CONSOLE`

The path to the application's console log file (`console.log`) in the cache storage directory
([`FLET_APP_STORAGE_CACHE`](#flet_app_storage_cache)).

Its value is set in production mode.

:::info
In a running Flet app, the equivalent of this environment variable is
[`StoragePaths.get_console_log_filename()`][flet.StoragePaths.get_console_log_filename].
:::

### `FLET_APP_STORAGE_DATA`

A directory for **durable** application data — databases, state, config — that is preserved between
app updates, backed up by the OS, and never auto-deleted. It is pre-created, app-private, and its
location depends on the platform (it maps to the platform's *application support* directory:
`%APPDATA%\<company>\<product>\data` on Windows, `~/Library/Application Support/<bundle-id>/data` on
macOS, `~/.local/share/<app-id>/data` on Linux, the app-sandboxed support dir on iOS/Android).

In production this directory is also the Python program's **current working directory**, so relative
file writes (e.g. `open("app.db", "w")`, `sqlite3.connect("app.db")`) land here. In `flet run` (dev
mode) it is `<project>/.flet/storage/data`.

:::info
In a running Flet app, this maps to a `data` subdirectory of
[`StoragePaths.get_application_support_directory()`][flet.StoragePaths.get_application_support_directory].
:::

### `FLET_APP_STORAGE_CACHE`

A directory for **regenerable** cached data. The OS may purge it under storage pressure (and the
platform "clear cache" action wipes it), so only store things you can rebuild. Pre-created and
app-private; it maps to the platform's *caches* directory (`%LOCALAPPDATA%\<company>\<product>` on
Windows, `~/Library/Caches/<bundle-id>` on macOS, `~/.cache/<app-id>` on Linux, the app cache dir on
iOS/Android). In `flet run` it is `<project>/.flet/storage/cache`.

:::info
In a running Flet app, the equivalent of this environment variable is
[`StoragePaths.get_application_cache_directory()`][flet.StoragePaths.get_application_cache_directory].
:::

### `FLET_APP_STORAGE_TEMP`

A directory for **throwaway** temporary files — the OS temporary directory (`getTemporaryDirectory()`).
It is the most volatile of the three and may be cleared between launches, so don't rely on its contents
persisting. (On Android it resolves to the same directory as
[`FLET_APP_STORAGE_CACHE`](#flet_app_storage_cache).) In `flet run` it is `<project>/.flet/storage/temp`,
and Python's `tempfile` is pointed here too (via `TMPDIR`). Equivalent to Python's
`tempfile.gettempdir()`.

:::info
In a running Flet app, the equivalent of this environment variable is
[`StoragePaths.get_temporary_directory()`][flet.StoragePaths.get_temporary_directory].
:::

### `FLET_APP_USER_MODEL_ID`

Windows [AppUserModelID](https://learn.microsoft.com/en-us/windows/win32/shell/appids)
used by the desktop client process for taskbar grouping and pinning.

For apps packaged with [`flet pack`](../cli/flet-pack.md), this value is set automatically
so taskbar pins point to the packaged app executable instead of the cached Flet client executable.

### `FLET_ASSETS_DIR`

Absolute path to the app's assets directory.

In production apps built with [`flet build`](../publish/index.md), this environment-variable points to the bundled assets absolute location at runtime.
Use it when your code needs a filesystem path to bundled files (for example, JSON configs, databases, or model files).

For local runs, it may be unset depending on how the app is started, so use a fallback:

```python
import os
from pathlib import Path
import flet as ft

default_assets_dir = Path(__file__).parent / "assets"
assets_dir = Path(os.environ.get("FLET_ASSETS_DIR", str(default_assets_dir))).resolve()

def main(page: ft.Page):
	...

ft.run(main, assets_dir="assets")
```

For control properties like [`Image.src`](../controls/image.md#flet.Image.src), continue using paths relative
to the `ft.run(assets_dir=...)`, as described in the [assets cookbook](../cookbook/assets.md).

### `FLET_ANDROID_SIGNING_KEY_ALIAS`

Android signing key alias used by
[`flet build`](../publish/android.md#key-alias) for Android app signing.

It is used only when a [keystore](../publish/android.md#key-store) is configured.

### `FLET_ANDROID_SIGNING_KEY_PASSWORD`

Android signing key password used by
[`flet build`](../publish/android.md#key-password) for Android app signing.

If [`FLET_ANDROID_SIGNING_KEY_STORE_PASSWORD`](#flet_android_signing_key_store_password) is set
but this variable is not, the keystore password is reused as the key password.

### `FLET_ANDROID_SIGNING_KEY_STORE`

Path to the Android upload keystore (`.jks`) used by [`flet build`](../publish/android.md#key-store)
for Android app signing.

### `FLET_ANDROID_SIGNING_KEY_STORE_PASSWORD`

Android signing keystore password used by
[`flet build`](../publish/android.md#key-store-password) for Android app signing.

If [`FLET_ANDROID_SIGNING_KEY_PASSWORD`](#flet_android_signing_key_password) is set
but this variable is not, the key password is reused as the keystore password.

### `FLET_CLI_NO_RICH_OUTPUT`

Whether to disable rich output in the console.

Defaults to `"false"`.

### `FLET_PLATFORM`

The platform on which the application is running.
Its value is one of the following: `"android"`, `"ios"`, `"linux"`, `"macos"`, `"windows"` or `"fuchsia"`.

### `FLET_CLI_SKIP_FLUTTER_DOCTOR`

Whether to skip running `flutter doctor` when a build fails.

Defaults to `False`.

### `FLET_HIDE_WINDOW_ON_START`

Set to `true` to start app with the main window hidden.

Defaults to `False`.

### `FLET_FORCE_WEB_SERVER`

Set to `true` to force running app as a web app. Automatically set on headless Linux hosts.

### `FLET_OAUTH_CALLBACK_HANDLER_ENDPOINT`

Custom path for OAuth handler.

Defaults to `"/oauth_callback"`.

### `FLET_OAUTH_STATE_TIMEOUT`

Maximum allowed time (in seconds) to complete OAuth web flow.

Defaults to `600`.

### `FLET_MAX_UPLOAD_SIZE`

Maximum allowed size (in bytes) of uploaded files.

Default is unlimited.

### `FLET_SECRET_KEY`

A secret key to sign temporary upload URLs.

### `FLET_SERVER_IP`

IP address to listen web app on, e.g. `"127.0.0.1"`.

Defaults to `0.0.0.0` - bound to all server IPs.

### `FLET_SERVER_PORT`

TCP port to run app on.

`8000` if the program is running on a Linux server or [`FLET_FORCE_WEB_SERVER`](#flet_force_web_server) is set; otherwise
random port.

### `FLET_SERVER_UDS_PATH`

The Unix Domain Socket (UDS) path for the Flet server. It enables inter-process communication on Unix-based systems, with its value being a socket file path in the format `flet_<pid>.sock`.

### `FLET_SESSION_TIMEOUT`

Session lifetime in seconds.

Defaults to `3600`.

### `FLET_UPLOAD_DIR`

Absolute path to app "upload" directory.

### `FLET_UPLOAD_HANDLER_ENDPOINT`

Custom path for upload handler.

Defaults to `"/upload"`.

### `FLET_WEB_APP_PATH`

A URL path after domain name to host web app under, e.g. `"/apps/myapp"`.

Defaults to `"/"` - host app in the root.

### `FLET_WEB_NO_CDN`

Set to `true` to avoid loading CanvasKit, Pyodide, and fonts from CDNs.

### `FLET_WEBSOCKET_HANDLER_ENDPOINT`

Custom path for WebSocket handler.

Defaults to `"/ws"`.

### `FLET_WEB_RENDERER`

Web rendering mode: `"canvaskit"` (default), `"skwasm"` or `"auto"`.

### `FLET_WEB_USE_COLOR_EMOJI`

Set to `True`, `true` or `1` to load web font with colorful emojis.

### `FLET_WEB_ROUTE_URL_STRATEGY`

The URL strategy of the web application. Its value can be either `"path"` (default) or `"hash"`.
