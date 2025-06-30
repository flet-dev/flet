Flet apps can be executed as either desktop or web applications using the [`flet run`](TBA) command.
Doing so will start the app in a native OS window or a web browser, respectively, with hot reload enabled to view changes in real-time.

## Desktop app

To run Flet app as a desktop app, use the following command:

/// tab | uv
```bash
uv run flet run
```
///
/// tab | pip
```bash
flet run
```
///
/// tab | poetry
```bash
poetry run flet run
```
///

When you run the command without any arguments, `main.py` script in the current directory will be executed, by default.

If you need to provide a different path, use the following command:

/// tab | uv
```bash
uv run flet run [script]
```
///
/// tab | pip
```bash
flet run [script]
```
///
/// tab | poetry
```bash
poetry run flet run [script]
```
///

Where `[script]` is a relative (ex: `counter.py`) or absolute (ex: `/Users/john/projects/flet-app/main.py`) path to the Python script you want to run.

The app will be started in a native OS window:

![macOS](../assets/getting-started/flet-counter-macos.png)
/// caption
macOS
///


![Windows](../assets/getting-started/flet-counter-windows.png)
/// caption
Windows
///

## Web app

To run Flet app as a web app, use the `--web` (or `-w`) option:
/// tab | uv
```bash
uv run flet run --web [script]  # (1)!
```

1. A fixed port can be specified using `--port` ( or `-p`) option, followed by the port number.
///
/// tab | pip
```bash
flet run --web [script]  # (1)!
```

1. A fixed port can be specified using `--port` ( or `-p`) option, followed by the port number.
///
/// tab | poetry
```bash
poetry run flet run --web [script]  # (1)!
```

1. A fixed port can be specified using `--port` ( or `-p`) option, followed by the port number.
///

A new browser window/tab will be opened and the app will be using a random TCP port:

![Web](../assets/getting-started/flet-counter-safari.png)

/// caption
Web app
///

## Watching for changes

By default, Flet will watch the script file that was run and reload the app whenever the contents 
of this file are modified+saved, but will **not** watch for changes in other files.

To modify this behavior, you can use one or more of the following options:

* `-d` or `--directory` to watch for changes in the `[script]`s directory only
* `-r` or `--recursive` to watch for changes in the `[script]`s directory and all sub-directories recursively

/// admonition | Example
    type: example

/// tab | uv
```bash
uv run flet run --recursive [script]
```
///
/// tab | pip
```bash
flet run --recursive [script]
```
///
/// tab | poetry
```bash
poetry run flet run --recursive [script]
```
///

///
