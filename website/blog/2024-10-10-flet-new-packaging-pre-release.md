---
slug: flet-new-packaging-pre-release
title: Flet new packaging pre-release
authors: feodor
---

Flet packaging for iOS and Android has been relying on Kivy and it was super annoying when your app depends on Python binary packages, such as Numpy or Pillow. You needed to compile those packages yourself using Kivy command line tools. It was really frustrating and even hopeless if Kivy didn't have "recipes" for some packages, like Pydantic.

Kivy no more! We've just published Flet 0.25.0.dev3519 pre-release with the improved `flet build` command which does not use Kivy! Flet is now using its own Python runtime "meticulously crafted in-house".

Flet packaging implementation for iOS and Androind adheres to strict specifications defined in [PEP 730](https://peps.python.org/pep-0730/) (iOS) and [PEP 738](https://peps.python.org/pep-0738/) (Android) which were implemented and released in Python 3.13 (and back-ported to Python 3.12). When pypi.org supports wheel tags for iOS and Android and 3rd-party Python package maintainers start uploading their mobile packages Flet will be compatible with them and you'll be able to use them in your Flet app.

<!-- truncate -->

## Installing pre-release

```
pip install flet==0.25.0.dev3519
```

:::note
For testing purposes we suggest installing Flet pre-release in a dedicated Python virtual environment.
:::

## Building the app with pre-release

To build your app with `flet build` command and pre-release version of Flet make sure your `requirements.txt` either contains exact version specifier:

```
flet==0.25.0.dev3519
```

or `--pre` flag before `flet` dependency:

```
--pre
flet
```

## Python 3.12

Packaged Flet app runs on Python 3.12.6 runtime for all platforms.

## Pre-built binary packages

`flet build` command for iOS and Android is now installing pre-built binary packages from https://pypi.flet.dev.

New packages can be built with creating a recipe in [Mobile Forge](https://github.com/flet-dev/mobile-forge) project. For now, Flet team is authoring those recipes for you, but when the process is polished and fully-automated you'll be able to send a PR and test the compiled package right away.

If you don't yet see a package at https://pypi.flet.dev you can request it in [Flet discussions - Packages](https://github.com/flet-dev/flet/discussions/categories/packages). Please do not request pure Python packages. Go to package's "Download files" section at https://pypi.org and make sure it contains binary platform-specific wheels.

Packaging behavior was changed too:

- The packaging is not trying to replace `flet` dependency with `flet-runtime`, `flet-embed` or `flet-pyodide`, but install all dependencies "as is" from `requirements.txt` or `pyproject.toml` - thanks to the new Flet packages structure (link).
- If the binary package for target platform is not found the packaging won't be trying to compile it from source distribution, but will fail instead with a meaningful error.

## New packages structure

The structure avoids rewriting pip dependencies while installing `flet` package on various platforms. There was a problem of detecting the correct `flet` package to install (`flet-runtime`, `flet-embed` or`flet-pyodide`?) if `flet` was not a direct dependency in user's app.

New Flet packages:

* `flet` - required for minimal Flet setup, app entry point for various platforms. Installed on all platforms.
* `flet-core` - required for minimal Flet setup, core logic and controls. Installed on all platforms.
* `flet-cli` - contains Flet CLI commands. Installed on desktop only.
* `flet-desktop` - contains pre-built Flet "client" app binary for macOS, Windows and Linux. By default installed on macOS and Windows desktops only. 
* `flet-desktop-light` - contains a light-weight version (without Audio and Video controls) of Flet "client" for Linux. By default installed on Linux desktops only. 
* `flet-web` - contains Flet web "client" and FastAPI integration. Installed on desktop only.

Other words, packaged Flet app contains only `flet` and `flet-core` packages.

### "Light" client for Linux

A light-weight desktop client, without Audio and Video controls, is not installed on Linux by default. It improves initial user experience as user doesn't need to immediately deal with gstreamer (audio) and mpv (video) dependencies right away and Flet "just works".  

Once user got some Flet experience and wants to use Video and Audio controls in their application they can install gstreamer and/or mpv and replace Flet desktop with a full version.

Uninstall "light" Flet client:

```
pip uninstall flet-desktop-light --yes
```

Install full Flet desktop client:

```
pip install flet-desktop==0.25.0.dev3519
```

## Permissions

New `flet build` command allows granular control over permissions, features and entitlements embedded into `AndroidManifest.xml`, `Info.plist` and `.entitlements` files.

No more hard-coded permissions in those files!

### iOS

Setting iOS permissions:

```
flet build --info-plist permission_1=True|False|description permission_2=True|False|description ...
```

For example:

```
flet build --info-plist NSLocationWhenInUseUsageDescription=This app uses location service when in use.
```

### macOS

Setting macOS entitlements:

```
flet build --macos-entitlements name_1=True|False name_2=True|False ...
```

Default macOS entitlements:

* `com.apple.security.app-sandbox = False`
* `com.apple.security.cs.allow-jit = True`
* `com.apple.security.network.client = True`
* `com.apple.security.network.server" = True`

### Android

Setting Android permissions and features:

```
flet build --android-permissions permission=True|False ... --android-features feature_name=True|False
```

For example:

```
flet build \
    --android-permissions android.permission.READ_EXTERNAL_STORAGE=True \
      android.permission.WRITE_EXTERNAL_STORAGE=True \
    --android-features android.hardware.location.network=False
```

Default Android permissions:

* `android.permission.INTERNET`

Default permissions can be disabled with `--android-permissions` option and `False` value, for example:

```
flet build --android-permissions android.permission.INTERNET=False
```

Default Android features:

* `android.software.leanback=False` (`False` means it's written in manifest as `android:required="false"`)
* `android.hardware.touchscreen=False`

### Cross-platform permission groups

There are pre-defined permissions that mapped to `Info.plist`, `*.entitlements` and `AndroidManifest.xml` for respective platforms.

Setting cross-platform permissions:

```
flet build --permissions permission_1 permission_2 ...
```

Supported permissions:

* `location`
* `camera`
* `microphone`
* `photo_library`

#### iOS mapping to `Info.plist` entries

* `location`
  * `NSLocationWhenInUseUsageDescription = This app uses location service when in use.`
  * `NSLocationAlwaysAndWhenInUseUsageDescription = This app uses location service.`
* `camera`
  * `NSCameraUsageDescription = This app uses the camera to capture photos and videos.`
* `microphone`
  * `NSMicrophoneUsageDescription = This app uses microphone to record sounds.`
* `photo_library`
  * `NSPhotoLibraryUsageDescription = This app saves photos and videos to the photo library.`

#### macOS mapping to entitlements

* `location`
  * `com.apple.security.personal-information.location = True`
* `camera`
  * `com.apple.security.device.camera = True`
* `microphone`
  * `com.apple.security.device.audio-input = True`
* `photo_library`
  * `com.apple.security.personal-information.photos-library = True`

#### Android mappings

* `location`
  * permissions:
    * `android.permission.ACCESS_FINE_LOCATION": True`
    * `android.permission.ACCESS_COARSE_LOCATION": True`
    * `android.permission.ACCESS_BACKGROUND_LOCATION": True`
  * features:
    * `android.hardware.location.network": False`
    * `android.hardware.location.gps": False`
* `camera`
  * permissions:
    * `android.permission.CAMERA": True`
  * features:
    * `android.hardware.camera": False`
    * `android.hardware.camera.any": False`
    * `android.hardware.camera.front": False`
    * `android.hardware.camera.external": False`
    * `android.hardware.camera.autofocus": False`
* `microphone`
  * permissions:
    * `android.permission.RECORD_AUDIO": True`
    * `android.permission.WRITE_EXTERNAL_STORAGE": True`
    * `android.permission.READ_EXTERNAL_STORAGE": True`
* `photo_library`
  * permissions:
    * `android.permission.READ_MEDIA_VISUAL_USER_SELECTED": True`

## Control over app compilation and cleanup

`flet build` command is no longer compiling app `.py` files into `.pyc` by default which allows you to avoid (defer?) discovery of any syntax errors in your app and complete the packaging.

You can control the compilation and cleanup with the following new options:

* `--compile-app` - compile app's `.py` files.
* `--compile-packages` - compile installed packages' `.py` files.
* `--cleanup-on-compile` - remove unnecessary files upon successful compilation.

## Signing Android bundles

Added new options for signing Android builds:

* `--android-signing-key-store` - path to an upload keystore `.jks` file for Android apps.
* `--android-signing-key-store-password` - Android signing store password.
* `--android-signing-key-alias` - Android signing key alias. Default is "upload".
* `--android-signing-key-password` - Android signing key password.

Read [Build and release an Android app](https://docs.flutter.dev/deployment/android#signing-the-app) for more information on how to configure upload key for Android builds.

## "Data" and "Temp" directories for the app

Flet developers have been asking where to store application data, such as uploaded files, SQLite databases, etc. that are persistent across application updates.

This release introduce two environment variables that are available in your Flet apps:

* `FLET_APP_STORAGE_DATA` - directory for storing application data that is preserved between app updates. That directory is already pre-created.
* `FLET_APP_STORAGE_TEMP` - directory for temporary application files, i.e. cache. That directory is already pre-created.

For example, data folder path can be read in your app as:

```
import os

# it's `None` when running the app in web mode
data_dir = os.getenv("FLET_APP_STORAGE_DATA")
```

:::note
`flet run` command creates data and temp directories and sets `FLET_APP_STORAGE_DATA` and `FLET_APP_STORAGE_TEMP` to their paths.
:::

## Deep linking configuration

There is a new `--deep-linking-url` option to configure deep linking for iOS and Android builds. The value must be in the format `<sheme>://<host>`.

## Faster re-builds

Ephemeral Flutter app created by `flet build` command is not re-created all the time in a temp directory, but cached in `build/flutter` directory which gives faster re-builds, improves packaging troubleshooting and does not pollute temp directory.

## Split APKs per ABI

`flet build` now provides the built-in `--split-per-abi` option to split the APKs per ABIs.

## Known pre-release issues

* `flet publish` is not yet working.

## What else coming in the release

We would like to include a few more things into Flet 0.25.0 release. Expect more pre-releases in the coming weeks.

### `pyproject.toml` support

It's inconvenient and bulky to carry all `flet build` settings as command line options.

You will be able to store project and build settings in `[tool.flet]` section of `pyproject.toml`.

### Running Flet app on simulator

We will add an option to `flet build` and run packaged app on a real device or simulator.

### Installing Flutter

`flet build` will download and configure Flutter for you if there is no suitable installation available on your machine.


