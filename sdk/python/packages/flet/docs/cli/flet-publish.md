---
title: flet publish
---

The `flet publish` command is used to compile and package a Flet app as a standalone static web application. It supports progressive web app (PWA) features, custom metadata, and options for web rendering and deployment.

## Usage

```
flet publish [OPTIONS] [SCRIPT]
```

## Arguments

### `SCRIPT`

Path to the Python script that starts your Flet app.

## Options

### `--pre`

Allow `micropip` to install pre-release Python packages. Use this if your app depends on a prerelease version of a package.

### `--assets ASSETS_DIR`, `-a`

Path to a directory containing static assets used by the app (e.g., images, fonts, icons).

### `--distpath DISTPATH`

Directory where the published web app should be placed.

**Default:** `./dist`

### `--app-name APP_NAME`

Full name of the application. This is used in PWA metadata and may appear in the install prompt.

### `--app-short-name APP_SHORT_NAME`

A shorter version of the application name, often used in homescreen icons or install prompts.

### `--app-description APP_DESCRIPTION`

Short description of the application. Used in PWA manifests and metadata.

### `--base-url BASE_URL`

Base URL path to serve the app from. Useful if the app is hosted in a subdirectory.

**Example:**
`--base-url /myapp`

### `--web-renderer {auto,canvaskit,skwasm}`

Specifies which Flutter web renderer to use:

- `auto`: Let Flutter decide
- `canvaskit`: Use CanvasKit for high-performance rendering
- `skwasm`: Use Skia Wasm (experimental)

### `--route-url-strategy {path,hash}`

Controls how routes are handled in the browser:

- `path`: Clean URLs like `/page`
- `hash`: Hash-based URLs like `#/page` (recommended for static hosting)

### `--pwa-background-color PWA_BACKGROUND_COLOR`

Initial background color of your web app during the loading phase (used in splash screens).

### `--pwa-theme-color PWA_THEME_COLOR`

Default color of the browser UI (e.g., address bar) when your app is installed as a PWA.

### `--no-cdn`

Disable loading of CanvasKit, Pyodide, and fonts from CDNs. Use this for full offline deployments or air-gapped environments.

### `--help`, `-h`

Show help information and exit.

### `--verbose`, `-v`

Enable verbose output. Use `-v` for standard verbose logging and `-vv` for more detailed output.