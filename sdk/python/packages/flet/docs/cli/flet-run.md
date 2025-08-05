---
title: flet run
---

The `flet run` command is used to start a Flet application in hot reload mode. It supports serving locally, watching for file changes, launching on web or mobile devices, and more.

## Usage

```
flet run [OPTIONS] [SCRIPT]
```

## Arguments

### `SCRIPT`

Path to the Python script that starts your Flet app.

## Options

### `--port PORT`

Custom TCP or HTTP (if `--web` option used) port to run the Flet app on.

**Default:** Assigned automatically

### `--host HOST`

Host to run the Flet web app on. Use `"*"` to listen on all interfaces.

### `--name APP_NAME`

Specify a unique name for your app. Useful when running multiple apps on the same port.

### `--module`, `-m`

Treat the `script` as a Python **module path** instead of a file path.

**Example:**

```bash
flet run -m my_app.main
```

### `--directory`, `-d`

Watch the directory of the script for changes and hot reload the app accordingly.

### `--recursive`, `-r`

Recursively watch all subdirectories of the script's directory for file changes.

### `--hidden`, `-n`

Start the application with the window hidden.

### `--web`, `-w`

Start Flet app as a dynamic website and open the application in a web browser automatically after starting.

### `--ios`

Launch the app on an iOS device (requires [Flet app for iOS](../getting-started/testing-on-mobile.md)).

### `--android`

Launch the app on an Android device (requires [Flet app for Android](../getting-started/testing-on-mobile.md)).

### `--assets ASSETS_DIR`, `-a` 

Path to a directory containing static assets used by the app (e.g., images, fonts).

### `--ignore-dirs IGNORE_DIRS`

Comma-separated list of directory names to ignore when watching for file changes.

### `--help`, `-h`

Show help information and exit.

### `--verbose`, `-v`

Enable verbose output. Use `-v` for standard verbose logging and `-vv` for more detailed output.