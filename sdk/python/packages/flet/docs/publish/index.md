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

If the minimum required version of the Flutter SDK is not already
available in the system `PATH`, it will be automatically downloaded
and installed (in the `$HOME/flutter/{version}` directory) during
the first build process.

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
    requires-python = ">=3.10"
    authors = [{ name = "Me", email = "me@example.com" }]
    dependencies = [
      "flet"
    ]

    [tool.flet]
    org = "com.mycompany"
    product = "My App"
    company = "My Company"
    copyright = "Copyright (C) 2025 by My Company"

    [tool.flet.app]
    path = "src"
    ```
    ///

2. An optional directory that contains application assets
    (images, sound, text, and other files required by your app) as well as images
    used for package [icons](#icons) and [splash screens](#splash-screen).
3. The main [entry point](#entry-point) of your Flet app. It usually contains the call to `ft.run()`.


/// admonition | Tip
    type: tip
To quickly set up a project with the correct structure, use the [`flet create`](../cli/flet-create.md) command:

```bash
flet create <project-name>
```

Where `<project-name>` is the name for your project directory.
///

/// admonition | Using `requirements.txt` instead of `pyproject.toml`
Instead of a `pyproject.toml` file, you can also use `requirements.txt` file to specify dependencies.

In this case, two things to keep in mind:

- if both files are present, `flet build` will ignore `requirements.txt`.
- don't use `pip freeze > requirements.txt` to generate this file or fill it with dependencies,
  as it may include packages incompatible with the target platform. Instead, hand-pick and include
  only the direct dependencies required by your app, including `flet`.
///

## How it works

`flet build <target_platform>` command could be run from the root of Flet app project directory:

```bash
<flet_app_directory> % flet build <target_platform>
```

When running from a different directory, you can provide the path to a directory with Flet app:

```bash
flet build <target_platform> <path_to_python_app>
```

Build results are copied to `<flet_app_directory>/build/<target_platform>` by default.
See [this](#custom-output-directory) to set a custom location for build results.

`flet build` uses Flutter SDK and the number of Flutter packages to build a distribution package from your Flet app.

When you run `flet build <target_platform>`, the following steps are performed (using the default configuration):

* A new Flutter project is created in `{flet_app_directory}/build/flutter` directory from [flet-dev/flet-build-template](https://github.com/flet-dev/flet-build-template) template. Flutter app will contain a packaged Python app in the assets and use `flet` and `serious_python` packages to run Python app and render its UI respectively. The project is ephemeral and deleted upon completion.
* Custom icons and splash images are copied from `assets` directory into a Flutter project.
* Icons are generated for all platforms using [`flutter_launcher_icons`](https://pub.dev/packages/flutter_launcher_icons) package.
* Splash screens are generated for web, iOS and Android targets using [`flutter_native_splash`](https://pub.dev/packages/flutter_native_splash) package.
* Python app is packaged using `package` command of [`serious_python`](https://pub.dev/packages/serious_python), which installs pure and binary Python packages from [pypi.org](https://pypi.org) and [pypi.flet.dev](https://pypi.flet.dev) for the selected platform. If configured, `.py` files of installed packages and/or application will be compiled to `.pyc` files. All files, except `build` directory will be added to a package asset.
* `flutter build <target_platform>` command is executed to produce an executable or an installable package.
* Build results are copied to `{flet_app_directory}/build/<target_platform>` directory.

## Configuration options

/// admonition | Placeholders
Throughout this documentation, the following placeholders are used:

- [`<target_platform>`](../cli/flet-build.md#target_platform) - one of the following: `apk`, `aab`, `ipa`, `web`, `macos`, `windows`, `linux`.
- `<PLATFORM>` - one of the following: `android`, `ios`, `web`, `macos`, `windows`, `linux`.
- `<flet_app_directory>` - the path to the directory containing your Flet project/app.
- [`<python_app_path>`](../cli/flet-build.md#python_app_path)
- `<flet_version>` - the version of Flet in use. Can be known by running `flet --version` or `uv run python -c "import flet; print(flet.__version__)"` in the terminal.
///

/// admonition | Understanding `pyproject.toml` structure
Flet loads `pyproject.toml` as a nested dictionary and looks up settings by
dot-separated paths (for example, `tool.flet.web.base_url`).

For example, the two forms below are equivalent (will be internally resolved to the same key-value pair):

- **Form 1** (will be used/preferred throughout this documentation)
    ```toml
    [tool.flet.section]
    key = "value"
    ```

- **Form 2**
    ```toml
    [tool.flet]
    section.key = "value"
    ```

But they are different or should not be confused with the
below ("quoted keys" are literals and do not create nesting):

```toml
[tool.flet]
"section.key" = "value"
```
///

### Entry point

This is where the execution of your Flet app begins. It is the Python file that
contains the call to `flet.run()` or `flet.render()`.
If provided without the Python file extension (`.py`), it will be appended internally.

[//]: # (Also, it must exist in the `package_app_path`.)

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--module-name`](../cli/flet-build.md#-module-name)
2. `[tool.flet.app].module`
3. `"main.py"`

#### Example

/// tab | `flet build`
```bash
flet build <target_platform> --module-name app.py
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.app]
module = "app.py"
```
///

### Project name

The project name in C-style identifier format (lowercase alphanumerics with underscores).
It is used for [bundle IDs](#bundle-id) and other internal identifiers.

Its value is internally slugified and hyphens become underscores
(e.g., `my-app` becomes `my_app`) to keep identifier names safe.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--project`](../cli/flet-build.md#-project)
2. `[project].name`
3. project/app directory name

#### Example

/// tab | `flet build`
```bash
flet build <target_platform> --project my_app
```
///
/// tab | `pyproject.toml`
```toml
[project]
name = "my_app"
```
///

### Product name

The display (user-facing) name shown in window titles, launcher labels, and about dialogs.

It does **not** control the on-disk executable or bundle
name. Use the [artifact name](#artifact-name) for artifact naming.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--product`](../cli/flet-build.md#-product)
2. `[tool.flet].product`
3. [`--project`](../cli/flet-build.md#-project)
4. `[project].name`
5. project/app directory name

#### Example

/// tab | `flet build`
```bash
flet build <target_platform> --product "My Awesome App"
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet]
product = "My Awesome App"
```
///

### Artifact name

The on-disk name for executables and/or app bundles. For example, on Windows it
determines the name of the `.exe` file, and on macOS it sets the name of the `.app` bundle.

It does **not** affect [bundle ID](#bundle-id)s or package identifiers.

It can contain spaces or accents.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--artifact`](../cli/flet-build.md#-artifact)
2. `[tool.flet].artifact`
3. [`--project`](../cli/flet-build.md#-project)
4. `[project].name`
5. project/app directory name

#### Example

/// tab | `flet build`
```bash
flet build <target_platform> --artifact "My Awesome App"
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet]
artifact = "My Awesome App"
```
///

### Organization name

The organization name in reverse domain name notation, typically in the form `com.mycompany`.

If you do not provide an explicit value for the organization name,
but specify the [bundle ID](#bundle-id), the organization name will be
internally constructed by taking the part of this [bundle ID](#bundle-id)
before the last dot. For example, with a bundle ID of `com.mycompany.myapp`,
the organization name becomes `com.mycompany`.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--org`](../cli/flet-build.md#-org)
2. `[tool.flet.<PLATFORM>].org`
3. `[tool.flet].org`
4. `"com.flet"`

#### Example

/// tab | `flet build`
```bash
flet build <target_platform> --org com.mycompany
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet]     # or [tool.flet.<PLATFORM>]
org = "com.mycompany"
```
///

### Bundle ID

The bundle ID for the application, typically in the form `"com.mycompany.my_app"`.

If not explicitly specified, it is formed by combining the [organization name](#organization-name)
and the [project name](#project-name).

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--bundle-id`](../cli/flet-build.md#-bundle-id)
2. `[tool.flet.<PLATFORM>].bundle_id`
3. `[tool.flet].bundle_id`
4. Default: `"[organization-name].[project-name]"`

#### Example

/// tab | `flet build`
```bash
flet build <target_platform> --bundle-id com.mycompany.my_app
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet] # or [tool.flet.<PLATFORM>]
bundle_id = "com.mycompany.my_app"
```
///

### Company Name

The company name displayed in about app dialogs and metadata.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--company`](../cli/flet-build.md#-company)
2. `[tool.flet].company`
3. `"Your Company"`

#### Example

/// tab | `flet build`
```bash
flet build <target_platform> --company "My Company Inc."
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet]
company = "My Company Inc."
```
///

### Copyright

Copyright text displayed in about app dialogs and metadata.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--copyright`](../cli/flet-build.md#-copyright)
2. `[tool.flet].copyright`
3. `"Copyright (c) 2023 Your Company"`

#### Example

/// tab | `flet build`
```bash
flet build <target_platform> --copyright "Copyright © 2026 My Company Inc."
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet]
copyright = "Copyright © 2026 My Company Inc."
```
///

### Versioning

#### Build Number

An integer identifier (defaults to `1`) used internally to distinguish one build from another.
Each new build must have a unique, incrementing number; higher numbers indicate more recent builds.

##### Resolution order

Its value is determined in the following order of precedence:

1. [`--build-number`](../cli/flet-build.md#-build-number)
2. `[tool.flet].build_number`

##### Example

/// tab | `flet build`
```bash
flet build <target_platform> --build-number 1
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet]
build_number = 1
```
///

#### Build Version

A user‑facing version string in `x.y.z` format (defaults to `1.0.0`).
Increment this for each new release to differentiate it from previous versions.

##### Resolution order

Its value is determined in the following order of precedence:

1. `--build-version`
2. `[project].version`
3. `[tool.poetry].version`

##### Example

/// tab | `flet build`
```bash
flet build <target_platform> --build-version 1.0.0
```
///
/// tab | `pyproject.toml`
```toml
[project]
version = "1.0.0"
```
///

### Output directory

The directory where the build output is saved.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--output`](../cli/flet-build.md#-output) (or `-o`)
2. `[tool.flet].output`
3. `<python_app_path>/build/<target_platform>`

#### Example

/// tab | `flet build`
```bash
flet build <target_platform> --output <path-to-output-dir>
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet]
output = "<path-to-output-dir>"
```
///

### App dependencies

These are the Python packages that your Flet app depends on to function correctly.

#### Resolution order

Its value is determined in the following order of precedence:

- `[project].dependencies` (PEP 621) or `[tool.poetry].dependencies`
- If `[tool.flet.<PLATFORM>].dependencies` is set, its values are appended to the above list.
- If the result of all above is empty and `requirements.txt` exists in `<python_app_path>`, it is used.
- If the result of all the above is empty, `flet==<flet_version>` is used.

#### Example

/// tab | `pyproject.toml`
```toml
[project]
dependencies = [
    "flet",
    "requests",
]

[tool.flet.<PLATFORM>]
dependencies = [
    "dep1",
    "dep2",
]
```
///

### Source packages

If one or more of your app dependencies do not provide a pre-built binary distribution (wheels),
they must be built from source distribution and packaged as `.whl` files.

A source distribution is a source archive (usually `.tar.gz` or `.zip`) that contains:
the package's Python source code, package metadata, and instructions on how to build
and install the package.

To know which packages require source distributions, you can run `pipdeptree` and look for
packages with a `No binaries` column.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--source-packages`](../cli/flet-build.md#-source-packages)
2. `[tool.flet.<PLATFORM>].source_packages`
3. `[tool.flet].source_packages`
4. `SERIOUS_PYTHON_ALLOW_SOURCE_DISTRIBUTIONS` (environment variable; comma-separated packages)

#### Example

/// tab | `flet build`
```bash
flet build <target_platform> --source-packages package1 package2
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet]
source_packages = ["package1", "package2"]
```
///
/// tab | `.env`
```dotenv
SERIOUS_PYTHON_ALLOW_SOURCE_DISTRIBUTIONS="package1,package2"
```
///

### Including Extensions

If your app uses Flet extensions (third-party packages),
they must equally be part of your app's dependencies.

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

Example of extensions can be found [here](../extend/built-in-extensions.md).

### Flutter dependencies

Adding a Flutter package can be done in the `pyproject.toml` as follows:

/// tab | `flet build`
```bash
flet build
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.flutter.dependencies]
package_1 = "x.y.z"

