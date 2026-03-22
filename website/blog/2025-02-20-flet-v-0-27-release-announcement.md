---
slug: flet-v-0-27-release-announcement
title: Flet v0.27.0 Release Announcement
authors: feodor
tags: [releases]
---

Flet 0.27.0 is now released with exciting new features and improvements!

* **iOS packaging & signing updates** – ensures compliance with App Store Connect verification requirements.
* **Reduced startup delay** – faster initial launch for desktop applications.
* **Faster incremental re-builds** – enhances development efficiency with quicker iteration times.
* **Enhanced Dropdown control** – improved functionality and user experience.
* **Bug fixes & stability improvements** – various fixes to enhance overall performance and reliability.

<!-- truncate -->

## How to upgrade

Run the following command to upgrade Flet:

```
pip install 'flet[all]' --upgrade
```

:::note
`[all]` is an "extra" specifier which tells pip to install or upgrade all `flet` packages: `flet`, `flet-cli`, `flet-desktop` and `flet-web`.
:::

Bump `flet` package version to `0.27.0` (or remove it at all to use the latest) in your `pyproject.toml`.

## Revamped iOS Packaging

* Third-party Flet app dependencies (also known as “site packages” like `numpy`, `pandas`, `flet`, etc.) are now bundled inside a framework, ensuring Xcode signs all files correctly and passes App Store Connect verification.
* New `flet build` options for proper iOS package signing.
* Comprehensive step-by-step documentation for packaging and deploying iOS apps. [Learn more!](https://docs.flet.dev/publish/ios/)

## Enhanced startup performance for desktop apps

Currently, when packaging for macOS, Windows, and Linux, third-party Flet app dependencies (e.g., numpy, pandas, flet, etc.), also known as **site packages**, are bundled inside the app.zip artifact. This can cause a startup delay, sometimes significant, as the app needs to extract the artifact to the user’s file system before launching.

With Flet 0.27.0, site packages are now copied in an **unpacked state** directly into the application bundle instead of being compressed into app.zip. This change significantly reduces the first launch time.

## Faster incremental re-builds

If certain parts of the build configuration remain unchanged, the `flet build` command attempts to skip or optimize specific build pipeline steps (such as re-installing Flet app dependencies), reducing the overall completion time for consecutive builds.

Faster builds mean happier developers! 😄

## Pyodide 0.27.2

Pyodide 0.27.2 is based on Python 3.12 and has some serious performance improvments to foreign function interface (FFI).

Flet now supports Python 3.12 across all packaging platforms.

The next stop is Python 3.13!

## Enhanced `Dropdown` control.

Since version 0.27.0, Flet uses [DropdownMenu](https://api.flutter.dev/flutter/material/DropdownMenu-class.html) flutter widget for [Dropdown](https://docs.flet.dev/controls/dropdown/) control, which is a Material 3 version of previously used DropdownButton. Additionally to enhanced look and feel, it allows filter the list based on the text input or search one item in the menu list.

<img src="/img/docs/controls/dropdown/dropdown-search.gif" className="screenshot-30"/>
 
Some properties of previous Dropdown implementation are not available in the new version and were "stubbed" - they will not break your program but don't do anything. See the list of deprecated properties [here](https://docs.flet.dev/controls/dropdown/).

Previous version of Dropdown control is available as [`DropdownM2`](https://docs.flet.dev/controls/dropdownm2/) control and will be removed in Flet 0.30.0.

## 💥 Breaking changes

### `flet build` command

- `--team` option renamed to `--ios-team-id`.
- `--include-packages` has been removed. Just add extension package into `dependencies` section of your `pyproject.toml` file: https://docs.flet.dev/extend/built-in-extensions/
- `--cleanup-on-compile` removed and two new options added to separate cleanup of app and 3rd-party site packages: `--cleanup-app` and `--cleanup-packages`. Two additional options: `--cleanup-app-files` and `--cleanup-package-files` work together with `--cleanup-*` and allow specifying lists of globs to exclude from app and site packages.
- `tool.flet.build_arch` renamed to `tool.flet.target_arch`.

### Removed `v0.24.0` Deprecations

The following items, deprecated in Flet 0.24.0, have been removed: https://flet.dev/blog/flet-v-0-24-release-announcement#deprecations

### `CupertinoCheckbox.inactive_color` property

The `inactive_color` property of the [`CupertinoCheckbox`](https://docs.flet.dev/controls/cupertinocheckbox/) has been removed in favor of [`fill_color`](https://docs.flet.dev/controls/cupertinocheckbox/#flet.CupertinoCheckbox.fill_color).

## Other changes

The full list of changes can be found in the [CHANGELOG](https://github.com/flet-dev/flet/blob/main/CHANGELOG.md).

### New features

* feat: `ReorderableListView` Control ([#4865](https://github.com/flet-dev/flet/pull/4865))
* feat: Implement `Container.dark_theme` property ([#4857](https://github.com/flet-dev/flet/issues/4857))
* Upgrade to Pyodide 0.27 for `httpx` Support ([#4840](https://github.com/flet-dev/flet/issues/4840))
* Remove `CupertinoCheckbox.inactive_color` in favor of `fill_color` ([#4837](https://github.com/flet-dev/flet/issues/4837))
* feat: `flet build`: use Provisioning Profile to sign iOS app archive (`.ipa`), deprecate `--team` option ([#4869](https://github.com/flet-dev/flet/issues/4869))
* feat: `flet doctor` CLI command ([#4803](https://github.com/flet-dev/flet/pull/4803))
* feat: implement button themes (for `ElevatedButton`, `OutlinedButton`, `TextButton`, `FilledButton`, `IconButton `) ([#4872](https://github.com/flet-dev/flet/pull/4872))
* feat: `ControlEvent.data` should be of type `Optional[str]` and default to `None` ([#4786](https://github.com/flet-dev/flet/issues/4786))
* feat: `flet build`: add `--source-packages` to allow installing certain Python packages from source distros ([#4762](https://github.com/flet-dev/flet/issues/4762))

### Bug fixes

* Fixed: Disable rich's Markup for stdout logs ([#4795](https://github.com/flet-dev/flet/issues/4795))
* Fixed: Setting `SearchBar.bar_border_side` isn't visually honoured ([#4767](https://github.com/flet-dev/flet/issues/4767))
* Fixed: Dropdown: Long options cause the down-arrow to oveflow ([#4838](https://github.com/flet-dev/flet/issues/4838))
* Fixed: CupertinoSlider initialisation does not allow values less then zero/greater then 1 ([#4853](https://github.com/flet-dev/flet/issues/4853))
* Fixed: Same code shows different appearance in Flet APP/Web/PC local. ([#4855](https://github.com/flet-dev/flet/issues/4855))
* Fixed: Transforming scale renders a grey screen ([#4759](https://github.com/flet-dev/flet/issues/4759))
* Fixed: UnicodeDecodeError when using accented characters in manifest.json ([#4713](https://github.com/flet-dev/flet/issues/4713))
* Fixed: Implement `SearchBar.blur()` to programmatically unfocus the bar ([#4827](https://github.com/flet-dev/flet/issues/4827))
* Fixed: Disable markup for flet-cli stdout logs ([#4796](https://github.com/flet-dev/flet/pull/4796))

## Conclusion

Upgrade to Flet 0.27.0, test your apps and let us know how you find the new features we added.

If you have any questions, please join [Flet Discord server](https://discord.gg/dzWXP8SHG8) or create a new thread
on [Flet GitHub discussions](https://github.com/flet-dev/flet/discussions).

Happy Flet-ing! 👾