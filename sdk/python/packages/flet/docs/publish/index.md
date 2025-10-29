# Publishing Flet app

Flet CLI provides [`flet build`](../cli/flet-build.md) command that allows packaging Flet app into a standalone executable
or install package for distribution.

## Prerequisites

### Platform matrix

The following matrix shows which OS you should run `flet build` command on in
order to build a package for specific platform:

<style>
    table {
      border-collapse: collapse;
      width: 100%;
      text-align: center;
    }
    th, td {
      border: 1px solid #000;
    }
</style>
<table border="1" cellspacing="0" cellpadding="6" style="border-collapse: collapse; width: 100%; text-align: center;">
  <thead>
    <tr>
      <th rowspan="2" style="vertical-align: middle; text-align: center;">Run on</th>
      <th colspan="6" style="text-align: center;">Target Platform</th>
    </tr>
    <tr>
      <th style="text-align: center;"><a href="android.md">apk/aab</a></th>
      <th style="text-align: center;"><a href="ios.md">ipa</a></th>
      <th style="text-align: center;"><a href="macos.md">macos</a></th>
      <th style="text-align: center;"><a href="linux.md">linux</a></th>
      <th style="text-align: center;"><a href="windows.md">windows</a></th>
      <th style="text-align: center;"><a href="web/index.md">web</a></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>macOS</strong></td>
      <td>✅</td>
      <td>✅</td>
      <td>✅</td>
      <td></td>
      <td></td>
      <td>✅</td>
    </tr>
    <tr>
      <td><strong>Windows</strong></td>
      <td>✅</td>
      <td></td>
      <td></td>
      <td><a href="https://docs.microsoft.com/en-us/windows/wsl/about">✅ (WSL)</a></td>
      <td>✅</td>
      <td>✅</td>
    </tr>
    <tr>
      <td><strong>Linux</strong></td>
      <td>✅</td>
      <td></td>
      <td></td>
      <td>✅</td>
      <td></td>
      <td>✅</td>
    </tr>
  </tbody>
</table>

### Flutter SDK

