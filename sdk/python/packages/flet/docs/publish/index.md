# Publishing a Flet app

Flet CLI provides the [`flet build`](../cli/flet-build.md) command to package a
Flet app into a standalone executable or installable package for distribution.

## Prerequisites

### Platform matrix

Use the following matrix to choose which OS to run `flet build`
on for each target platform:

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
      <th style="text-align: center;"><a href="ios.md">ipa/ios-simulator</a></th>
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

/// admonition | Tip
    type: tip
The recommended (minimum required) Flutter SDK version
depends on the Flet version installed or in use.

It can be viewed by running one of the following commands:

```bash
flet --version
```
```bash
uv run python -c "import flet.version; print(flet.version.flutter_version)"
```

or the below Python code snippet:

```python
import flet.version
print(flet.version.flutter_version)
```
///

## Project structure

The `flet build` command assumes the following minimal Flet project structure:

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
Instead of a `pyproject.toml` file, you can also use a `requirements.txt` file to specify dependencies.

In this case, two things to keep in mind:

- if both files are present, `flet build` will ignore `requirements.txt`.
- don't use `pip freeze > requirements.txt` to generate this file or fill it with dependencies,
  as it may include packages incompatible with the target platform. Instead, hand-pick and include
  only the direct dependencies required by your app, including `flet`.
///

## How it works

When you run `flet build <target_platform>`, the pipeline is:

1. Create a Flutter project in `{flet_app_directory}/build/flutter` from the [template](#template-source).
   The Flutter app embeds your packaged Python app in its assets and uses `flet` and
   [`serious_python`](https://pub.dev/packages/serious_python) to run the app and render the UI.
   The project is cached and reused across builds for rapid iterations;
   use [`--clear-cache`](../cli/flet-build.md#-clear-cache) to force a rebuild.
2. Copy custom [icons](#icons) and [splash images](#splash-screen) from `assets` into the
   Flutter project, then generate:
     - Icons for all platforms via [`flutter_launcher_icons`](https://pub.dev/packages/flutter_launcher_icons).
     - Splash screens for web, iOS, and Android via [`flutter_native_splash`](https://pub.dev/packages/flutter_native_splash).
3. Package the Python app using `serious_python package`:
      - Install app dependencies from [pypi.org](https://pypi.org) and
         [pypi.flet.dev](https://pypi.flet.dev) for the selected platform, as configured in
         [App dependencies](#app-dependencies) and [Source packages](#source-packages).
     - If [configured](#compilation-and-cleanup), compile `.py` files to `.pyc`.
     - Add all project files, except those [excluded](#excluding-files-and-directories), to the app asset.
4. Run [`flutter build`](https://docs.flutter.dev/deployment) to produce the
   executable or installable package.
5. Copy build outputs from Step 4 into the [output directory](#output-directory).

## Configuration options

/// admonition | Placeholders
Throughout this documentation, the following placeholders are used:

- [`<target_platform>`](../cli/flet-build.md#target_platform) - one of: `apk`, `aab`, `ipa`, `ios-simulator`, `web`, `macos`, `windows`, `linux`.
- `<PLATFORM>` - the config namespace under `[tool.flet.<PLATFORM>]`; one of: `android` (for `apk` and `aab` targets), `ios` (for `ipa` and `ios-simulator` targets), `web`, `macos`, `windows`, `linux`.
- [`<python_app_path>`](../cli/flet-build.md#python_app_path) - the path passed to `flet build` (defaults to the current directory).
- `<flet_app_directory>` - the resolved project root for `<python_app_path>`; `pyproject.toml` and `requirements.txt` are read from here.
- `<flet_version>` - the version of Flet in use. You can check with `flet --version` or
  `uv run python -c "import flet; print(flet.__version__)"`.
///

/// admonition | Understanding `pyproject.toml` structure
Flet loads `pyproject.toml` as a nested dictionary and looks up settings using
dot-separated paths (for example, `tool.flet.web.base_url`).

The two forms below are equivalent and resolve to the same key-value pair:

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

### App path

Defines the root directory of your Python app within `<python_app_path>`.
Flet looks for the [entry point](#entry-point), the `assets` directory, and
[exclude paths](#excluding-files-and-directories) relative to this directory.

#### Resolution order

Its value is determined in the following order of precedence:

1. `[tool.flet.app].path`
2. `<python_app_path>`

`path` is resolved relative to `<python_app_path>`.

#### Example

/// tab | `pyproject.toml`
```toml
[tool.flet.app]
path = "src"
```
///

### Entry point

This is the Python module that starts your app and contains the call to
`flet.run()` or `flet.render()`. Flet uses the module *stem* and looks for
`<module>.py` in your [app path](#app-path).

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--module-name`](../cli/flet-build.md#-module-name)
2. `[tool.flet.app].module`
3. `"main"` (entry file `main.py`)

Its value can either be `<module>` or `<module>.py`; both resolve to the same Python module.

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

The project name is the base identifier for [bundle IDs](#bundle-id) and other internal
names. The source value is normalized to a safe identifier: lowercased, punctuation
and spaces removed or collapsed, and hyphens converted to underscores (for example,
`My App` or `my-app` becomes `my_app`).

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

It does **not** control the on-disk executable or bundle name. Use the
[artifact name](#artifact-name) for artifact naming.

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

It can contain spaces or accents, but keep file system restrictions in mind on
your target platforms.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--artifact`](../cli/flet-build.md#-artifact)
2. `[tool.flet.<PLATFORM>].artifact`
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

/// admonition | Note
[Android](android.md), [iOS](ios.md),
[macOS](macos.md), and [Linux](linux.md) only.
///

The organization name in reverse domain name notation, typically in the form
`com.mycompany`. It is used as the prefix for the [bundle ID](#bundle-id) and
for package identifiers on mobile and desktop targets.

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

/// admonition | Note
[Android](android.md), [iOS](ios.md),
[macOS](macos.md), and [Linux](linux.md) only.
///

The bundle ID for the application, typically in the form `"com.mycompany.my_app"`.

If not explicitly specified, it is derived from the [organization name](#organization-name)
and the [project name](#project-name) used by the build template.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--bundle-id`](../cli/flet-build.md#-bundle-id)
2. `[tool.flet.<PLATFORM>].bundle_id`
3. `[tool.flet].bundle_id`

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

/// admonition | Note
[Windows](windows.md) and [macOS](macos.md) only.
///

The company name displayed in about app dialogs and metadata (notably on desktop builds).

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--company`](../cli/flet-build.md#-company)
2. `[tool.flet].company`
3. Build template default (see [Template Source](#template-source))

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

/// admonition | Note
[Windows](windows.md) and [macOS](macos.md) only.
///

Copyright text displayed in about app dialogs and metadata.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--copyright`](../cli/flet-build.md#-copyright)
2. `[tool.flet].copyright`
3. Build template default (see [Template Source](#template-source))

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

An integer identifier used internally to distinguish one build from another.

Each new build must have a unique, incrementing number;
higher numbers indicate more recent builds.

##### Resolution order

Its value is determined in the following order of precedence:

1. [`--build-number`](../cli/flet-build.md#-build-number)
2. `[tool.flet].build_number`
3. Otherwise, the build number from the generated `pubspec.yaml`
   (see [Template Source](#template-source)) will be used.

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

A user‑facing version string in `x.y.z` format.
Increment this for each new release to differentiate it from previous versions.

##### Resolution order

Its value is determined in the following order of precedence:

1. `--build-version`
2. `[project].version`
3. `[tool.poetry].version`
4. Otherwise, the build version from the generated `pubspec.yaml`
   (see [Template Source](#template-source)) will be used.

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
If the directory already exists, it is deleted and recreated on each build.

For web builds, the app's `assets` directory is copied into the output directory.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--output`](../cli/flet-build.md#-output) (or `-o`)
2. `<python_app_path>/build/<target_platform>`

#### Example

/// tab | `flet build`
```bash
flet build <target_platform> --output <path-to-output-dir>
```
///

### App dependencies

These are the Python packages that your Flet app depends on to function correctly.

#### Resolution order

Its value is determined in the following order of precedence:

- `[tool.poetry].dependencies` if present; otherwise `[project].dependencies` (PEP 621).
- If `[tool.flet.<PLATFORM>].dependencies` is set (where `<PLATFORM>` corresponds to `<target_platform>`), its values are appended to the list above.
- If the result of all above is empty and `requirements.txt` exists in `<python_app_path>`, it is used.
- If the result of all the above is empty, `flet==<flet_version>` is used.

To use a local development version of a dependency during builds, configure
`[tool.flet].dev_packages` or `[tool.flet.<PLATFORM>].dev_packages` with a
package name to path mapping.

If your app uses Flet extensions (third-party packages), list them in your
Python dependencies so they are packaged with the app. Examples of extensions
can be found in [Built-in extensions](../extend/built-in-extensions.md).

#### Example

/// tab | `pyproject.toml`
```toml
[project]
dependencies = [
    "flet",
    "requests",
    "flet-extension1",
    "flet-extension2 @ git+https://github.com/account/flet-extension2.git",   # git repo
    "flet-extension3 @ file:///path/to/flet-extension3",  # local package
]

[tool.flet.<PLATFORM>]  # will be used/appended only if <PLATFORM> corresponds to <target_platform>
dependencies = [
    "dep1",
    "dep2",
]
```
///

### Source packages

/// admonition | Note
[Android](android.md) and [iOS](ios.md) only.
///

By default, packaging for mobile and web only installs binary wheels. Use source packages
to allow specific dependencies to be installed from [source distributions (sdists)](https://pydevtools.com/handbook/reference/sdist/).

This can be useful for installing - pure Python - dependencies that do not have pre-built wheels for the
target mobile platform or an all-platform wheel (`*-py3-none-any.whl`), but instead provide a source distribution (`*.tar.gz`).

For more information on pure vs non-pure Python packages, see our
[blog post](https://flet.dev/blog/flet-packaging-update#pure-python-packages) on the topic.

On desktop targets, source installs are already allowed, so this setting is mainly/only for
[Android](android.md) and [iOS](ios.md) builds.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--source-packages`](../cli/flet-build.md#-source-packages)
2. `[tool.flet.<PLATFORM>].source_packages`
3. `[tool.flet].source_packages`

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

### Icons

/// admonition | Note
[Android](android.md), [iOS](ios.md), [macOS](macos.md), [Windows](windows.md)
and [Web](web/static-website/index.md#flet-build-web) only.
///

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

/// admonition | Note
[Android](android.md), [iOS](ios.md),
and [Web](web/static-website/index.md#flet-build-web) only.
///

A splash screen is a visual element displayed when an app is launching,
typically showing a logo or image while the app loads.

You can customize splash screens for iOS, Android, and Web platforms by
placing image files in the `assets` directory of your Flet app.

If platform-specific splash images are not provided, Flet will fall back to `splash.png`.
If that is also missing, it will use `icon.png` or any supported format such as `.bmp`, `.jpg`, or `.webp`.

#### Splash images

| Platform | Dark Fallback Order                                                                              | Light Fallback Order                             |
|----------|--------------------------------------------------------------------------------------------------|--------------------------------------------------|
| iOS      | `splash_dark_ios.png` → `splash_dark.png` → `splash_ios.png` → `splash.png` → `icon.png`         | `splash_ios.png` → `splash.png` → `icon.png`     |
| Android  | `splash_dark_android.png` → `splash_dark.png` → `splash_android.png` → `splash.png` → `icon.png` | `splash_android.png` → `splash.png` → `icon.png` |
| Web      | `splash_dark_web.png` → `splash_dark.png` → `splash_web.png` → `splash.png` → `icon.png`         | `splash_web.png` → `splash.png` → `icon.png`     |

#### Splash Background Colors

You can customize splash background colors using the following options:

- **Splash Color**: Background color for light mode splash screens.
- **Splash Dark Color**: Background color for dark mode splash screens.

##### Resolution order

Their values are respectively determined in the following order of precedence:

1. [`--splash-color`](../cli/flet-build.md#-splash-color) / [`--splash-dark-color`](../cli/flet-build.md#-splash-dark-color)
2. `[tool.flet.<PLATFORM>.splash].color` / `[tool.flet.<PLATFORM>.splash].dark_color`
3. `[tool.flet.splash].color` / `[tool.flet.splash].dark_color`
4. [Build template](#build-template) defaults

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

Splash screens are enabled by default but can be disabled.

##### Resolution order

Its value is determined in the following order of precedence:

- on Android:
    - [`--no-android-splash`](../cli/flet-build.md#-no-android-splash)
    - `[tool.flet.splash].android`
- on iOS:
    - [`--no-ios-splash`](../cli/flet-build.md#-no-ios-splash)
    - `[tool.flet.splash].ios`
- on Web:
    - [`--no-web-splash`](../cli/flet-build.md#-no-web-splash)
    - `[tool.flet.splash].web`

##### Example

/// tab | `flet build`
```bash
flet build apk --no-android-splash
flet build ipa --no-ios-splash
flet build ios-simulator --no-ios-splash
flet build web --no-web-splash
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.splash]
android = false
ios = false
web = false
```
///

### Boot screen

/// admonition | Note
[Windows](windows.md), [macOS](macos.md), [Linux](linux.md),
[Android](android.md), and [iOS](ios.md) only.
///

The boot screen is shown while the packaged app archive (`app.zip`) is extracted
to the app data directory (typically on first launch or after the app bundle changes).
It appears after the [splash screen](#splash-screen) and before the
[startup screen](#startup-screen).

It is not shown by default. Enable it, for example, when then extraction time is noticeable.

#### Example

/// tab | `pyproject.toml`
```toml
[tool.flet.app.boot_screen]     # or [tool.flet.<PLATFORM>.app.boot_screen]
show = true
message = "Preparing the app for its first launch…"
```
///

### Startup screen

/// admonition | Note
[Windows](windows.md), [macOS](macos.md), [Linux](linux.md),
[Android](android.md), and [iOS](ios.md) only.
///

The startup screen is shown while the Python runtime and your app are starting.
On mobile targets this can include preparing packaged dependencies. It appears
after the [boot screen](#boot-screen).

It is not shown by default.

#### Example

/// tab | `pyproject.toml`
```toml
[tool.flet.app.startup_screen]      # or [tool.flet.<PLATFORM>.app.startup_screen]
show = true
message = "Starting up the app…"
```
///

### Hidden app window on startup

/// admonition | Note
[Windows](windows.md), [macOS](macos.md), and [Linux](linux.md) only.
///

A Flet desktop app (Windows, macOS, or Linux) can start with its window hidden.
This lets your app perform initial setup (for example, add content, resize or
position the window) before showing it to the user.

See this [code example](../controls/page.md#hidden-app-window-on-startup).

#### Resolution order

Its value is determined in the following order of precedence:

- `[tool.flet.<PLATFORM>.app].hide_window_on_start`, where `<PLATFORM>` can be `windows`, `macos` or `linux`
- `[tool.flet.app].hide_window_on_start`
- [`FLET_HIDE_WINDOW_ON_START`](../reference/environment-variables.md#flet_hide_window_on_start)

#### Example

/// tab | `pyproject.toml`
```toml
[tool.flet.app]    # or [tool.flet.<PLATFORM>.app]
hide_window_on_start = true
```
///

### Deep linking

/// admonition | Note
[Android](android.md) and [iOS](ios.md) only.
///

[Deep linking](https://en.wikipedia.org/wiki/Mobile_deep_linking) allows users
to navigate directly to specific content within a mobile app
using a [URI (Uniform Resource Identifier)](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier).
Instead of opening the app's homepage, deep links direct users to a specific page,
feature, or content within the app, enhancing user experience and engagement.

- **Scheme**: deep linking URL scheme, e.g. `"https"` or `"myapp"`.
- **Host**: deep linking URL host.

See [this](https://docs.flutter.dev/ui/navigation/deep-linking) guide for more information.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--deep-linking-scheme`](../cli/flet-build.md#-deep-linking-scheme) and
   [`--deep-linking-host`](../cli/flet-build.md#-deep-linking-host) (only when both are provided)
2. `[tool.flet.<PLATFORM>.deep_linking].scheme` / `[tool.flet.<PLATFORM>.deep_linking].host`, where `<PLATFORM>` can be android or ios
3. `[tool.flet.deep_linking].scheme` / `[tool.flet.deep_linking].host`

Both scheme and host are required; if either is missing, the deep-linking entries are not added.

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

/// admonition | Note
For [Android](android.md) and [macOS](macos.md) only.
///

A target platform can have different CPU architectures,
which in turn support different instruction sets.

It is possible to build your app for specific CPU architectures.
This is useful for reducing the size of the resulting binary or package,
or for targeting specific devices.

For more/complementary information, see the specific platform guides:
[Android](android.md#supported-target-architectures), [macOS](macos.md#target-architecture).

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--arch`](../cli/flet-build.md#-arch)
2. `[tool.flet.<PLATFORM>].target_arch`, where `<PLATFORM>` can be `android` or `macos`
3. `[tool.flet].target_arch`
4. Platform defaults for the `<target_platform>`

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
paths to the [app path](#app-path) directory. Paths are matched exactly (no globs), and
directories are excluded recursively.

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
`.pyc` files during the packaging process (via `python -m compileall -b`). Cleanup
removes known junk files and any additional globs you specify.

1. Compilation:
    * `compile-app`: compile app's `.py` files
    * `compile-packages`: compile site/installed packages' `.py` files

2. Cleanup:
    * `cleanup-app`: remove junk files from the app directory
    * `cleanup-app-files`: additional globs to delete from the app directory
      (implies `cleanup-app`)
    * `cleanup-package-files`: additional globs to delete from site-packages
      (implies `cleanup-packages`)
    * `cleanup-packages`: remove junk files from site-packages (defaults to `true`)

`[tool.flet.compile].cleanup` (deprecated) enables both `cleanup-app` and
`cleanup-packages` when set to `true`.

By default, Flet does **not** compile your app files during packaging.
This allows the build process to complete even if there are syntax errors,
which can be useful for debugging or rapid iteration.

#### Resolution order

The values of `compile-app` and `cleanup-app` are respectively determined in the following order of precedence:

1. [`--compile-app`](../cli/flet-build.md#-compile-app) / [`--cleanup-app`](../cli/flet-build.md#-cleanup-app)
2. `[tool.flet.<PLATFORM>.compile].app` / `[tool.flet.<PLATFORM>.cleanup].app`
3. `[tool.flet.compile].app` / `[tool.flet.cleanup].app`
4. empty list / empty list

The values of `compile-packages` and `cleanup-packages` are respectively determined in the following order of precedence:

1. [`--compile-packages`](../cli/flet-build.md#-compile-packages) / [`--cleanup-packages`](../cli/flet-build.md#-cleanup-packages)
2. `[tool.flet.<PLATFORM>.compile].packages` / `[tool.flet.<PLATFORM>.cleanup].packages`
3. `[tool.flet.compile].packages` / `[tool.flet.cleanup].packages`
4. `False` / `True`

The values of `cleanup-app-files` and `cleanup-package-files` are respectively determined in the following order of precedence:

1. [`--cleanup-app-files`](../cli/flet-build.md#-cleanup-app-files) / [`--cleanup-package-files`](../cli/flet-build.md#-cleanup-package-files)
2. `[tool.flet.<PLATFORM>.cleanup].app_files` / `[tool.flet.<PLATFORM>.cleanup].package_files`
3. `[tool.flet.cleanup].app_files` / `[tool.flet.cleanup].package_files`
4. `False` / `False`

#### Example

/// tab | `flet build`
```bash
flet build <target_platform> --compile-app --compile-packages --cleanup-app-files "**/*.c" "**/*.h" --cleanup-package-files "**/*.pyi"
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.compile]     # or [tool.flet.<PLATFORM>.compile]
app = true
packages = true

[tool.flet.cleanup]     # or [tool.flet.<PLATFORM>.cleanup]
app = true
packages = true
app_files = ["**/*.c", "**/*.h"]
package_files = ["**/*.pyi"]
```
///

### Permissions

/// admonition | Note
[Android](android.md), [iOS](ios.md), and [macOS](macos.md) only.
///

`flet build` allows granular control over permissions, features, and entitlements
embedded into `AndroidManifest.xml`, `Info.plist` and `.entitlements` files.

See platform guides for setting specific [iOS](ios.md#permissions),
[Android](android.md#permissions) and [macOS](macos.md) permissions.

#### Predefined cross-platform permission bundles

Cross-platform permissions are named and predefined bundles that apply a baseline set of
platform-specific entries required for a feature. Each bundle expands into the
corresponding platform-specific equivalents. This is especially useful for beginners
who may be unfamiliar with the underlying platform APIs or prefer not to interact with them directly.

Only the bundles you list are applied. If you need different wording or extra
entries, set the platform-specific tables directly; those values are merged on top and
can override the bundle defaults. The examples below show the exact `pyproject.toml` equivalents for each bundle.

Below is a list of available bundles:

{{ cross_platform_permissions() }}

##### Resolution order

Its value is determined in the following order of precedence:

1. [`--permissions`](../cli/flet-build.md#-permissions)
2. `[tool.flet].permissions` (type: list of strings)
3. `[]`

##### Example

/// tab | `flet build`
```bash
flet build <target_platform> --permissions location microphone
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet]
permissions = ["location", "microphone"]
```
///

### Build template

`flet build` creates (and reuses) a Flutter project under `<app_root>/build/flutter` using a
[cookiecutter](https://cookiecutter.readthedocs.io/en/stable/) template from the flet-dev/flet-build-template
repository. The version of the template used is determined by the
[template reference](#template-reference) option.

The cached project is refreshed when template inputs change or when you pass
[`--clear-cache`](../cli/flet-build.md#-clear-cache).

#### Template Source

Defines the location of the cookiecutter build-template to be used.

Supported values include:

- A GitHub repository using the `gh:` prefix (e.g., `gh:org/template`)
- A full Git URL (e.g., `https://github.com/org/template.git`)
- A local directory path

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--template`](../cli/flet-build.md#-template)
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

1. [`--template-ref`](../cli/flet-build.md#-template-ref)
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
subdirectory within its root; otherwise, it is relative to the template root.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--template-dir`](../cli/flet-build.md#-template-dir)
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

### Additional `flutter build` Arguments

During the `flet build` process, `flutter build` command gets called internally to
package your app for the specified platform. However, not all `flutter build`
arguments are exposed or usable through the `flet build` command directly.

For possible `flutter build` arguments, see [Flutter docs](https://docs.flutter.dev/deployment)
guide. For most targets, run `flutter build <target_platform> --help`; for
[`ios-simulator`](ios.md#flet-build-ios-simulator), run `flutter build ios --simulator --help`.

/// admonition | Important
    type: warning
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
  --flutter-build-args=--export-method=development \
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

### Flutter dependencies

When you run `flet build`, Flet generates a Flutter shell project and then
updates its [`pubspec.yaml`](#build-template) using values from `pyproject.toml`.

Use:

- `[tool.flet.flutter.pubspec.dependencies]` for normal package declarations.
    ([Dart docs](https://dart.dev/tools/pub/dependencies))
- `[tool.flet.flutter.pubspec.dependency_overrides]` when you must force a
    version or source, for example, a local path or Git fork.
    ([Dart docs](https://dart.dev/tools/pub/dependencies#dependency-overrides))

Values follow [standard Pub dependency syntax](https://dart.dev/tools/pub/dependencies#dependency-sources),
expressed in TOML.

/// admonition | Note
- **Important:** In most cases, you usually do not need to add/override Flutter dependencies.
  We recommend doing it only if you fully know what you are doing, as it can lead to
  unexpected behavior.
- If the same package appears in both `pyproject.toml` and the resulting `pubspec.yaml`,
  the value from `pyproject.toml` wins.
- If you use `{ path = "..." }` under `[tool.flet.flutter.pubspec.dependencies]`
  or `[tool.flet.flutter.pubspec.dependency_overrides]`, that path is resolved by
  Flutter from the generated `pubspec.yaml` location: `<flet_app_directory>/build/flutter/pubspec.yaml`.
  This means relative paths are **not** resolved from your `pyproject.toml` file.
///

#### Example

/// tab | `pyproject.toml`
```toml
[tool.flet.flutter.pubspec.dependencies]    # or [tool.flet.flutter.pubspec.dependency_overrides]
# Version
pkg_1 = "^1.2.3"

# Local path
pkg_2 = { path = "../pkg_2" }

# Git (short form)
pkg_3 = { git = "https://github.com/org/pkg_3.git" }

# Git (expanded form: URL + ref + subdirectory)
pkg_4 = { git = { url = "https://github.com/org/mono_repo.git", ref = "main", path = "packages/pkg_4" } }

# Hosted source
pkg_5 = { hosted = { name = "pkg_5", url = "https://pub.dev" }, version = "^1.0.0" }

# SDK package (dependencies only; typically not used in dependency_overrides)
flutter_test = { sdk = "flutter" }
```
///

### Verbose logging

The [`-v`](../cli/flet-build.md#-verbose) (or `--verbose`) and `-vv` flags
enable detailed output from all commands during the flet build process.

Use `-v` for standard/basic verbose logging, or `-vv` for even more detailed
output (higher verbosity level). If you need support,
we may ask you to share this verbose log.

## Console output

In packaged apps (`flet build` output), all output from your Python code such as
`print()` statements, `sys.stdout.write()` calls, and messages from the Python
`logging` module is redirected to a `console.log` file. The full path to this file is available via
[`StoragePaths.get_console_log_filename()`][flet.StoragePaths.get_console_log_filename] or the
`FLET_APP_CONSOLE` environment variable.

Note: `FLET_APP_CONSOLE` is only set in production builds;
in development runs, output stays in your terminal.

The log file is written in an unbuffered manner, allowing you to read
it at any point in your Python program using:

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
This is a special "magic" exit code for debugging purposes:

```python
import sys
sys.exit(100)
```

Calling `sys.exit()` with any other code will terminate the app without displaying the log.

## Continuous Integration/Continuous Deployment (CI/CD)

You can use `flet build` command in your CI/CD pipelines to automate
the build and release process of your Flet apps.

### GitHub Actions

You can use [GitHub Actions](https://docs.github.com/en/actions) to build your
Flet app automatically on every push, pull request, or manual run.

{% raw %}
```yaml
name: Build Flet App # (1)!

on: # (2)!
  push: # (3)!
  pull_request: # (4)!
  workflow_dispatch: # (5)!

env: # (6)!
  UV_PYTHON: 3.12 # (7)!
  PYTHONUTF8: 1 # (8)!

  # https://docs.flet.dev/reference/environment-variables
  FLET_CLI_NO_RICH_OUTPUT: 1 # (9)!

jobs:
  build:
    name: Build ${{ matrix.name }}
    runs-on: ${{ matrix.runner }}
    strategy: # (10)!
      fail-fast: false
      matrix:
        include:
          # -------- Desktop --------
          - name: linux
            runner: ubuntu-latest
            build_cmd: "flet build linux"
            artifact_path: build/linux
            needs_linux_deps: true

          - name: macos
            runner: macos-latest
            build_cmd: "flet build macos"
            artifact_path: build/macos
            needs_linux_deps: false

          - name: windows
            runner: windows-latest
            build_cmd: "flet build windows"
            artifact_path: build/windows
            needs_linux_deps: false

          # -------- Android --------
          - name: aab
            runner: ubuntu-latest
            build_cmd: "flet build aab"
            artifact_path: build/aab
            needs_linux_deps: false

          - name: apk
            runner: ubuntu-latest
            build_cmd: "flet build apk"
            artifact_path: build/apk
            needs_linux_deps: false

          # -------- iOS --------
          - name: ipa
            runner: macos-latest
            build_cmd: "flet build ipa"
            artifact_path: build/ipa
            needs_linux_deps: false

          - name: ios-simulator
            runner: macos-latest
            build_cmd: "flet build ios-simulator"
            artifact_path: build/ios-simulator
            needs_linux_deps: false

          # -------- Web --------
          - name: web
            runner: ubuntu-latest
            build_cmd: "flet build web"
            artifact_path: build/web
            needs_linux_deps: false

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4 # (11)!

      - name: Setup uv
        uses: astral-sh/setup-uv@v6 # (12)!

      - name: Install Linux dependencies # (13)!
        if: matrix.needs_linux_deps # (14)!
        shell: bash
        run: |
            sudo apt update --allow-releaseinfo-change
            sudo apt-get install -y --no-install-recommends \
              clang ninja-build libgtk-3-dev libasound2-dev libmpv-dev mpv \
              libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev \
              gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
              gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 \
              gstreamer1.0-qt5 gstreamer1.0-pulseaudio pkg-config libsecret-1-0 libsecret-1-dev
            sudo apt-get clean

      - name: Build app # (15)!
        shell: bash
        run: |
          uv run ${{ matrix.build_cmd }} --yes --verbose

      - name: Upload Artifact
        uses: actions/upload-artifact@v5.0.0 # (16)!
        with:
          name: ${{ matrix.name }}-build-artifact
          path: ${{ matrix.artifact_path }} # (17)!
          if-no-files-found: error # (18)!
          overwrite: false
```
{% endraw %}

1. Workflow display name shown in the **Actions** tab.
2. Trigger block for automatic and manual workflow runs.
3. Runs this workflow on every push (unless you restrict branches).
4. Runs this workflow when pull requests are opened/updated.
5. Enables manual runs from GitHub UI (**Actions** → **Run workflow**).
6. Environment variables shared by all jobs and steps.
7. Python version used by `uv`.
8. Forces UTF-8 mode for Python output/IO. Especially useful on Windows builds.
9. Disables rich output from `flet build` for better readability in CI logs.
10. Matrix strategy: each `include` item becomes a parallel build job.
11. Checks out your repository so this workflow can access project files. View its docs [here](https://github.com/actions/checkout).
12. Installs `uv` on the runner. View its docs [here](https://github.com/astral-sh/setup-uv).
13. Installs Linux system packages required by Linux desktop builds.
14. Runs Linux package installation only for matrix entries that need it.
15. Main build step for each target. Executes the target-specific command defined by `matrix.build_cmd`.
16. Uploads build output files as downloadable artifacts. View its docs [here](https://github.com/actions/upload-artifact).
17. Artifact path expected from each build target.
18. If no files were found to upload, the workflow fails, indicating something went wrong during the build.

The workflow file above builds for all major targets and uploads each build output as an artifact.
You can further customize the workflow for your specific needs, for example,
restricting the build targets or adding additional steps.

See it in action [here](https://github.com/ndonkoHenri/flet-github-action-workflows).

## Troubleshooting

### Prerelease compatibility

If you are using a prerelease version of the [Flet Python package](https://pypi.org/project/flet) (for example, `0.80.6.devNNNN`) to build an app,
the [build template](#build-template) may still resolve the latest **stable** [`flet` Flutter package](https://pub.dev/packages/flet), which can lead to version incompatibility issues.

**Why?**: Under normal circumstances, each prerelease of the Flet Python package would require
a matching prerelease of the Flutter Flet package to guarantee compatibility.
However, we don't publish prerelease versions of the Flutter package to [pub.dev](https://pub.dev/).
Because of this, the build template resolves the latest **stable** Flutter `flet` release instead.

This creates a version mismatch/incompatibility for apps packaged with `flet build`:

* Your Python code may depend on newly introduced controls or features.
* The packaged Flutter shell may still be using an older stable `flet` version.
* At runtime, the app fails because the Flutter layer does not recognize the new controls/features in your prerelease `flet` package, leading to errors like `Unknown control: <ControlName>`.

**Note**: this issue does not affect the development workflows (ex: running an app with [`flet run`](../getting-started#running-app)),
as the `flet` Flutter dependency is only resolved during the `flet build` process.

### Solution

The rule-of-thumb is, if you are using a prerelease Flet Python package, always ensure the Flutter `flet`
dependency is aligned with the same development version before building your app:

1. Override the Flutter `flet` dependency to point to the corresponding development Git reference.

    /// tab | `pyproject.toml`
    ```toml
    [tool.flet.flutter.pubspec.dependency_overrides]
    flet = { git = { url = "https://github.com/flet-dev/flet.git", ref = "main", path = "packages/flet" } }
    ```
    ///

2. Rebuild the app with the build cache cleared (use [`--clear-cache`](../cli/flet-build.md#-clear-cache); or manually delete `build/flutter`)

To ensure reproducible builds (ex: in production or CI), prefer using a specific commit SHA, instead of a branch or tag ref.
