---
slug: flet-v-0-25-release-announcement
title: Flet v0.25.0 Release Announcement
authors: feodor
tags: [releases]
---

Hey Flet developers, we’ve got something exciting to share — Flet 0.25.0 is officially released!

The biggest news? No more Kivy for iOS and Android packaging. No more dealing with frustrating Python binary dependencies — Flet now uses its own custom Python runtime, so your app builds are easier than ever. Plus, we’ve added loads of new features like better permissions control, faster rebuilds, and even a lightweight Linux client that skips the bloat.

Let’s dive into all the cool stuff Flet 0.25.0 has to offer! 🚀

<!-- truncate -->

## How to upgrade

Run the following command to upgrade Flet:

```
pip install 'flet[all]' --upgrade
```

:::note
`[all]` is an "extra" specifier which tells pip to install all `flet` package dependencies. See [New Python packages structure](#new-python-packages-structure) section below for the explanation.
:::

Bump `flet` package version to `0.25.0` (or remove it at all to use the latest) in `requirements.txt` or `pyproject.toml`.

## New packaging

Flet packaging for iOS and Android has been relying on Kivy and it was super annoying when your app depends on Python binary packages, such as Numpy or Pillow. You needed to compile those packages yourself using Kivy command line tools. It was really frustrating and even hopeless if Kivy didn't have "recipes" for some packages, like Pydantic.

Flet does not depend on Kivy anymore and uses its own Python runtime "meticulously crafted in-house".

Flet packaging implementation for iOS and Androind adheres to strict specifications defined in [PEP 730](https://peps.python.org/pep-0730/) (iOS) and [PEP 738](https://peps.python.org/pep-0738/) (Android) which were implemented and released in Python 3.13 (and back-ported to Python 3.12). When pypi.org supports wheel tags for iOS and Android and 3rd-party Python package maintainers start uploading their mobile packages Flet will be compatible with them and you'll be able to use them in your Flet app.

### Pre-built binary packages

`flet build` command for iOS and Android is now installing pre-built binary packages from https://pypi.flet.dev.

New packages can be built with creating a recipe in [Mobile Forge](https://github.com/flet-dev/mobile-forge) project. For now, Flet team is authoring those recipes for you, but when the process is polished and fully-automated you'll be able to send a PR and test the compiled package right away.

If you don't yet see a package you require at https://pypi.flet.dev, you can request it in [Flet discussions - Packages](https://github.com/flet-dev/flet/discussions/categories/packages). Please do not request pure Python packages. Go to package's "Download files" section at https://pypi.org and make sure it contains binary platform-specific wheels.

Packaging behavior was changed too:

- The packaging is not trying to replace `flet` dependency with `flet-runtime`, `flet-embed` or `flet-pyodide`, but install all dependencies "as is" from `requirements.txt` or `pyproject.toml` - thanks to the [new Flet packages structure](#new-python-packages-structure).
- If the binary package for target platform is not found the packaging won't be trying to compile it from source distribution, but will fail instead with a meaningful error.

### Python 3.12

Packaged Flet app runs on Python 3.12.7 runtime on all platforms.

### Permissions

New `flet build` command allows granular control over permissions, features and entitlements embedded into `AndroidManifest.xml`, `Info.plist` and `.entitlements` files.

No more hard-coded permissions in those files!

For example, setting permissions for iOS bundle:

```
flet build --info-plist NSLocationWhenInUseUsageDescription="This app uses location service when in use."
```

or the same in `pyproject.toml` (read about `pyproject.toml` support below):

```toml
[tool.flet.ios.info] # --info-plist
NSLocationWhenInUseUsageDescription = "This app uses location service when in use."
```

An example of setting Android permissions and features:

```
flet build \
    --android-permissions android.permission.READ_EXTERNAL_STORAGE=True \
      android.permission.WRITE_EXTERNAL_STORAGE=True \
    --android-features android.hardware.location.network=False
```

[Read more about permissions in the docs](https://docs.flet.dev/publish/#permissions).

### Control over app compilation and cleanup

`flet build` command is no longer compiling app `.py` files into `.pyc` by default which allows you to defer discovery of any syntax errors in your app and complete the packaging.

You can control the compilation and cleanup with the following new options:

* `--compile-app` - compile app's `.py` files.
* `--compile-packages` - compile installed packages' `.py` files.
* `--cleanup-on-compile` - remove unnecessary files upon successful compilation.

### Signing Android bundles

We also added new options for signing Android builds:

* `--android-signing-key-store` - path to an upload keystore `.jks` file for Android apps.
* `--android-signing-key-store-password` - Android signing store password.
* `--android-signing-key-alias` - Android signing key alias. Default is "upload".
* `--android-signing-key-password` - Android signing key password.

Read [Build and release an Android app](https://docs.flutter.dev/deployment/android#signing-the-app) for more information on how to configure upload key for Android builds.

### Deep linking configuration

There is a new `--deep-linking-url` option to configure deep linking for iOS and Android builds. The value must be in the format `<sheme>://<host>`.

### Faster re-builds

Ephemeral Flutter app created by `flet build` command is no longer being re-created on every build in a temp directory, but cached in `build/flutter` directory which gives faster re-builds, improves packaging troubleshooting and does not pollute user temp directory.

You can use `--clear-cache` option to do a clean build though.

### Split APKs per ABI

`flet build` now provides the built-in `--split-per-abi` option to split the APKs per ABIs.

## "Data" and "Temp" directories for the app

Flet developers have been asking where to store application data, such as uploaded files, SQLite databases, etc. that are persistent across application updates.

This release introduce two environment variables that are available in your Flet apps:

* `FLET_APP_STORAGE_DATA` - directory for storing application data that is preserved between app updates. That directory is already pre-created and its location depends on the platform the app is running on.
* `FLET_APP_STORAGE_TEMP` - directory for temporary application files, i.e. cache. That directory is already pre-created and its location depends on the platform the app is running on.

For example, data folder path can be read in your app as:

```
import os

# it's `None` when running the app in web mode
data_dir = os.getenv("FLET_APP_STORAGE_DATA")
```

:::note
`flet run` command creates data and temp directories and sets `FLET_APP_STORAGE_DATA` and `FLET_APP_STORAGE_TEMP` to their paths.
:::

## `pyproject.toml` support

It's inconvenient and bulky to carry all `flet build` settings as command line options.

In Flet 0.25.0 release is now possible to configure `flet build`, `flet run`, and `flet publish` settings in `pyproject.toml`!

Flet adds `tool.flet` section and sub-sections to `pyproject.toml`. Here's the minimal version of `pyproject.toml` you can put into root folder of your app:

```toml
[project]
name = "my_app"
version = "1.0.0"
description = "My first Flet project"
authors = [
  {name = "John Smith", email = "john@email.com"}
]
dependencies = ["flet"]
```

You can also generate a starting `pyproject.toml` (and other files) for your project with `flet create` command.


## New Python packages structure

We re-factored Flet Python packages and removed `flet-core`, `flet-runtime`, `flet-embed` or`flet-pyodide` packages.

The new structure avoids rewriting pip dependencies while installing `flet` package on various platforms. There was a problem of detecting the correct `flet` package to install (`flet-runtime`, `flet-embed` or`flet-pyodide`?) if `flet` was not a direct dependency in user's app.

New Flet packages:

* `flet` - required for minimal Flet setup, app entry point for various platforms with core logic and controls. Installed on all platforms.
* `flet-cli` - contains Flet CLI commands. Installed on desktop only.
* `flet-desktop` - contains pre-built Flet "client" app binary for macOS, Windows and Linux. By default installed on macOS and Windows desktops only. 
* `flet-desktop-light` - contains a light-weight version (without Audio and Video controls) of Flet "client" for Linux. By default installed on Linux desktops only. 
* `flet-web` - contains Flet web "client" and FastAPI integration. Installed on desktop only.

Packaged Flet app contains only `flet` package now.

### `flet` package extras

`flet` package defines the following extras that can be specified when installing Flet with pip, uv, poetry and other package manager:

* `flet[all]` - installs `flet`, `flet-cli`, `flet-desktop` and `flet-web`. Recommended for development.
* `flet[cli]` - installs `flet` and `flet-cli`. Can be used in CI environment for packaging only.
* `flet[web]` - installs `flet` and `flet-web`. Used for deploying Flet web apps.
* `flet[desktop]` - installs `flet` and `flet-desktop`. Used for desktop-only development.

### New Flet install and upgrade commands

Starting from this release the development version of `flet` package should be installed with the following command:

```
pip install 'flet[all]'
```

Ugrading `flet` package:

```
pip install 'flet[all]' --upgrade
```

:::note
`pip install flet` still works too, but it will install `flet` package only and dependent packages will be installed on demand. For example, when you run any `flet` CLI command `flet-cli` will be installed, or when you run `flet run` command `flet-desktop` package will be installed.
:::

## "Light" client for Linux

A lightweight desktop client, without Audio and Video controls, is now installed on Linux by default. It improves initial user experience as user doesn't need to immediately deal with `gstreamer` (audio) and `mpv` (video) dependencies and Flet "just works".

Once user got some Flet experience and wants to use Video and Audio controls in their application they can install gstreamer and/or mpv and replace Flet desktop with a full version.

Uninstall "light" Flet client:

```
pip uninstall flet-desktop-light --yes
```

Install full Flet desktop client:

```
pip install flet-desktop
```

## New controls

* Mobile Ads (`Banner` and `Interstitial`) ([details and example](https://github.com/flet-dev/flet/pull/3288)).
* `Button` control ([#4265](https://github.com/flet-dev/flet/pull/4265)) - which is just an alias for `ElevatedButton` control.

## Breaking changes

* Refactor `Badge` Control to a Dataclass; added new `badge` property to all controls ([#4077](https://github.com/flet-dev/flet/pull/4077)).

Below is how to migrate:

```python
# before
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon_content=ft.Badge(
                    content=ft.Icon(ft.Icons.PHONE),
                    text=10,
                ),
                label="Calls",
            ),
        ]
    )

# after
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                  icon=ft.Icon(
                        ft.Icons.PHONE,
                        badge="10",
                    ),
                label="Calls",
            ),
        ]
    )
```

## Other changes

* Added `{value_length}`, `{max_length}`, and `{symbols_left}` placeholders to `TextField.counter_text` ([#4403](https://github.com/flet-dev/flet/pull/4403)).
* Added `--skip-flutter-doctor` to build cli command ([#4388](https://github.com/flet-dev/flet/pull/4388)).
* `WebView` enhancements ([#4018](https://github.com/flet-dev/flet/pull/4018)).
* `Map` control enhancements ([#3994](https://github.com/flet-dev/flet/pull/3994)).
* Exposed more `Theme` props ([#4278](https://github.com/flet-dev/flet/pull/4278), [#4278](https://github.com/flet-dev/flet/pull/4278)).
* Exposed more properties in multiple Controls ([#4105](https://github.com/flet-dev/flet/pull/4105))
* Added `__contains__` methods in container-alike Controls ([#4374](https://github.com/flet-dev/flet/pull/4374)).
* Added a custom `Markdown` code theme ([#4343](https://github.com/flet-dev/flet/pull/4343)).
* Added `barrier_color` prop to dialogs ([#4236](https://github.com/flet-dev/flet/pull/4236)).
* Merged `icon` and `icon_content` props into `icon: str | Control` ([#4305](https://github.com/flet-dev/flet/pull/4305)).
* Migrated `colors` and `icons` variables to Enums ([#4180](https://github.com/flet-dev/flet/pull/4180)).
* TextField: `suffix_icon`, `prefix_icon` and `icon` can be `Control` or `str` ([#4173](https://github.com/flet-dev/flet/pull/4173)).
* Added `--pyinstaller-build-args` to `flet pack` CLI command ([#4187](https://github.com/flet-dev/flet/pull/4187)).
* Made SearchBar's view height adjustable; added new properties ([#4039](https://github.com/flet-dev/flet/pull/4039)).
* Bumped Rive version and fixed Linux app build template for `rive_common`.

## Bug fixes

* Fixed `Icon` rotation ([#4384](https://github.com/flet-dev/flet/pull/4384)).
* Fixed regression in `Markdown.code_theme` when using `MarkdownCodeTheme` enum ([#4373](https://github.com/flet-dev/flet/pull/4373)).
* Fixed `Segment` and `NavigationBarDestination` accept only string tooltips ([#4326](https://github.com/flet-dev/flet/pull/4326)).
* Display informative message when `date` has wrong format ([#4019](https://github.com/flet-dev/flet/pull/4019)).
* Fixed `MapConfiguration.interaction_configuration` is not honoured ([#3976](https://github.com/flet-dev/flet/pull/3976)).
* Fixed `Video.jump_to()` fails with negative indexes ([#4294](https://github.com/flet-dev/flet/pull/4294)).
* Fixed condition in `AppBar.tooltip_opacity` ([#4280](https://github.com/flet-dev/flet/pull/4280)).
* Fixed wrong type (asyncio.Future -> concurrent.futures.Future) and handle `CancelledError` ([#4268](https://github.com/flet-dev/flet/pull/4268)).
* Fixed clicking on `CupertinoContextMenuAction` doesn't close context menu ([#3948](https://github.com/flet-dev/flet/pull/3948)).
* Fixed dropdown `max_menu_height` ([#3974](https://github.com/flet-dev/flet/pull/3974)).
* Fixed prevent button style from being modified in `before_update()` ([#4181](https://github.com/flet-dev/flet/pull/4181)).
* Fixed disabling filled buttons is not visually respected ([#4090](https://github.com/flet-dev/flet/pull/4090)).
* when `label` is set, use `MainAxisSize.min` for the `Row` ([#3998](https://github.com/flet-dev/flet/pull/3998)).
* Fixed `NavigationBarDestination.disabled` has no visual effect ([#4073](https://github.com/flet-dev/flet/pull/4073)).
* Fixed autofill in `CupertinoTextField` ([#4103](https://github.com/flet-dev/flet/pull/4103)).
* Linechart: `jsonDecode` tooltip before displaying ([#4069](https://github.com/flet-dev/flet/pull/4069)).
* Fixed button's `bgcolor`, `color` and `elevation` ([#4126](https://github.com/flet-dev/flet/pull/4126)).
* Fixed scrolling issues on Windows ([#4145](https://github.com/flet-dev/flet/pull/4145)).
* Skip running flutter doctor on windows if `no_rich_output` is `True` ([#4108](https://github.com/flet-dev/flet/pull/4108)).
* Fixed `TextField` freezes on Linux Mint #4422](https://github.com/flet-dev/flet/pull/4422)).

## Conclusion

Flet 0.25.0 is a huge release and your feedback is highly welcomed!

Upgrade to Flet 0.25.0, test your apps and let us know how you find the new features we added.

If you have any questions, please join [Flet Discord server](https://discord.gg/dzWXP8SHG8) or create a new thread
on [Flet GitHub discussions](https://github.com/flet-dev/flet/discussions).

Happy Flet-ing! 👾