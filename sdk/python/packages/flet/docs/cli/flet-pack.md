---
title: flet pack
---

The `flet pack` command packages a Flet application into a standalone desktop executable or app bundle using [PyInstaller](https://pyinstaller.org/). It supports platform-specific options such as icons, metadata, code signing, and more.

[//]: # (You can find the guide [here]&#40;../cookbook/packaging-desktop-app&#41;.)

## Usage

```
flet pack [OPTIONS] SCRIPT
```

## Arguments

### `SCRIPT`

Path to the Python script that launches your Flet app.

## Options

### `--icon ICON`, `-i`

Path to an icon file for your executable or app bundle. Supported formats:
- `.ico` (Windows)
- `.png` (Linux)
- `.icns` (macOS)

### `--name NAME`, `-n`

Name for the generated executable (Windows) or app bundle (macOS).

### `--onedir`, `-D`

Create a one-folder bundle instead of a single-file executable (Windows only).

### `--distpath DISTPATH`

Directory where the packaged app will be placed.  
**Default:** `./dist`

### `--add-data ADD_DATA`

Add additional non-binary files or folders to the bundle.  
Accepts one or more arguments in the form `source:destination`.

**Example:**
```bash
--add-data "assets:assets"
```

### `--add-binary ADD_BINARY`

Add binary files to the executable.  
Format: `source:destination[:platform]`

### `--hidden-import HIDDEN_IMPORT`

Add Python modules that are dynamically imported and not detected by static analysis.

**Example:**
```bash
--hidden-import my_plugin_module
```

### `--product-name PRODUCT_NAME`

Product name to be embedded in the executable (Windows) or bundle (macOS).

### `--file-description FILE_DESCRIPTION`

File description to embed in the executable (Windows).

### `--product-version PRODUCT_VERSION`

Product version for the executable (Windows) or bundle (macOS).

### `--file-version FILE_VERSION`

File version for the executable in `n.n.n.n` format (Windows only).

### `--company-name COMPANY_NAME`

Company name metadata for the Windows executable.

### `--copyright COPYRIGHT`

Copyright string embedded in the executable (Windows) or bundle (macOS).

### `--codesign-identity CODESIGN_IDENTITY`

Code signing identity to sign the app bundle (macOS only).

### `--bundle-id BUNDLE_ID`

Bundle identifier used for macOS app packaging.

### `--debug-console DEBUG_CONSOLE`

Enable or disable the Python debug console window.  
Useful for troubleshooting runtime errors.

### `--uac-admin`

Request elevated (admin) permissions on application start (Windows only).  
Adds a UAC manifest to the executable.

### `--pyinstaller-build-args PYINSTALLER_BUILD_ARGS`

Pass additional raw arguments to the underlying `pyinstaller` build command.

### `--yes`, `-y`

Enable non-interactive mode. All prompts will be skipped.

### `--help`, `-h`

Show help information and exit.

### `--verbose`, `-v`

Enable verbose output. Use `-v` for standard verbose logging and `-vv` for more detailed output.