# or

[tool.flet.flutter.dependencies.<LOCAL_PACKAGE>]
path = "/path/to/LOCAL_PACKAGE"
```
///

### Icons

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
| Windows  | `icon_windows.ico` or `icon_windows.png` | 256×256 px       | `.png` file will be internally converted to a 256×256 px `.ico` icon.                       |
| macOS    | `icon_macos.png`                         | ≥ 1024×1024 px   |                                                                                             |


### Splash screen

A splash screen is a visual element displayed when an app is launching,
typically showing a logo or image while the app loads.

You can customize splash screens for iOS, Android, and Web platforms by
placing image files in the `assets` directory of your Flet app.

If platform-specific splash images are not provided, Flet will fall back to `splash.png`.
If that is also missing, it will use `icon.png` or any supported format such as `.bmp`, `.jpg`, or `.webp`.

#### Splash images

| Platform | Dark Fallback Order                                                                              | Light Fallback Order                             |
|----------|--------------------------------------------------------------------------------------------------|--------------------------------------------------|
| iOS      | `splash_dark_ios.png` → `splash_ios.png` → `splash_dark.png` → `splash.png` → `icon.png`         | `splash_ios.png` → `splash.png` → `icon.png`     |
| Android  | `splash_dark_android.png` → `splash_android.png` → `splash_dark.png` → `splash.png` → `icon.png` | `splash_android.png` → `splash.png` → `icon.png` |
| Web      | `splash_dark_web.png` → `splash_web.png` → `splash_dark.png` → `splash.png` → `icon.png`         | `splash_web.png` → `splash.png` → `icon.png`     |

#### Splash Background Colors

You can customize splash background colors using the following options:

- **Splash Color**: Background color for light mode splash screens.
- **Splash Dark Color**: Background color for dark mode splash screens.

##### Resolution order

Their values are respectively determined in the following order of precedence:

1. [`--splash-color`](../cli/flet-build.md#-splash-color) / [`--splash-dark-color`](../cli/flet-build.md#-splash-dark-color)
2. `[tool.flet.<PLATFORM>.splash].color` / `[tool.flet.<PLATFORM>.splash].dark_color`
3. `[tool.flet.splash].color` / `[tool.flet.splash].dark_color`
4. `#ffffff` / `#333333`

