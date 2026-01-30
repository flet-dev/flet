---
title: Packaging app for macOS
---

Instructions for packaging a Flet app into a macOS application bundle.

/// admonition | Info
    type: tip
This guide provides detailed macOS-specific information.
Complementary and more general information is available [here](index.md).
///

## Prerequisites

### Rosetta 2

[Flutter](https://flutter.dev), which we use for packaging,
requires [Rosetta 2](https://support.apple.com/en-us/HT211861) on Apple Silicon:

```bash
sudo softwareupdate --install-rosetta --agree-to-license
```

### Xcode

[Xcode](https://developer.apple.com/xcode/) 15 or later is required to compile
native Swift or Objective-C code.

### CocoaPods

[CocoaPods](https://cocoapods.org/) 1.16 or later is required to install and
compile Flutter plugins.

## `flet build macos`

/// admonition | Note
This command can be run on **macOS only**.
///

Builds a macOS application bundle from your Flet app.

## Target architecture

By default, `flet build macos` creates a universal bundle that runs on both
Apple Silicon and Intel Macs. Packaging downloads Python wheels for both
`arm64` and `x86_64` architectures.

To limit packaging to a specific architecture, see [this](index.md#target-architecture).
This affects which Python wheels are bundled and, in turn, which CPU architectures the app will run on.
You will then have to provide your users with the correct build for their Macs.

## Permissions

macOS permissions are declared through [`Info.plist`](#infoplist) privacy usage strings and
app [entitlements](#entitlements). You can also use the [cross-platform permission bundles](index.md#predefined-cross-platform-permission-bundles)
to inject common entries, then override or extend them with platform-specific values.

### Info.plist

Add or override `Info.plist` entries for macOS builds.
These values are written to `macos/Runner/Info.plist` of the [build project](index.md#build-template).

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--info-plist`](../cli/flet-build.md#-info-plist)
2. `[tool.flet.macos].info`
3. Values injected by [`permissions`](index.md#permissions)

CLI booleans must be `True` or `False` (case-sensitive). For lists or nested
structures, use TOML in `[tool.flet.macos].info`.

#### Example

/// tab | `flet build`
```
flet build macos --info-plist LSApplicationCategoryType="public.app-category.utilities"
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.macos.info]
LSApplicationCategoryType = "public.app-category.utilities"
```
///

### Entitlements

Entitlements are boolean key-value pairs that grant an executable permission
to use a service or technology. Supported entitlements are defined in the
[Apple Developer Entitlements Reference](https://developer.apple.com/documentation/bundleresources/entitlements).

Entitlements are written to `macos/Runner/DebugProfile.entitlements` and
`macos/Runner/Release.entitlements` in the [build template](index.md#build-template).

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--macos-entitlements`](../cli/flet-build.md#-macos-entitlements)
2. `[tool.flet.macos.entitlement]`
3. Values injected by [`permissions`](index.md#permissions)
4. Defaults:
   ```toml
    [tool.flet.macos.entitlement]
    "com.apple.security.app-sandbox" = false
    "com.apple.security.cs.allow-jit" = true
    "com.apple.security.network.client" = true
    "com.apple.security.network.server" = true
    "com.apple.security.files.user-selected.read-write" = true
    ```

CLI values are `True` or `False` (case-sensitive). In `pyproject.toml`, use
`true`/`false`.

#### Example

/// tab | `flet build`
```bash
flet build macos --macos-entitlements com.apple.security.network.client=True com.apple.security.app-sandbox=False
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.macos.entitlement]
"com.apple.security.network.client" = true
"com.apple.security.app-sandbox" = false
```
///
