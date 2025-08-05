---
title: flet serve
---

The `flet serve` command launches a lightweight static web server, optionally adding WebAssembly-related headers for Flet web apps.

## Usage

```
flet serve [OPTIONS] [WEB_ROOT]
```

## Arguments

### `WEB_ROOT`

Path to the directory to serve. Use this to specify the root directory containing your static files (e.g., your built Flet web app).
 
**Default:** `./build/web`

## Options

### `--port`, `-p`

Port number to serve the files on. Use this to customize the port if the default (`8000`) is already in use or needs to be changed.

**Default:** `8000`

### `--help`, `-h`

Show help information and exit.

### `--verbose`, `-v`

Enable verbose output. Use `-v` for standard verbose logging and `-vv` for more detailed output.