##### Example

/// tab | `flet build`
```
flet build <target_platform> --splash-color #ffffff --splash-dark-color #333333
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.splash]
color = "#ffffff"
dark_color = "#333333"
```
///

#### Disabling Splash Screens

Splash screens are enabled by default. To disable it for a particular platform,
see the corresponding documentation: [iOS](ios.md#disable-splash-screen),[Android](android.md#disable-splash-screen), and [Web](web/static-website/index.md#disable-splash-screen).

### Boot screen

The boot screen is shown while the archive with Python app is being unpacked to a
device file system. It is shown after the [splash screen](#splash-screen) and
before the [startup screen](#startup-screen). App archive does not include
3rd-party site packages. If the archive is small and its
unpacking is fast you could leave this screen disabled (default).

#### Example

/// tab | `pyproject.toml`
```toml
[tool.flet.app.boot_screen]     # or [tool.flet.<PLATFORM>.app.boot_screen]
show = false
message = "Preparing the app for its first launch…"
```
///

### Startup screen

The startup screen is shown while the archive (`app.zip`),
which contains the 3rd-party site packages (Android only),
is being unpacked and the Python app is starting.

It is shown after the [boot screen](#boot-screen).

#### Example

/// tab | `pyproject.toml`
```toml
[tool.flet.app.startup_screen]      # or [tool.flet.<PLATFORM>.app.startup_screen]
show = false
message = "Starting up the app…"
```
///

### Hidden app window on startup

A Flet desktop app (Windows, macOS, or Linux) can start with its window hidden.
This lets your app perform initial setup (for example, add content, resize or
position the window) before showing it to the user.

See this [code example](../controls/page.md#hidden-app-window-on-startup).

#### Example

/// tab | `pyproject.toml`
```toml
[tool.flet.app]
hide_window_on_start = true
```
///

### Permissions

`flet build` command allows granular control over permissions, features, and entitlements
embedded into `AndroidManifest.xml`, `Info.plist` and `.entitlements` files.

See platform guides for setting specific [iOS](ios.md), [Android](android.md) and [macOS](macos.md) permissions.

#### Cross-platform permissions

There are pre-defined permissions that mapped to `Info.plist`, `*.entitlements` and `AndroidManifest.xml`
for respective platforms.

Setting permissions can be done as follows:

/// tab | `flet build`
```bash
flet build <target_platform> --permissions camera microphone
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet]
permissions = ["camera", "microphone"]
```
///

Supported permissions:

* `location`
* `camera`
* `microphone`
* `photo_library`

##### iOS mapping to `Info.plist` entries

* `location`
    * `NSLocationWhenInUseUsageDescription = This app uses location service when in use.`
    * `NSLocationAlwaysAndWhenInUseUsageDescription = This app uses location service.`
* `camera`
    * `NSCameraUsageDescription = This app uses the camera to capture photos and videos.`
* `microphone`
    * `NSMicrophoneUsageDescription = This app uses microphone to record sounds.`
* `photo_library`
    * `NSPhotoLibraryUsageDescription = This app saves photos and videos to the photo library.`

##### macOS mapping to entitlements

* `location`
    * `com.apple.security.personal-information.location = True`
* `camera`
    * `com.apple.security.device.camera = True`
* `microphone`
    * `com.apple.security.device.audio-input = True`
* `photo_library`
    * `com.apple.security.personal-information.photos-library = True`

##### Android mappings

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

### Deep linking

[Deep linking](https://en.wikipedia.org/wiki/Mobile_deep_linking) allows users to navigate directly to specific content within a mobile app
using a URI (Uniform Resource Identifier). Instead of opening the app's homepage, deep
links direct users to a specific page, feature, or content within the app, enhancing
user experience and engagement.

- **Scheme**: deep linking URL scheme, e.g. `"https"` or `"myapp"`.
- **Host**: deep linking URL host.

See [this](https://docs.flutter.dev/ui/navigation/deep-linking) guide for more information.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--deep-linking-scheme`](../cli/flet-build.md#-deep-linking-scheme) / [`--deep-linking-host`](../cli/flet-build.md#-deep-linking-host)
2. `[tool.flet.<PLATFORM>.deep_linking].scheme` / `[tool.flet.<PLATFORM>.deep_linking].host`, where `<PLATFORM>` can be android or ios
3. `[tool.flet.deep_linking].scheme` / `[tool.flet.deep_linking].host`

#### Example

/// tab | `flet build`
```bash
flet build <target_platform> --deep-linking-scheme "https" --deep-linking-host "mydomain.com"
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.deep_linking]    # or [tool.flet.<PLATFORM>.deep_linking]
scheme = "https"
host = "mydomain.com"
```
///

### Target Architecture

A target platform can have different CPUs architectures,
which in turn support different instruction sets.

It is possible to build your app for specific CPU architectures.
This is useful for reducing the size of the resulting binary or package,
or for targeting specific devices.

For more/complementary information on supported architectures, see the specific platform guides:
[Android](android.md#split-apk-per-abi), [macOS](macos.md#target-architecture).

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--arch`](../cli/flet-build.md#-arch)
2. `[tool.flet.<PLATFORM>].target_arch`, where `<PLATFORM>` can be `android` or `macos`
3. `[tool.flet].target_arch`
4. All supported architectures for the `<target_platform>`

#### Example

/// tab | `flet build`
```bash
flet build macos --arch arm64 x86_64
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.macos]     # or [tool.flet]
target_arch = ["arm64", "x86_64"]
```
///

### Excluding files and directories

Files and/or directories can be excluded from the build process.
This can be useful for reducing the size of the resulting binary or package.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--exclude`](../cli/flet-build.md#-exclude) (can be used multiple times)
2. `[tool.flet.<PLATFORM>.app].exclude` (type: list of strings)
3. `[tool.flet.app].exclude` (type: list of strings)

The files and/or directories specified should be provided as relative
paths to the app root directory, `python_app_path`.

By default, the `build` directory is always excluded.
Additionally, when the target_platform is web, the `assets`
directory is always excluded.

#### Example

/// tab | `flet build`
```bash
flet build <target_platform> --exclude .git .venv
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.app]    # or [tool.flet.<PLATFORM>.app]
exclude = [".git", ".venv"]
```
///

### Compilation and cleanup

Flet can compile your app's `.py` files and/or installed packages' `.py` files into
`.pyc` files during the packaging process. Additionally, it can remove/cleanup
unnecessary package files upon successful compilation.

- Compilation:
    * `compile-app`: compile app's `.py` files
    * `compile-packages`: compile site/installed packages' `.py` files

- Cleanup:
    * `cleanup-app`:
    * `cleanup-app-files`:
    * `cleanup-packages-files`:
    * `cleanup-packages`: remove unnecessary package files upon successful compilation

By default, Flet does **not** compile your app files during packaging.
This allows the build process to complete even if there are syntax errors,
which can be useful for debugging or rapid iteration.

#### Resolution order

The values of `compile-app` and `cleanup-app` are respectively determined in the following order of precedence:

1. [`--compile-app`](../cli/flet-build.md#-compile-app) / [`--cleanup-app`](../cli/flet-build.md#-cleanup-app)
2. `[tool.flet.<PLATFORM>.compile].app` / `[tool.flet.<PLATFORM>.cleanup].app`
3. `[tool.flet.compile].app` / `[tool.flet.cleanup].app`
4. `False` / `False`

The values of `compile-packages` and `cleanup-packages` are respectively determined in the following order of precedence:

1. [`--compile-packages`](../cli/flet-build.md#-compile-packages) / [`--cleanup-packages`](../cli/flet-build.md#-cleanup-packages)
2. `[tool.flet.<PLATFORM>.compile].packages` / `[tool.flet.<PLATFORM>.cleanup].packages`
3. `[tool.flet.compile].packages` / `[tool.flet.cleanup].packages`
4. `False` / `True`

The values of `cleanup-app-files` and `cleanup-packages-files` are respectively determined in the following order of precedence:

1. [`--cleanup-app-files`](../cli/flet-build.md#-cleanup-app-files) / [`--cleanup-package-files`](../cli/flet-build.md#-cleanup-package-files)
2. `[tool.flet.<PLATFORM>.cleanup].app_files` / `[tool.flet.<PLATFORM>.cleanup].package_files`
3. `[tool.flet.cleanup].app_files` / `[tool.flet.cleanup].package_files`
4. `False` / `False`

#### Example

/// tab | `flet build`
```bash
flet build <target_platform> --compile-app --compile-packages --cleanup-packages
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.compile]     # or [tool.flet.<PLATFORM>.compile]
app = true
packages = true
cleanup = true
```
///

### Additional `flutter build` Arguments

During the `flet build` process, `flutter build` command gets called internally to
package your app for the specified platform. However, not all `flutter build`
arguments are exposed or usable through the `flet build` command directly.

For possible `flutter build` arguments, see [Flutter docs](https://docs.flutter.dev/deployment)
guide, or run `flutter build <target_platform> --help`.

/// admonition | Note
Passing additional `flutter build` arguments might cause unexpected behavior.
Use at your own risk, and only if you fully know what you're doing!
///

#### Resolution order

Its value is determined in the following order of precedence:

1. `--flutter-build-args` (can be used multiple times)
2. `[tool.flet.<PLATFORM>.flutter].build_args`
3. `[tool.flet.flutter].build_args`

#### Example

/// tab | `flet build`
```bash
flet build apk \
  --flutter-build-args=--obfuscate \
  --flutter-build-args=--export-method=development
  --flutter-build-args=--dart-define=API_URL=https://api.example.com
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.flutter]     # or [tool.flet.<PLATFORM>.flutter]
build_args = [
  "--obfuscate",
  "--export-method=development",
  "--dart-define=API_URL=https://api.example.com",
]
```
///

### Customizing build template

By default, `flet build` creates a temporary Flutter project using a
[cookiecutter](https://cookiecutter.readthedocs.io/en/stable/) template from the flet-dev/flet-build-template
repository. The version of the template used is determined by the [template reference](#template-reference)
option, which defaults to the current Flet version.

You can customize this behavior by specifying your own template
source, reference, and subdirectory.

#### Template Source

Defines the location of the cookiecutter build-template to be used.

Supported values include:

- A GitHub repository using the `gh:` prefix (e.g., `gh:org/template`)
- A full Git URL (e.g., `https://github.com/org/template.git`)
- A local directory path

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--template`](../cli/flet-build.md#-template) (can be used multiple times)
2. `[tool.flet.template].url`
3. [`"gh:flet-dev/flet-build-template"`](https://github.com/flet-dev/flet-build-template)

#### Example

/// tab | `flet build`
```bash
flet build apk --template gh:flet-dev/flet-build-template
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.template]
url = "gh:flet-dev/flet-build-template"
```
///

#### Template Reference

Defines the branch, tag, or commit to check out from the [template source](#template-source).

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--template-ref`](../cli/flet-build.md#-template-ref) (can be used multiple times)
2. `[tool.flet.template].ref`
3. [`<flet_version>`](#configuration-options)

#### Example

/// tab | `flet build`
```bash
flet build <target_platform> --template-ref main
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.template]
ref = "main"
```
///

#### Template Directory

Defines the relative path to the cookiecutter template.
If [template source](#template-source) is set, the path is treated as a
subdirectory within its root; otherwise, it is relative to
`<user-directory>/.cookiecutters/flet-build-template`.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--template-dir`](../cli/flet-build.md#-template-dir) (can be used multiple times)
2. `[tool.flet.template].dir`
3. root of the [template source](#template-source)

#### Example

/// tab | `flet build`
```bash
flet build <target_platform> --template gh:org/template --template-dir sub/directory
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.template]
url = "gh:org/template"
dir = "sub/directory"
```
///

### Verbose logging

The [`-v`](../cli/flet-build.md/#-verbose) (or `--verbose`) and `-vv` flags
enables detailed output from all commands during the flet build process.

Use `-v` for standard/basic verbose logging, or `-vv` for even more detailed
output (higher verbosity level). If you need support,
we may ask you to share this verbose log.

## Console output

All output from Flet apps—such as `print()` statements, `sys.stdout.write()` calls, and messages from the Python
logging module is redirected to a `console.log` file. The full path to this file is available via
[`StoragePaths.get_console_log_filename()`][flet.StoragePaths.get_console_log_filename] or the
`FLET_APP_CONSOLE` environment variable.

The log file is written in an unbuffered manner, allowing you to read it at any point in your Python program using:

```python
import os
import flet as ft

async def main(page: ft.Page):
    log_file = await ft.StoragePaths().get_console_log_filename()
    # or
    # log_file = os.getenv("FLET_APP_CONSOLE")

    with open(log_file, "r") as f:
        logs = f.read()
        page.add(ft.Text(logs)) # display on UI

ft.run(main)
```

If your program calls `sys.exit(100)`, the complete log will automatically be shown in a scrollable window.
This is a special “magic” exit code for debugging purposes:

```python
import sys
sys.exit(100)
```

Calling `sys.exit()` with any other code will terminate the app without displaying the log.

## Continuous Integration/Continuous Deployment (CI/CD)

You can use `flet build` command in your CI/CD pipelines to automate the build and release process of your Flet apps.

### GitHub Actions

TBA
