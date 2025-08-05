---
title: flet build
---

The `flet build` command packages a Flet Python app into a platform-specific executable or installable bundle. It supports building for desktop (macOS, Linux, Windows), web, Android (APK/AAB), and iOS (IPA), with a wide range of customization options for metadata, assets, splash screens, and signing.

Full guide is [here](../publish/index.md).

## Usage

```
flet build {TARGET} [OPTIONS] [PYTHON_APP_PATH]
```

## Arguments

### `TARGET`

Target platform or type of a package to build for:

* `macos`
* `linux`
* `windows`
* `web`
* `apk`
* `aab`
* `ipa`

### `PYTHON_APP_PATH`

Path to a Python application directory.

## Common Options

### `--help`, `-h`

Show help information and exit.

### `--verbose`, `-v`

Enable verbose output. Use `-v` for standard logging and `-vv` for detailed logging.

### `--arch TARGET_ARCH`

Build for specific CPU architectures (used in macOS and Android builds).  
**Example:** `--arch arm64 x64`

### `--exclude EXCLUDE`

Exclude files or directories from the package.

### `--output OUTPUT_DIR`, `-o`

Output directory for the final bundle.  
**Default:** `<python_app_path>/build/<target_platform>`

### `--clear-cache`

Clear build cache before starting.

## Project Metadata

### `--project PROJECT_NAME`

Project name used in metadata and bundle IDs.

### `--description DESCRIPTION`

Short description of the application.

### `--product PRODUCT_NAME`

Display name of the application (shown in UI dialogs).

### `--org ORG_NAME`

Reverse-domain organization name (e.g., `com.example`).  
Used in bundle IDs and signing.

### `--bundle-id BUNDLE_ID`

Explicit bundle ID to use (overrides `org.project` default).

### `--company COMPANY_NAME`

Company name shown in the application.

### `--copyright COPYRIGHT`

Copyright text for About dialogs.

## Icons & Splash

### `--android-adaptive-icon-background`

Background color for adaptive Android icons.

### `--splash-color`, `--splash-dark-color`

Background colors for the splash screen (light and dark modes).

### `--no-web-splash`, `--no-ios-splash`, `--no-android-splash`

Disable splash screens on respective platforms.

## iOS Code Signing

### `--ios-team-id`

Apple developer team ID for signing iOS apps.

### `--ios-export-method`

Export method (`debugging`, `ad-hoc`, etc.).  
**Default:** `debugging`

### `--ios-provisioning-profile`

Name or UUID of provisioning profile.

### `--ios-signing-certificate`

Signing certificate name, SHA-1 hash, or selector.

## Web Options

### `--base-url`

Base URL from which the app is served.

### `--web-renderer {auto,canvaskit,skwasm}`

Flutter web renderer to use.

### `--route-url-strategy {path,hash}`

URL strategy for routing.

### `--pwa-background-color`, `--pwa-theme-color`

PWA metadata: splash background and UI theme color.

### `--no-wasm`

Disable WASM support in web build.

### `--no-cdn`

Don’t load CanvasKit, Pyodide, or fonts from CDN.

## Android Signing

### `--android-signing-key-store`

Path to `.jks` keystore.

### `--android-signing-key-store-password`

Keystore password.

### `--android-signing-key-password`

Key password.

### `--android-signing-key-alias`

Key alias (default: `upload`).

## App Compilation and Cleanup

### `--compile-app`, `--compile-packages`

Pre-compile Python source files (`.pyc`) in app and dependencies.

### `--cleanup-app`, `--cleanup-packages`

Remove unused files from the app or packages.

### `--cleanup-app-files`, `--cleanup-package-files`

List of glob patterns to remove from app or package.

## Flutter and Template Options

### `--flutter-build-args`

Additional args passed to the `flutter build` command.

### `--source-packages`

List of packages to install from source distribution.

### `--template`, `--template-dir`, `--template-ref`

Custom Flutter bootstrap template (local or git).

### `--module-name`

Module name with the app entry point (used for packaging).

## Info.plist and Entitlements (macOS/iOS)

### `--info-plist`

Key-value pairs to add to `Info.plist`.

### `--macos-entitlements`

Key-value entitlements to add for macOS builds.

## Android Manifest Customization

### `--android-features`

List of `<feature>=True|False` entries.

### `--android-permissions`

List of `<permission>=True|False` entries.

### `--android-meta-data`

List of `<name>=value` metadata entries.

## Cross-Platform Permissions

### `--permissions {location,camera,microphone,photo_library}`

Set of permissions to request in iOS, Android, and macOS apps.

## Deep Linking

### `--deep-linking-scheme`, `--deep-linking-host`

Configure deep linking (e.g., `myapp://host/path`) for iOS and Android.

## Miscellaneous

### `--build-number`, `--build-version`

Set app internal build number and user-visible version string.

### `--show-platform-matrix`

Display the build platform compatibility matrix and exit.

### `--no-rich-output`

Use plain text instead of rich terminal output.

### `--skip-flutter-doctor`

Skip running `flutter doctor` during build validation.