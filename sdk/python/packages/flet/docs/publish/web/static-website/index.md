Instructions for publishing Flet app into a standalone static website (SPA) that runs entirely in the browser with
[Pyodide](https://pyodide.org/en/stable/index.html) and does not require any code running on the server side.

Pyodide is a port of CPython to WebAssembly (WASM) which is an emerging technology with [some limitations](https://pyodide.org/en/stable/usage/wasm-constraints.html).

/// admonition | Native Python packages
    type: caution
Native Python packages (vs "pure" Python packages written in Python only) are packages that partially written in
C, Rust or other languages producing native code. Example packages are `numpy`, `cryptography`, `lxml`, `pydantic`.

Pyodide comes with a long list of [built-in packages](https://pyodide.org/en/stable/usage/packages-in-pyodide.html). However, to use a Python package from PyPI it must be a
pure Python package or provide a wheel with binaries [built for Emscripten](https://pyodide.org/en/stable/development/new-packages.html).
///

### Async and threading

Flet app that published to a static website could use both sync and async event handlers and methods.
Pyodide is a WebAssembly application which does not support threading. The entire Flet is running in a single thread
and all sync and async control event handlers are running in the same thread. If your app has CPU-bound logic
(e.g. calculating Fibonacci 😀) or "sleeps" to make UI prettier it may "hang" UI. Consider moving that logic to
a server and calling it via web API. Using `asyncio.sleep` in async methods is OK though.

## `flet build web`

Publish Flet app as a static website.

This is the recommended publishing method for static website.

### Prerequisites

Flutter SDK [must be installed](../../../publish/index.md#flutter-sdk) on your
computer for `flet build web` command to work.

### Testing website

You can test a published Flet app using [`flet serve`](../../../cli/flet-serve.md) command:

```bash
flet serve
```

Open `http://localhost:8000` in your browser to check the published app.

### Packaging assets

Once the website is published all files from `assets` directory will be
copied "as is" to the root of the website.

This allows overriding such things as `favicon.png` or ` manifest.json`
with your own content.

### URL strategy

Flet apps support two ways of configuring URL-based routing:

- **path** (default) - paths are read and written without a hash. For example, `fletapp.dev/path/to/view`.
- **hash** - paths are read and written to the [hash fragment](https://en.wikipedia.org/wiki/Uniform_Resource_Locator#Syntax). For example, `fletapp.dev/#/path/to/view`.

If a hosting provider supports [Single-page application (SPA) rendering](https://developers.cloudflare.com/pages/platform/serving-pages/#single-page-application-spa-rendering) you can
leave default "path" URL strategy as it gives pretty URLs.

However, if a hosting provider (like GitHub Pages) doesn't support SPA mode, then you
need to publish your app with the "hash" URL strategy.

Use `--route-url-strategy` argument to change URL strategy.

### Web renderer

You can change default "canvaskit" web renderer ([more about renderers here](../../../cookbook/fonts.md)
to "html" with `--web-renderer` option:

```bash
flet build web --web-renderer html
```

### Color emojis

To reduce app size default "CanvasKit" renderer does not use colorful emojis,
because the font file with color emojies weights around 8 MB.

You can, however, opt-in for color emojis with `--use-color-emoji` flag:

```bash
flet build web --use-color-emoji
```

Alternatively, switch to `html` renderer which uses browser fonts.

### Hosting website in a sub-directory

Multiple Flet apps can be hosted on a single domain
- each app in it's own sub-directory.

To make a published Flet app work in a sub-directory
you have to publish it with `--base-url` option:

```bash
flet build web --base-url <sub-directory>
```

For example, if app's URL is `https://mywebsite.com/myapp` then
it must be published with `--base-url myapp`.

## Disable splash screen

The [splash screen](../../index.md#splash-screen) is enabled/shown by default.

It can be disabled as follows:

/// tab | `flet build`
```bash
flet build apk --no-android-splash
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.splash]
android = false
```
///

## `flet publish`

An alternative method to publish Flet app as a static website.

Compared to [`flet build web`](#flet-build-web) command it does not require Flutter SDK to be installed on your computer.

However, static websites built with `flet build web` command, compared to `flet publish`, have faster load time
as all Python dependencies are now packaged into a single archive instead of being pulled in runtime with `micropip`.
`flet build web` also detects native Python [packages built into Pyodide](https://pyodide.org/en/stable/usage/packages-in-pyodide.html), such as `bcrypt`, `html5lib`, `numpy`
and many others, and installs them from Pyodide package registry.

### Publish app as a static website

Run the following command to publish Flet app to a standalone website:

```bash
flet publish <your-flet-app.py>
```

A static website is published into `./dist` directory.

Command optional arguments:

* `--pre` - allow micropip to install pre-release Python packages.
* `-a ASSETS_DIR`, `--assets ASSETS_DIR` - path to an assets directory.
* `--app-name APP_NAME` - application namee.
* `--app-description APP_DESCRIPTION` - application description.
* `--base-url BASE_URL` - base URL for the app.
* `--web-renderer {canvaskit,html}` - web renderer to use.
* `--route-url-strategy {path,hash}` - URL routing strategy.

### Testing website

You can test a published Flet app using [`flet serve`](../../../cli/flet-serve.md) command:

```bash
flet serve dist
```

Open `http://localhost:8000` in your browser to check the published app.

### Loading packages

You can load custom packages from PyPI during app start by listing them
in `requirements.txt`. `requirements.txt` must be created in the same
directory with `<your-flet-app.py>`.

Each line of `requirements.txt` contains a package name
followed by an optional version specifier.

/// admonition | Micropip
    type: tip

To install custom packages Pyodide uses [micropip](https://pypi.org/project/micropip/)
- a lightweight version of `pip` that works in a browser.

You can use [Micropip API](https://micropip.pyodide.org/en/stable/project/api.html) directly in your Flet app:

```python
import sys

if sys.platform == "emscripten": # check if run in Pyodide environment
    import micropip
    await micropip.install("regex")
```
///

#### Pre-release Python packages

You can allow loading pre-release versions of PyPI packages,
by adding `--pre` option to `flet publish` command:

```bash
flet publish <your-flet-app.py> --pre
```

### Assets

If your app requires assets (images, fonts, etc.) you can copy them into website d
irectory by using `--assets <directory>` option with `flet publish` command:

```bash
flet publish <your-flet-app.py> --assets assets
```

/// admonition | Assets directory
If you have `assets` directory in your app's directory and don't specify
`--assets` option then the contents of `assets` will be packaged along with
a Python application rather than copied to `dist`.
///

### URL strategy

Flet apps support two ways of configuring URL-based routing:

* **Path** (default) - paths are read and written without a hash. For example, `fletapp.dev/path/to/view`.
* **Hash** - paths are read and written to the [hash fragment](https://en.wikipedia.org/wiki/Uniform_Resource_Locator#Syntax). For example, `fletapp.dev/#/path/to/view`.

If a hosting provider supports [Single-page application (SPA) rendering](https://developers.cloudflare.com/pages/platform/serving-pages/#single-page-application-spa-rendering)
you can leave default "path" URL strategy as it gives pretty URLs.

However, if a hosting provider (like GitHub Pages) doesn't support SPA mode
then you need to publish your app with "hash" URL strategy.

To specify "hash" URL strategy during static app publishing use `--route-url-strategy` option:

```bash
flet publish <your-flet-app.py> --route-url-strategy hash
```

### Web renderer

You can change default "canvaskit" web renderer
([more about renderers here][flet.WebRenderer]) to "html" with `--web-renderer` option:

```bash
flet publish <your-flet-app.py> --web-renderer html
```

### Color emojis

To reduce app size default "CanvasKit" renderer does not use colorful emojis,
because the font file with color emojies weights around 8 MB.

You can, however, opt-in for color emojis with `--use-color-emoji` flag:

```bash
flet publish <your-flet-app.py> --use-color-emoji
```

Alternatively, switch to `html` renderer which uses browser fonts.

### Hosting website in a sub-directory

Multiple Flet apps can be hosted on a single domain - each app in it's own sub-directory.

To make a published Flet app work in a sub-directory you have to publish it with `--base-url` option:

```bash
flet publish <your-flet-app.py> --base-url <sub-directory>
```

For example, if app's URL is `https://mywebsite.com/myapp` then it
must be published with `--base-url myapp`.
