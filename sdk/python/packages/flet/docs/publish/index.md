---
title: Publishing Flet app to multiple platforms
---

## Introduction

Flet CLI provides `flet build` command that allows packaging Flet app into a standalone executable or install package for distribution.

## Platform matrix

The following matrix shows which OS you should run `flet build` command on in order to build a package for specific platform:

| Run on / `flet build` | `apk/aab` | `ipa` | `macos` | `linux` | `windows` | `web` |
|:---------------------:|:---------:|:-----:|:-------:|:-------:|:---------:|:-----:|
|         macOS         |     ✅     |   ✅   |    ✅    |         |           |   ✅   |
|        Windows        |     ✅     |       |         | ✅ (WSL) |     ✅     |   ✅   |
|         Linux         |     ✅     |       |         |    ✅    |           |   ✅   |

## Prerequisites

### Flutter SDK

If the correct version of the Flutter SDK is not found in the `PATH`, it will be automatically installed during the first run when building a Flet app for any platform.

Flutter SDK is installed into `$HOME/flutter/{version}` directory.

## Project structure

`flet build` command assumes the following minimal Flet project structure:

```tree
README.md
pyproject.toml
src
  assets
    icon.png
  main.py
```

`main.py` is the entry point of your Flet application with `ft.run(main)` at the end. A different entry point could be specified with `--module-name` argument.

`assets` is an optional directory that contains application assets (images, sound, text and other files required by your app) as well as images used for package icons and splash screens.

If only `icon.png` (or other supported format such as `.bmp`, `.jpg`, `.webp`) is provided it will be used as a source image to generate all icons and splash screens for all platforms. See section below for more information about icons and splashes.

`pyproject.toml` contains the application metadata, lists its dependencies and controls build process. The list of project dependencies should contain at least `flet` package:

```toml title="pyproject.toml"
[project]
name = "myapp"
version = "0.1.0"
description = ""
readme = "README.md"
requires-python = ">=3.9"
authors = [
    { name = "Flet developer", email = "you@example.com" }
]
dependencies = [
  "flet"
]

[tool.flet]
org = "com.mycompany"
product = "MyApp"
company = "My Company"
copyright = "Copyright (C) 2025 by My Company"

[tool.flet.app]
path = "src"
```

::note
Though `requirements.txt` can also be used to list app requirements Flet recommends using `pyproject.toml` for new projects. If both `pyproject.toml` and `requirements.txt` exist the latter will be ignored.
::

::caution No pip freeze
Do not use `pip freeze > requirements.txt` command to create `requirements.txt` for the app that
will be running on mobile. As you run `pip freeze` command on a desktop `requirements.txt` will have
dependencies that are not intended to work on a mobile device, such as `watchdog`.

Hand-pick `requirements.txt` to have only direct dependencies required by your app, plus `flet`. 
::

The easiest way to start with the right project structure is to use `flet create` command:

```
flet create myapp
```

where `myapp` is a target directory.

## How it works

`flet build <target_platform>` command could be run from the root of Flet app directory:

```
<flet_app_directory> % flet build <target_platform>
```

where `<target_platform>` could be one of the following: `apk`, `aab`, `ipa`, `web`, `macos`, `windows`, `linux`.

When running from a different directory you can provide the path to a directory with Flet app:

```
flet build <target_platform> <path_to_python_app>
```

Build results are copied to `<python_app_directory>/build/<target_platform>`. You can specify a custom output directory with `--output` option:

```
flet build <target_platform> --output <path-to-output-dir>
```

`flet build` uses Flutter SDK and the number of Flutter packages to build a distribution package from your Flet app.

When you run `flet build <target_platform>` command it:

