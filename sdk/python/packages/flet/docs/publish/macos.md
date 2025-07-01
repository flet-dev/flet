---
title: Packaging app for macOS
---

Flet CLI provides `flet build macos` command that allows packaging Flet app into a macOS application bundle.

::note
The command can be run on macOS only.
::

## Prerequisites

## Prerequisites

### Rosetta 2

Flutter requires [Rosetta 2](https://support.apple.com/en-us/HT211861) on Apple silicon:

```
sudo softwareupdate --install-rosetta --agree-to-license
```

### Xcode

[Xcode](https://developer.apple.com/xcode/) 15 or later to compile native Swift or ObjectiveC code.

### CocoaPods

[CocoaPods](https://cocoapods.org/) 1.16 to compile and enable Flutter plugins.

## `flet build macos`

Creates a macOS application bundle from your Flet app.

## Bundle architecture

By default, `flet build macos` command builds universal app bundle that works on both Apple Silicon and older Intel processors. Therefore, packaging utility will try to download Python binary wheels for both `arm64` and `x86_64` platforms. Recent releases
of some popular packages do not include `x86_64` wheels anymore, so the entire packaging operation will fail.

You can limit the build command to a specific architecture only, by using `--arch` option. For example, to build macOS app bundle that works on Apple Silicon only use the following command:

```
flet build macos --arch arm64
```

The same can be configured in `pyproject.toml`:

```toml
[tool.flet.macos]
build_arch = "arm64"
```

## Permissions

Setting macOS entitlements which are written and `.entitlements` files:

```
flet build --macos-entitlements name_1=True|False name_2=True|False ...
```

Default macOS entitlements:

* `com.apple.security.app-sandbox = False`
* `com.apple.security.cs.allow-jit = True`
* `com.apple.security.network.client = True`
* `com.apple.security.network.server" = True`

Configuring macOS app entitlements in `pyproject.toml` (notice `"` around entitlement name):

```toml
[tool.flet.macos]
entitlement."com.apple.security.personal-information.photos-library" = true
```