[Flutter](https://flutter.dev) is required to build Flet apps for any platform.

If the minimum required version of the Flutter SDK is not already available in the system `PATH`, it will be automatically downloaded and installed (in the `$HOME/flutter/{version}` directory) during the first build process.

<!-- TODO: Add a link to a table containing a map for Flet to min Flutter version required -->

## Project structure

`flet build` command assumes the following minimal Flet project structure:

```tree
README.md
pyproject.toml # (1)!
src
    assets # (2)!
        icon.png
    main.py # (3)!
```

1. Serves as the main configuration file for your application.
    It includes metadata, dependencies, and build settings.
    At a minimum, the `dependencies` section should specify `flet` package.

    /// admonition | Example
        type: example
    Below is an example of a `pyproject.toml` file:
    ```toml title="pyproject.toml"
    [project]
    name = "example"
    version = "0.1.0"
    description = "An Example."
    readme = "README.md"
    requires-python = ">=3.9"
    authors = [{ name = "Me", email = "me@example.com" }]
    dependencies = [
      "flet"
    ]

    [tool.flet.app]
    path = "src"

    [tool.flet]
    org = "com.mycompany"
    product = "Example"
    company = "My Company"
    copyright = "Copyright (C) 2025 by My Company"
    ```
    ///

2. An optional directory that contains application assets
    (images, sound, text and other files required by your app) as well as images
    used for package [icons](#icons) and [splash screens](#splash-screen).
3. The main [entry point](#entry-point) of your Flet app. It usually contains the call to `ft.run()`.


/// admonition | Using `requirements.txt` instead of `pyproject.toml`
Instead of a `pyproject.toml` file, you can also use `requirements.txt` file to specify dependencies.

In this case, two things to keep in mind:

- if both files are present, `flet build` will ignore `requirements.txt`.
- don't use `pip freeze > requirements.txt` to generate this file or fill it with dependencies,
  as it may include packages incompatible with the target platform. Instead, hand-pick and include
  only the direct dependencies required by your app, including `flet`.
///

/// admonition | Tip
    type: tip
To quickly set up a project with the correct structure, use the [`flet create`](../cli/flet-create.md) command:

```bash
flet create <project-name>
```

Where `<project-name>` is the name for your project directory.
///

/// admonition | Note
Throughout this documentation, the following placeholders are used:

- `<target_platform>` - one of the following: `apk`, `aab`, `ipa`, `web`, `macos`, `windows`, `linux`.
- `<flet_app_directory>` - the path to the directory containing your Flet project/app.
- `PLATFORM` - one of the following: `android`, `ios`, `web`, `macos`, `windows`, `linux`.
///

## How it works

`flet build <target_platform>` command could be run from the root of Flet app directory:

```
<flet_app_directory> % flet build <target_platform>
```

When running from a different directory you can provide the path to a directory with Flet app:

```
flet build <target_platform> <path_to_python_app>
```

Build results are copied to `<flet_app_directory>/build/<target_platform>` by default.
See [this](#custom-output-directory) to set a custom location for build results.

`flet build` uses Flutter SDK and the number of Flutter packages to build a distribution package from your Flet app.

When you run `flet build <target_platform>` command it:

* Creates a new Flutter project in `{flet_app_directory}/build/flutter` directory from https://github.com/flet-dev/flet-build-template template. Flutter app will contain a packaged Python app in the assets and use `flet` and `serious_python` packages to run Python app and render its UI respectively. The project is ephemeral and deleted upon completion.
* Copies custom icons and splash images (see below) from `assets` directory into a Flutter project.
* Generates icons for all platforms using [`flutter_launcher_icons`](https://pub.dev/packages/flutter_launcher_icons) package.
* Generates splash screens for web, iOS and Android targets using [`flutter_native_splash`](https://pub.dev/packages/flutter_native_splash) package.
* Packages Python app using `package` command of [`serious_python`](https://pub.dev/packages/serious_python) package. `package` command installs pure and binary Python packages from https://pypi.org and https://pypi.flet.dev for selected platform. If configured, `.py` files of installed packages and/or application will be compiled to `.pyc` files. All files, except `build` directory will be added to a package asset.
* Runs `flutter build <target_platform>` command to produce an executable or an installable package.
* Copies build results to `{flet_app_directory}/build/<target_platform>` directory.

## Including Extensions

If your app uses Flet extensions (third-party packages),
simply add them to your project's dependencies:

/// tab | PyPI
```toml
dependencies = [
  "flet-extension",
  "flet",
]
```
///
/// tab | Git Repo
```toml
dependencies = [
"flet-extension @ git+https://github.com/account/flet-extension.git",
"flet",
]
```
///
/// tab | Local Package
```toml
dependencies = [
"flet-extension @ file:///path/to/flet-extension",
"flet",
]
```
///

Example of extensions can be found here.

## Product Name

The display name shown in window titles, about dialogs, and app launchers.
This is the user-facing name of your application.

**Default:** Derived from `project.name`, `tool.poetry.name` in `pyproject.toml`,
or the name of your Flet app directory.

/// tab | `flet build`
```bash
flet build <target_platform> --product "My Awesome App"
```
///
/// tab | `pyproject.toml`

/// tab | `[tool.flet]`
```toml
[tool.flet]
product = "My Awesome App"
```
///

///

## Company Name

The company name displayed in about app dialogs and metadata.

/// tab | `flet build`
```bash
flet build <target_platform> --company "My Company Inc."
```
///
/// tab | `pyproject.toml`

/// tab | `[tool.flet]`
```toml
[tool.flet]
company = "My Company Inc."
```
///

///

## Copyright

Copyright text displayed in about app dialogs and metadata.

/// tab | `flet build`
```bash
flet build <target_platform> --copyright "Copyright © 2025 My Company Inc."
```
///
/// tab | `pyproject.toml`

/// tab | `[tool.flet]`
```toml
[tool.flet]
copyright = "Copyright © 2025 My Company Inc."
```
///

///

## Flutter dependencies

Adding a Flutter package can be done in the `pyproject.toml` as follows:

/// tab | `flet build`
```bash
flet build
```
///
/// tab | `pyproject.toml`

/// tab | `[tool.flet]`
```toml
[tool.flet]
flutter.dependencies = [
    "package_1",
    "package_2",
]
```
///
/// tab | `[tool.flet.flutter.dependencies]`
```toml
[tool.flet.flutter.dependencies]
package_1 = "x.y.z"
package_2 = "x.y.z"
```
///
/// tab | `[tool.flet.flutter.dependencies.LOCAL_PACKAGE]`
```toml
[tool.flet.flutter.dependencies.LOCAL_PACKAGE]
path = "/path/to/LOCAL_PACKAGE"
```
///

///

## Custom output directory

By default, the build output is saved in the `<flet_app_directory>/build/<target_platform>` directory.

This can be customized as follows:

/// tab | CLI
```bash
flet build <target_platform> --output <path-to-output-dir>
```
///
/// tab | `pyproject.toml`

/// tab | `[tool.flet]`
```toml
[tool.flet]
output = "<path-to-output-dir>"
```
///

///

## Icons

You can customize app icons for all platforms (except Linux) using image files placed in
the `assets` directory of your Flet app.

If a platform-specific icon (as in the table below) is not provided, `icon.png`
(or any supported format like `.bmp`, `.jpg`, or `.webp`) will be used as fallback.
For the iOS platform, transparency (alpha channel) will be automatically removed, if present.

| Platform | File Name                                | Recommended Size | Notes                                                                                       |
|----------|------------------------------------------|------------------|---------------------------------------------------------------------------------------------|
| iOS      | `icon_ios.png`                           | ≥ 1024×1024 px   | Transparency (alpha channel) is not supported and will be automatically removed if present. |
| Android  | `icon_android.png`                       | ≥ 192×192 px     |                                                                                             |
| Web      | `icon_web.png`                           | ≥ 512×512 px     |                                                                                             |
| Windows  | `icon_windows.ico` or `icon_windows.png` | 256×256 px       | `.png` file will be internally converted to a 256×256 px `.ico` icon.                        |
| macOS    | `icon_macos.png`                         | ≥ 1024×1024 px   |                                                                                             |


## Splash screen

A splash screen is a visual element displayed when an app is launching,
typically showing a logo or image while the app loads.

You can customize splash screens for iOS, Android, and Web platforms by placing image files in
the `assets` directory of your Flet app.

If platform-specific splash images are not provided, Flet will fall back to `splash.png`.
If that is also missing, it will use `icon.png` or any supported format such as `.bmp`, `.jpg`, or `.webp`.

### Splash images

| Platform | Dark Fallback Order                                                                              | Light Fallback Order                             |
|----------|--------------------------------------------------------------------------------------------------|--------------------------------------------------|
| iOS      | `splash_dark_ios.png` → `splash_ios.png` → `splash_dark.png` → `splash.png` → `icon.png`         | `splash_ios.png` → `splash.png` → `icon.png`     |
| Android  | `splash_dark_android.png` → `splash_android.png` → `splash_dark.png` → `splash.png` → `icon.png` | `splash_android.png` → `splash.png` → `icon.png` |
| Web      | `splash_dark_web.png` → `splash_web.png` → `splash_dark.png` → `splash.png` → `icon.png`         | `splash_web.png` → `splash.png` → `icon.png`     |

### Splash Background Colors

You can customize splash background colors using the following options:

- **Splash Color:** Background color for light mode splash screens (defaults to `#ffffff`)
- **Splash Dark Color:** Background color for dark mode splash screens (defaults to `#333333`)

/// tab | `pyproject.toml`

/// tab | `[tool.flet]`
```toml
[tool.flet]
splash.color = "#ffffff"
splash.dark_color = "#333333"
```
///
/// tab | `[tool.flet.splash]`
```toml
[tool.flet.splash]
color = "#ffffff"
dark_color = "#333333"
```
///

///
/// tab | `flet build`
```bash
flet build <target_platform> --splash-color #ffffff --splash-dark-color #333333
```
///

### Disabling Splash Screens

Splash screens are enabled by default.

See the respective platform docs for more information: [iOS](ios.md#disable-splash-screen),
[Android](android.md#disable-splash-screen), and [Web](web/static-website/index.md#disable-splash-screen).

## Boot screen

The boot screen is shown while the archive with Python app is being unpacked to a device file system.
It is shown after splash screen and before startup screen. App archive does not include 3rd-party site packages.
If the archive is small and its unpacking is fast you could leave this screen disabled (default).

Below are its customizable properties and respective defaults:

/// tab | `[tool.flet.app.boot_screen]`
```toml
[tool.flet.app.boot_screen]
show = false
message = "Preparing the app for its first launch…"
```
///
/// tab | `[tool.flet.PLATFORM.app.boot_screen]`
Its values can be set platform-specific too:

```toml
[tool.flet.android.app.boot_screen]
show = false
message = "Preparing the app for its first launch…"
```
///

## Startup screen

The startup screen is shown while the archive (`app.zip`), which contains the 3rd-party site packages (Android only),
is being unpacked and the Python app is starting.

/// admonition | Note
Startup screen is shown after the [boot screen](#boot-screen).
///

Below are its customizable properties and respective defaults:

/// tab | `[tool.flet.app.startup_screen]`
```toml
[tool.flet.app.startup_screen]
show = false
message = "Starting up the app…"
```
///
/// tab | `[tool.flet.PLATFORM.app.startup_screen]`
Its values can be set platform-specific too:

```toml
[tool.flet.android.app.startup_screen]
show = false
message = "Starting up the app…"
```
///

## Entry point

The Flet application entry (or starting) point refers to the file that contains the call to `ft.run()`.

By default, Flet assumes this file is named `main.py`.
However, if your entry point is different (for example, `start.py`), you can specify it as follows:

/// tab | `pyproject.toml`

/// tab | `[tool.flet]`
```toml
[tool.flet]
app.module = "start.py"
```
///
/// tab | `[tool.flet.app]`
```toml
[tool.flet.app]
module = "start.py"
```
///

///
/// tab | `flet build`
```bash
flet build <target_platform> --module-name start.py
```
///

## Compilation and cleanup

By default, Flet does **not** compile your app files during packaging.
This allows the build process to complete even if there are syntax errors,
which can be useful for debugging or rapid iteration.

* `compile-app`: compile app's `.py` files
* `compile-packages`: compile site/installed packages' `.py` files
* `cleanup-packages`: remove unnecessary package files upon successful compilation

Enable one or more of them as follows:

/// tab | `pyproject.toml`

/// tab | `[tool.flet]`
```toml
[tool.flet]
compile.app = true
compile.packages = true
compile.cleanup = true
```
///
/// tab | `[tool.flet.compile]`
```toml
[tool.flet.compile]
app = true
packages = true
cleanup = true
```
///

///
/// tab | `flet build`
```bash
flet build <target_platform> --compile-app --compile-packages --cleanup-packages
```
///

## Permissions

`flet build` command allows granular control over permissions, features and entitlements
embedded into `AndroidManifest.xml`, `Info.plist` and `.entitlements` files.

See platform guides for setting specific [iOS](ios.md), [Android](android.md) and [macOS](macos.md) permissions.

### Cross-platform permissions

There are pre-defined permissions that mapped to `Info.plist`, `*.entitlements` and `AndroidManifest.xml`
for respective platforms.

Setting permissions can be done as follows:

/// tab | `pyproject.toml`

/// tab | `[tool.flet]`
```toml
[tool.flet]
permissions = ["camera", "microphone"]
```
///

///
/// tab | `flet build`
```bash
flet build <target_platform> --permissions camera microphone
```
///

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

## Versioning

### Build Number

An integer identifier (defaults to `1`) used internally to distinguish one build from another.
Each new build must have a unique, incrementing number; higher numbers indicate more recent builds.

It's value can be set as follows:

/// tab | `pyproject.toml`

/// tab | `[tool.flet]`
```toml
[tool.flet]
build_number = 1
```
///

///
/// tab | `flet build`
```bash
flet build <target_platform> --build-number 1
```
///

### Build Version

A user‑facing version string in `x.y.z` format (defaults to `1.0.0`).
Increment this for each new release to differentiate it from previous versions.

It's value can be set as follows:

/// tab | `pyproject.toml`

/// tab | `[project]`
```toml
[project]
version = "1.0.0"
```
///
/// tab | `[tool.poetry]`
```toml
[tool.poetry]
version = "1.0.0"
```
///

///
/// tab | `flet build`
```bash
flet build <target_platform> --build-version 1.0.0
```
///

## Customizing build template

By default, `flet build` creates a temporary Flutter project using a
[cookiecutter](https://cookiecutter.readthedocs.io/en/stable/) template from the flet-dev/flet-build-template
repository. The version of the template used is determined by the [template reference](#template-reference) option,
which defaults to the current Flet version.

You can customize this behavior by specifying your own template source, reference, and subdirectory.

### Template Source

Defines the location of the template to be used. Defaults to `gh:flet-dev/flet-build-template`,
the [official Flet template](https://github.com/flet-dev/flet-build-template).

Valid values include:

- A GitHub repository using the `gh:` prefix (e.g., `gh:org/template`)
- A full Git URL (e.g., `https://github.com/org/template.git`)
- A local directory path

It's value can be set in either of the following ways:

- via Command Line:
  ```bash
  flet build apk --template gh:flet-dev/flet-build-template
  ```

- via `pyproject.toml`:
  ```toml
  [tool.flet.template]
  url = "gh:flet-dev/flet-build-template"
  ```

### Template Reference

Defines the branch, tag, or commit to check out from the [template source](#template-source).
Defaults to the version of Flet installed.

It's value can be set as follows:

/// tab | `pyproject.toml`

/// tab | `[tool.flet.template]`
```toml
[tool.flet.template]
ref = "main"
```
///

///
/// tab | `flet build`
```bash
flet build <target_platform> --template-ref main
```
///

### Template Directory

Defines the relative path to the cookiecutter template.
If [template source](#template-source) is set, the path is treated as a
subdirectory within its root; otherwise, it is relative to`<user-directory>/.cookiecutters/flet-build-template`.

It's value can be set as follows:

/// tab | `pyproject.toml`

/// tab | `[tool.flet.template]`
```toml
[tool.flet.template]
url = "gh:org/template"
dir = "sub/directory"
```
///

///
/// tab | `flet build`
```bash
flet build <target_platform> --template gh:org/template --template-dir sub/directory
```
///

## Deep linking

[Deep linking](https://en.wikipedia.org/wiki/Mobile_deep_linking) allows users to
navigate directly to specific content within a mobile app
using a URI (Uniform Resource Identifier). Instead of opening the app's homepage, deep
links direct users to a specific page, feature, or content within the app, enhancing
user experience and engagement.

- **Scheme**: deep linking URL scheme, e.g. `"https"` or `"myapp"`.
- **Host**: deep linking URL host.

See [this](https://docs.flutter.dev/ui/navigation/deep-linking) Flutter guide for more information.

It can be configured as follows:

/// tab | `flet build`
```bash
flet build ipa --deep-linking-scheme "https" --deep-linking-host "mydomain.com"
```
///
/// tab | `pyproject.toml`

/// tab | `[tool.flet]`
```toml
[tool.flet]
deep_linking.scheme = "https"
deep_linking.host = "mydomain.com"
```
///
/// tab | `[tool.flet.deep_linking]`
```toml
[tool.flet.deep_linking]
scheme = "https"
host = "mydomain.com"
```
///
/// tab | `[tool.flet.PLATFORM.deep_linking]`
`PLATFORM` can be `android` or `ios`.
```toml
[tool.flet.PLATFORM.deep_linking]
scheme = "https"
host = "mydomain.com"
```
///

///



### Project name

The project name in C-style identifier format (lowercase alphanumerics with underscores).
It is used to build [bundle ID](#bundle-id) and as a name for bundle executable.

**Default:** the name of your Flet project directory

/// tab | `flet build`
```bash
flet build <target_platform> --project my-app
```
///
/// tab | `pyproject.toml`

/// tab | `[tool.flet]`
```toml
[tool.flet]
project = "my-app"
```
///

///

### Organization name

The organization name in reverse domain name notation, typically in the form `com.mycompany`.

If you do not provide an explicit value for the organization name, but specify the [bundle ID](#bundle-id),
the organization name will be automatically generated by taking the part of the bundle ID before the last dot.
For example, with a bundle ID of `com.mycompany.myapp`, the organization name becomes `com.mycompany`.

**Default:** `"com.flet"`

/// tab | `flet build`
```bash
flet build <target_platform> --org com.mycompany
```
///
/// tab | `pyproject.toml`

/// tab | `[tool.flet]`
```toml
[tool.flet]
org = "com.mycompany"
```
///

///

## Bundle ID

The bundle ID for the application, typically in the form `"com.mycompany.app-name"`.

If not explicitly specified, it is formed by combining the [organization name](#organization-name)
and the [project name](#project-name).

**Default:** `"[organization-name].[project-name]"`

/// tab | `flet build`
```bash
flet build <target_platform> --bundle-id com.mycompany.example-app
```
///
/// tab | `pyproject.toml`

/// tab | `[tool.flet]`
```toml
[tool.flet]
bundle_id = "com.mycompany.example-app"
```
///
/// tab | `[tool.flet.PLATFORM]`
```toml
[tool.flet.PLATFORM]
bundle_id = "com.mycompany.example-app-platform"
```
///

///

## Additional `flutter build` Arguments

During the `flet build` process, `flutter build` command gets called internally to
package your app for the specified platform.

It's value can be set in either of the following ways:

/// tab | `pyproject.toml`

/// tab | `[tool.flet]`
```toml
[tool.flet]
flutter.build_args = [
  "--no-tree-shake-icons",
  "--export-method", "development"
]
```
///
/// tab | `[tool.flet.flutter]`
```toml
[tool.flet.flutter]
build_args = [
  "--no-tree-shake-icons",
  "--export-method", "development"
]
```
///

/// tab | `flet build`
```bash
flet build <target_platform> --flutter-build-args=--no-tree-shake-icons # (1)!

# OR as key-value

flet build <target_platform> --flutter-build-args=--export-method --flutter-build-args=development
```

1. `--flutter-build-args` can be used multiple times.
///

## Verbose logging

The `-v` (or `--verbose`) and `-vv` flags enables detailed output from all commands during the flet build process.
Use `-v` for standard/basic verbose logging, or `-vv` for even more detailed output (higher verbosity level).
If you need support, we may ask you to share this verbose log.

## Console output

All output from Flet apps—such as `print()` statements, `sys.stdout.write()` calls, and messages from the Python
logging module—is now redirected to a `console.log` file. The full path to this file is available via the
`FLET_APP_CONSOLE` environment variable.

The log file is written in an unbuffered manner, allowing you to read it at any point in your Python program using:

```python
with open(os.getenv("FLET_APP_CONSOLE"), "r") as f:
  log = f.read()
```

You can then display the `log` content using an `AlertDialog` or any other Flet control.

If your program calls sys.exit(100), the complete log will automatically be shown in a scrollable window.
This is a special “magic” exit code for debugging purposes:

```python
import sys
sys.exit(100)
```

Calling `sys.exit()` with any other code will terminate the app without displaying the log.