* Creates a new Flutter project in `{flet_app_directory}/build/flutter` directory from https://github.com/flet-dev/flet-build-template template. Flutter app will contain a packaged Python app in the assets and use `flet` and `serious_python` packages to run Python app and render its UI respectively. The project is ephemeral and deleted upon completion.
* Copies custom icons and splash images (see below) from `assets` directory into a Flutter project.
* Generates icons for all platforms using [`flutter_launcher_icons`](https://pub.dev/packages/flutter_launcher_icons) package.
* Generates splash screens for web, iOS and Android targets using [`flutter_native_splash`](https://pub.dev/packages/flutter_native_splash) package.
* Packages Python app using `package` command of [`serious_python`](https://pub.dev/packages/serious_python) package. `package` command installs pure and binary Python packages from https://pypi.org and https://pypi.flet.dev for selected platform. If configured, `.py` files of installed packages and/or application will be compiled to `.pyc` files. All files, except `build` directory will be added to a package asset.
* Runs `flutter build <target_platform>` command to produce an executable or an install package.
* Copies build results to `{flet_app_directory}/build/<target_platform>` directory.

## Including optional controls

If your app uses the following controls their packages must be added to a build command:

* Ad controls (`BannerAd` and `InterstitialAd`) implemented in `flet_ads` package.
* [`Audio`](/docs/controls/audio) control implemented in `flet_audio` package.
* [`AudioRecorder`](/docs/controls/audiorecorder) control implemented in `flet_audio_recorder` package.
* [`Flashlight`](/docs/controls/flashlight) control implemented in `flet_flashlight` package.
* [`Geolocator`](/docs/controls/geolocator) control implemented in `flet_geolocator` package.
* [`Lottie`](/docs/controls/lottie) control implemented in `flet_lottie` package.
* [`Map`](/docs/controls/map) control implemented in `flet_map` package.
* [`PermissionHandler`](/docs/controls/permissionhandler) control implemented in `flet_permission_handler` package.
* [`Rive`](/docs/controls/rive) control implemented in `flet_rive` package.
* [`Video`](/docs/controls/video) control implemented in `flet_video` package.
* [`WebView`](/docs/controls/webview) control implemented in `flet_webview` package.

Use `--include-packages <package_1> <package_2> ...` option to add Flutter packages with optional
Flet controls or use `tool.flet.flutter.dependencies` section in `pyproject.toml`.

For example, to build your Flet app with `Video` and `Audio` controls add `--include-packages flet_video flet_audio` to your `flet build` command:

```
flet build apk --include-packages flet_video flet_audio
```

or the same in `pyproject.toml`:

```toml
flutter.dependencies = ["flet_video", "flet_audio"]
```

or an alternative syntax with versions:

```toml
[tool.flet.flutter.dependencies]
flet_video = "1.0.0"
flet_audio = "2.0.0"
```

or with path to the package on your disk:

```toml
[tool.flet.flutter.dependencies.my_package]
path = "/path/to/my_package"
```

## Icons

You can customize app icons for all platforms (excluding Linux) with images in `assets` directory of your Flet app.

If only `icon.png` (or other supported format such as `.bmp`, `.jpg`, `.webp`) is provided it will be used as a source image to generate all icons.

* **iOS** - `icon_ios.png` (or any supported image format). Recommended minimum image size is 1024 px. Image should not be transparent (have alpha channel). Defaults to `icon.png` with alpha-channel automatically removed.
* **Android** - `icon_android.png` (or any supported image format). Recommended minimum image size is 192 px. Defaults to `icon.png`.
* **Web** - `icon_web.png` (or any supported image format). Recommended minimum image size is 512 px. Defaults to `icon.png`.
* **Windows** - `icon_windows.png` (or any supported image format). ICO will be produced of 256 px size. Defaults to `icon.png`. If `icon_windows.ico` file is provided it will be just copied to `windows/runner/resources/app_icon.ico` unmodified.
* **macOS** - `icon_macos.png` (or any supported image format). Recommended minimum image size is 1024 px. Defaults to `icon.png`.

## Splash screen

You can customize splash screens for iOS, Android and web applications with images in `assets` directory of your Flet app.

If only `splash.png` or `icon.png` (or other supported format such as `.bmp`, `.jpg`, `.webp`) is provided it will be used as a source image to generate all splash screen.

* **iOS (light)** - `splash_ios.png` (or any supported image format). Defaults to `splash.png` and then `icon.png`.
* **iOS (dark)** - `splash_dark_ios.png` (or any supported image format). Defaults to light iOS splash, then to `splash_dark.png`, then to `splash.png` and then `icon.png`.
* **Android (light)** - `splash_android.png` (or any supported image format). Defaults to `splash.png` and then `icon.png`.
* **Android (dark)** - `splash_dark_android.png` (or any supported image format).  Defaults to light Android splash, then to `splash_dark.png`, then to `splash.png` and then `icon.png`.
* **Web (light)** - `splash_web.png` (or any supported image format). Defaults to `splash.png` and then `icon.png`.
* **Web (dark)** - `splash_dark_web.png` (or any supported image format). Defaults to light web splash, then `splash_dark.png`, then to `splash.png` and then `icon.png`.

`--splash-color` option specifies background color for a splash screen in light mode. Defaults to `#ffffff`.

`--splash-dark-color` option specifies background color for a splash screen in dark mode. Defaults to `#333333`.

Configuring splash settings in `pyproject.toml`:

```toml
[tool.flet.splash]
color = "#FFFF00" # --splash-color
dark_color = "#8B8000" # --splash-dark-color
web = false # --no-web-splash
ios = false # --no-ios-splash
android = false # --no-android-splash
```

## Entry point

By default, `flet build` command assumes `main.py` as the entry point of your Flet application, i.e. the file with `ft.run(main)` at the end. A different entry point could be specified with `--module-name` argument or in `pyproject.toml`:

```toml
[tool.flet]
app.module = "main"
```

## Compilation and cleanup

`flet build` command is not compiling app `.py` files into `.pyc` by default which allows you to avoid (or defer?) discovery of any syntax errors in your app and successfully complete the packaging.

You can enable the compilation and cleanup with the following new options:

* `--compile-app` - compile app's `.py` files.
* `--compile-packages` - compile installed packages' `.py` files.
* `--cleanup-on-compile` - remove unnecessary files upon successful compilation.

Configuring compilation in `pyproject.toml`:

```toml
[tool.flet]
compile.app = true # --compile-app
compile.packages = true # --compile-packages
compile.cleanup = true # --cleanup-on-compile
```

## Permissions

`flet build` command allows granular control over permissions, features and entitlements embedded into `AndroidManifest.xml`, `Info.plist` and `.entitlements` files.

See platform guides for setting specific [iOS](/docs/publish/ios), [Android](/docs/publish/android) and [macOS](/docs/publish/macos) permissions.

### Cross-platform permissions

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

Configuring cross-platform permissions in `pyproject.toml`:

```toml
[tool.flet]
permissions = ["camera", "microphone"]
```

## Versioning

You can provide a version information for built executable or package with `--build-number` and `--build-version` arguments. This is the information that is used to distinguish one build/release from another in App Store and Google Play and is shown to the user in about dialogs.

`--build-number` - an integer number (defaults to `1`), an identifier used as an internal version number.
Each build must have a unique identifier to differentiate it from previous builds.
It is used to determine whether one build is more recent than another, with higher numbers indicating
more recent build.

`--build-version` - a "x.y.z" string (defaults to `1.0.0`) used as the version number shown to users. For each new
version of your app, you will provide a version number to differentiate it from previous versions.

Configuring display version and version number in `pyproject.toml`:

```toml
[project]
name = "my_app"
version = "1.0.0"
description = "My Flet app"
authors = [
  {name = "John Smith", email = "john@email.com"}
]
dependencies = ["flet==0.25.0"]

[tool.flet]
build_number = 1
```

## Customizing packaging template

To create a temporary Flutter project `flet build` uses [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/) template stored in https://github.com/flet-dev/flet-build-template repository.

You can customize that template to suit your specific needs and then use it with `flet build`.

`--template` option can be used to provide the URL to the repository or path to a directory with your own template. Use `gh:` prefix for GitHub repos, e.g. `gh:{my-org}/{my-repo}` or provide a full path to a Git repository, e.g. `https://github.com/{my-org}/{my-repo}.git`.

For Git repositories you can checkout specific branch/tag/commit with `--template-ref` option.

`--template-dir` option specifies a relative path to a cookiecutter template in a repository given by `--template` option. When `--template` option is not used, this option specifies path relative to the `<user-directory>/.cookiecutters/flet-build-template`.

Configuring template in `pyproject.toml`:

```toml
[tool.flet.template]
path = "gh:some-github/repo" # --template
dir = "" # --template-dir
ref = "" # --template-ref
```

## Extra args to `flutter build` command

`--flutter-build-args` option allows passing extra arguments to `flutter build` command called during the build process. The option can be used multiple times.

For example, if you want to add `--no-tree-shake-icons` option:

```
flet build macos --flutter-build-args=--no-tree-shake-icons
```

To pass an option with a value:

```
flet build ipa --flutter-build-args=--export-method --flutter-build-args=development
```

Configuring Flutter build extra args:

```toml
[tool.flet]
flutter.build_args = [
    "--some-flutter-arg-1",
    "--some-flutter-arg-2"
]
```

## Verbose logging

`--verbose` or `-vv` option allows to see the output of all commands during `flet build` run.
We might ask for a detailed log if you need support.

## Console output

All Flet apps output to `stdout` and `stderr` (e.g. all `print()` statements or `sys.stdout.write()` calls, Python `logging` library) is now redirected to `console.log` file with a full path to it stored in `FLET_APP_CONSOLE` environment variable.

Writes to that file are unbuffered, so you can retrieve a log in your Python program at any moment with a simple:

```python
with open(os.getenv("FLET_APP_CONSOLE"), "r") as f:
    log = f.read()
```

`AlertDialog` or any other control can be used to display the value of `log` variable.

When the program is terminated by calling `sys.exit()` with exit code `100` (magic code)
the entire log will be displayed in a scrollable window.

```python
import sys
sys.exit(100)
```

Calling `sys.exit()` with any other exit code will terminate (close) the app without displaying a log.
