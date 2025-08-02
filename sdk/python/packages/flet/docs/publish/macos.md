---
title: Packaging app for macOS
---

Instructions for packaging a Flet app into a macOS application bundle.

**See complementary information [here](index.md).**

## Prerequisites

### Rosetta 2

[Flutter](https://flutter.dev), which we use for packaging,
requires [Rosetta 2](https://support.apple.com/en-us/HT211861) on Apple Silicon:
```
sudo softwareupdate --install-rosetta --agree-to-license
```

### Xcode

[Xcode](https://developer.apple.com/xcode/) 15 or later to compile native Swift or ObjectiveC code.

### CocoaPods

[CocoaPods](https://cocoapods.org/) 1.16 or later to compile and enable Flutter plugins.

## <code class="doc-symbol doc-symbol-command"></code> `flet build macos`

/// admonition | Note
This command can be run on a **macOS only**.
///

Creates a macOS application bundle from your Flet app.

## Bundle architecture

By default, `flet build macos` command builds universal app bundle that works on both
Apple Silicon and older Intel processors. Therefore, packaging utility will try to download
Python binary wheels for both `arm64` and `x86_64` platforms. Recent releases
of some popular packages do not include `x86_64` wheels anymore, so the entire packaging operation will fail.

You can limit the build command to specific architectures only, by using `--arch` option.
For example, to build macOS app bundle that works on Apple Silicon only use the following command:

/// tab | `flet build`
```
flet build macos --arch arm64
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.macos]
target_arch = ["arm64"] # (1)!
```

1. This setting can be a list (for one or more targets) or a string (for one target).
///

**TBD: list some common/supported archs**

## Entitlements

Key-value pairs that grant an executable permission to use a service or technology. 
Supported entitlements are defined in [Apple Developer Entitlements Reference](https://developer.apple.com/documentation/bundleresources/entitlements).

They can be set as follows:

/// tab | `flet build`
```
flet build --macos-entitlements "key"=value
```
///
/// tab | `pyproject.toml`

/// tab | `[tool.flet.macos]`
```toml
[tool.flet.macos]
entitlement."key" = value
```
///
/// tab | `[tool.flet.macos.entitlement]`
```toml
[tool.flet.macos.entitlement]
"key" = value
```
///

///

They get written into specific `.entitlements` files.

/// details | Default values
    type: info
Below is a list of default entitlements:

```toml
[tool.flet.macos.entitlement]
"com.apple.security.app-sandbox" = false
"com.apple.security.cs.allow-jit" = true
"com.apple.security.network.client" = true
"com.apple.security.network.server" = true
```
