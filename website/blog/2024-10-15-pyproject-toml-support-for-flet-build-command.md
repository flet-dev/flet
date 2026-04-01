---
slug: pyproject-toml-support-for-flet-build-command
title: pyproject.toml support for flet build command
authors: feodor
---

The number of options for `flet build` command grew substantially over the time and it's been inconvenient to carry all these settings in a command line.

Today, we are excited to announce another Flet pre-release which now allows configuring app build settings in `pyproject.toml`!

<!-- truncate -->

## Installing pre-release

```
pip install flet==0.25.0.dev3526
```

:::note
For testing purposes we suggest installing Flet pre-release in a dedicated Python virtual environment.
:::

## Building the app with pre-release

To build your app with `flet build` command and pre-release version of Flet make sure your `requirements.txt` either contains exact version specifier:

```
flet==0.25.0.dev3526
```

or `--pre` flag before `flet` dependency:

```
--pre
flet
```

## Quick start

Create the following minimal `pyproject.toml` file in the root of your Flet app or run `flet create` to create a new app from template:

```toml
[project]
name = "my_app"
version = "1.0.0"
description = "My first Flet project"
authors = [
  {name = "John Smith", email = "john@email.com"}
]
dependencies = ["flet==0.25.0.dev3526"]
```

:::note
With `pyproject.toml`, you no longer need `requirements.txt`. However, if a `requirements.txt` file exists in the app's directory, the flet build command will prioritize reading dependencies from it instead of those listed in `pyproject.toml`.
:::

`[project]` is the standard required section of `project.toml`.

:::note
Flet also supports `[tool.poetry]` section created by Poetry which contains project settings.
:::

A minimal `pyproject.toml` for Poetry, which is also supported by `flet build` command, is the following:

```toml
[tool.poetry]
name = "my_app"
version = "1.0.0"
description = "My first Flet project"
authors = ["John Smith <john@email.com>"]

[tool.poetry.dependencies]
python = "^3.10"
flet = "0.25.0.dev3526"
```

`project.name` (or `tool.poetry.name`) corresponds to `--project` option of `flet build` command and it will be the name of app bundle or executable. The value of `project.name` will be "slugified" where all non-alphanumeric values are replaced with dashes `-`.

`project.version` (or `tool.poetry.version`) corresponds to `--build-version` option and it is a value in "x.y.z" string used as the version number shown to users.

`project.description` (or `tool.poetry.description`) corresponds to `--description` option which is the description to use for executable or bundle.

:::note
`project.authors` and `tool.poetry.authors` are not used by `flet build`, but required by a standard and other tools.
:::

### Overriding config with CLI options

All settings in `pyproject.toml` have corresponding `flet build` CLI options. If you run the flet build command and specify options that are already configured in `pyproject.toml`, the CLI option values will override those from the configuration file.

## Project dependencies

List project dependencies in `project.dependencies` section. The value is an array with pip-like requirement specifiers:

```
[project]
dependencies = [
  "flet==0.25.0.dev3526",
  "numpy"
]
```

## Product information

All Flet specific settings should be put into `[tool.flet]` section and sub-sections below it.

Product information settings complement the ones in `[project]` section and allows configuring app bundle identifier and product display name.

```toml
[tool.flet]
org = "com.mycompany" # --org
product = "Product name" # --product
company = "My Company" # --company
copyright = "Copyright (C) 2024 by MyCompany" # --copyright
build_number = 1 # --build-number
```

## App package contents

The following settings control the contents of Python app archive and compilation of app/packages sources.

```toml
[tool.flet]
app.module = "main" # --module-name
app.path = "src" # path to Python app relative to `pyproject.toml`
app.exclude = ["assets"] # --exclude

compile.app = false # --compile-app
compile.packages = false # --compile-packages
compile.cleanup = false # --cleanup-on-compile
```

They could be alternatively written under their own sub-sections as:

```toml
[tool.flet.app]
module = "main"
path = "src"
exclude = ["assets"]

[tool.flet.compile]
app = false
packages = false
cleanup = false
```

## Splash

```toml
[tool.flet.splash]
color = "" # --splash-color
dark_color = "" # --splash-dark-color
web = false # --no-web-splash
ios = false # --no-ios-splash
android = false # --no-android-splash
```

## Permissions

```toml
[tool.flet]
permissions = ["camera", "microphone"] # --permissions
```

## Deep linking

```toml
[tool.flet.deep_linking]
scheme = "https" # --deep-linking-scheme
host = "mydomain.com" # --deep-linking-host
```

### Android settings

```toml
[tool.flet.android]
adaptive_icon_background = "" # --android-adaptive-icon-background
split_per_abi = false # --split-per-abi
```

Permissions (notice quotes `"` around key names):

```toml
[tool.flet.android.permission] # --android-permissions
"android.permission.CAMERA" = true
"android.permission.CAMERA" = true
```

Features (notice quotes `"` around key names):

```toml
[tool.flet.android.feature] # --android-features
"android.hardware.camera" = false
```

Android-specific deep-linking:

```toml
[tool.flet.android.deep_linking]
scheme = "https" # --deep-linking-scheme
host = "mydomain.com" # --deep-linking-host
```

Android bundle signing options:

```toml
[tool.flet.android.signing]
# store and key passwords can be passed with `--android-signing-key-store-password`
# and `--android-signing-key-password` options or
# FLET_ANDROID_SIGNING_KEY_STORE_PASSWORD
# and FLET_ANDROID_SIGNING_KEY_PASSWORD environment variables.
key_store = "path/to/store.jks" # --android-signing-key-store
key_alias = "upload"
```

### iOS settings

```toml
[tool.flet.ios]
team = "team_id" # --team

[tool.flet.ios.info] # --info-plist
NSCameraUsageDescription = "This app uses the camera to ..."

[tool.flet.ios.info.deep_linking]
scheme = "https"
host = "mydomain.com"
```

### macOS settings

```toml
[tool.flet.macos]
entitlement."com.apple.security.personal-information.photos-library" = true
```

```toml
[tool.flet]
build_arch = "arm64" # --arch - if arch is not specified Flet will build universal package for both arm64 and x86_64 archs
```

### Web settings

```toml
[tool.flet.web]
base_url = "/" # --base-url
renderer = "canvaskit" # --web-renderer
use_color_emoji = false # --use-color-emoji
route_url_strategy = "path" # --route-url-strategy
```

## Flutter settings

### Dependencies

```toml
flutter.dependencies = ["flet_video", "flet_audio"] # --include-packages
```

or with alternative syntax with versions:

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

### Extra build args

flutter.build_args = ["--some-flutter-arg"] # --flutter-build-args

### Extra `pubspec.yaml` settings

Allows injecting arbitrary content into resulting `pubspec.yaml`, for example:

```toml
[tool.flet.flutter.pubspec.dependency_overrides]
web = "1.0.0"
```

## Custom template

```toml
[tool.flet.template]
path = "gh:some-github/repo" # --template
dir = "" # --template-dir
ref = "" # --template-ref
```

That's it! Upgrade to Flet 0.25.0.dev3526, give this new feature and try and let us know what you think!

Cheers!