---
title: "Publish web app as static website"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';

Instructions for publishing a Flet app as a standalone static website (SPA) that
runs entirely in the browser with [Pyodide](https://pyodide.org/en/stable/index.html).
No Python code runs on the server.

Pyodide is a port of CPython to WebAssembly (WASM) and has
some [limitations](https://pyodide.org/en/stable/usage/wasm-constraints.html).

:::note[Native Python packages]
Native Python packages (vs "pure" Python packages written in Python only) are packages
partially written in C, Rust, or other languages producing native code.
Example packages are `numpy`, `cryptography`, `lxml`, `pydantic-core`.

Pyodide comes with a list of [built-in packages](https://pyodide.org/en/stable/usage/packages-in-pyodide.html).
To use a package from PyPI, it must be pure Python or provide a wheel built for
[Emscripten](https://pyodide.org/en/stable/development/new-packages.html).
:::

:::note[Async and threading]
Static websites run in a single browser thread. You can use sync and async handlers,
but long-running CPU work or blocking calls will freeze the UI. Prefer async I/O,
or move heavy work to a server and call it via a web API.
:::

:::tip[Micropip]
Pyodide installs packages with [micropip](https://pypi.org/project/micropip/).
You can use the [Micropip API](https://micropip.pyodide.org/en/stable/project/api.html)
directly in your Flet app:

```python
import sys

if sys.platform == "emscripten":
    import micropip
    await micropip.install("regex")
```
:::

## Differences

There are two ways to publish a static website: [`flet build web`](#flet-build-web) and [`flet publish`](#flet-publish).
Both produce a static site that runs in the browser via Pyodide. They
differ mainly in how and when Python dependencies are installed:

|                               | [`flet publish`](#flet-publish)                       | [`flet build web`](#flet-build-web)                                                  |
|-------------------------------|-------------------------------------------------------|--------------------------------------------------------------------------------------|
| Flutter required              | No                                                    | Yes                                                                                  |
| Dependency install            | At runtime, in the browser (`micropip`)               | At build time, on your machine (`pip`)                                               |
| Build time                    | Faster — no Flutter compilation, no local pip install | Slower — Flutter build + local dependency install                                    |
| Initial load time             | Slower — wheels are fetched from PyPI on page load    | Faster — dependencies are already bundled                                            |
| Pure-Python wheels            | ✅                                                     | ✅                                                                                    |
| Pyodide-built binary wheels   | ✅ (from Pyodide CDN)                                  | ✅ (auto-detected from Pyodide registry)                                              |
| Source distributions (sdists) | ❌ `micropip` can't build sdists in the browser        | ✅ pure-Python sdists, opt in via [`source_packages`](../../index.md#source-packages) |

### Sdist-only dependencies

A common failure mode with `flet publish` is a (transitive) dependency that ships only a
source distribution (`.tar.gz`, no wheel) — for example,
[`docopt`](https://pypi.org/project/docopt/#files). `micropip` cannot build
sdists, so load fails with:

```
ValueError: Can't find a pure Python 3 wheel for '<package>'
```

In such cases, we suggest switching to [`flet build web`](#flet-build-web) and
adding the package to [`source_packages`](../../index.md#source-packages).
**Note** that `source_packages` only works for **pure-Python** sdists. Sdists with C/Rust
extensions (e.g. `numpy`, `cryptography`) cannot be built for Pyodide — use Pyodide's
[built-in packages](https://pyodide.org/en/stable/usage/packages-in-pyodide.html) instead.

## `flet publish`

Does not require Flutter. It packages your app and installs dependencies in the
browser at runtime via [micropip](https://pypi.org/project/micropip/).

To publish an app, run:

```bash
flet publish <path-to-app.py>
```

The website is published to [`--distpath`](../../../cli/flet-publish.md#--distpath) (default: `./dist`).

### Testing the site

You can try published Flet app using [`flet serve`](../../../cli/flet-serve.md) command:

```bash
flet serve dist
```

Then, open `http://localhost:8000` in your browser to check the published app.

### Assets

If the [assets](../../../cookbook/assets.md) directory exists (default: `./assets`), its contents are copied
to the published site root. Use [`--assets`](../../../cli/flet-publish.md#--assets) to point to a different
folder. Assets are not packaged inside the `app.tar.gz`.

## `flet build web`

Uses [Flutter](https://flutter.dev/) and [Pyodide](https://pyodide.org/en/stable/index.html).
Dependencies are resolved and installed locally at build time (via `pip`), then bundled into the output archive.

:::tip[Note]
Complementary and more general information is available [here](../../index.md).
:::

### Testing the site

[`flet serve`](../../../cli/flet-serve.md) serves the default
[output directory](../../index.md#output-directory) (`./build/web`):

```bash
flet serve
```

## Configuration options

These settings apply to `flet build web` and `flet publish`, unless noted.

### Base URL

Use a base URL when hosting your app in a subdirectory. Flet normalizes it to
`/<value>/` and uses `/` when unset.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--base-url`](../../../cli/flet-build.md#--base-url)
2. `[tool.flet.web].base_url`
3. `"/"`

#### Example

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build web --base-url /myapp/
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.web]
base_url = "/myapp/"
```
</TabItem>
</Tabs>
### Route URL strategy

Controls how routes are represented in the URL:

- `path` - clean paths; requires SPA-capable hosting.
- `hash` - uses the URL hash; works on static hosts without SPA support.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--route-url-strategy`](../../../cli/flet-build.md#--route-url-strategy)
2. `[tool.flet.web].route_url_strategy`
3. `"path"`

#### Example

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build web --route-url-strategy hash
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.web]
route_url_strategy = "hash"
```
</TabItem>
</Tabs>
### Web renderer

Selects the Flutter web renderer:

- `auto` (default) - let Flutter choose the best renderer
- `canvaskit`
- `skwasm`

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--web-renderer`](../../../cli/flet-build.md#--web-renderer)
2. `[tool.flet.web].renderer`
3. `"auto"`

#### Example

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build web --web-renderer canvaskit
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.web]
renderer = "canvaskit"
```
</TabItem>
</Tabs>
### CDN assets

By default, Pyodide, CanvasKit, and fonts are loaded from CDNs to keep the output
small. Disable CDN loading for offline or air-gapped deployments.

#### Resolution order

CDN loading is disabled in the following order of precedence:

1. [`--no-cdn`](../../../cli/flet-build.md#--no-cdn)
2. `[tool.flet.web].cdn = false`
3. default: CDN enabled

#### Example

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build web --no-cdn
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.web]
cdn = false
```
</TabItem>
</Tabs>
### PWA colors

Configure PWA colors used in `manifest.json` and browser UI.

#### Resolution order

For each setting:

1. [`--pwa-background-color`](../../../cli/flet-build.md#--pwa-background-color) / [`--pwa-theme-color`](../../../cli/flet-build.md#--pwa-theme-color)
2. `[tool.flet.web].pwa_background_color` / `[tool.flet.web].pwa_theme_color`
3. `#FFFFFF` / `#0175C2`

#### Example

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build web --pwa-background-color "#000000" --pwa-theme-color "#FF0000"
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.web]
pwa_background_color = "#000000"
pwa_theme_color = "#FF0000"
```
</TabItem>
</Tabs>
### WASM output

By default, [`flet build web`](#flet-build-web) enables Flutter's WASM output.

:::note[Note]
[`flet build web`](#flet-build-web) only.
:::

#### Resolution order

The WASM output is disabled in the following order of precedence:

1. [`--no-wasm`](../../../cli/flet-build.md#--no-wasm)
2. `[tool.flet.web].wasm = false`
3. default: WASM enabled

#### Example

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build web --no-wasm
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.web]
wasm = false
```
</TabItem>
</Tabs>
