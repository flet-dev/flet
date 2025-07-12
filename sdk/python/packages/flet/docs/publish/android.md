---
title: Packaging app for Android
---

## Introduction

Flet CLI provides `flet build apk` and `flet build aab` commands that allow packaging Flet app into Android APK and Android App Bundle (AAB) respectively.

## Prerequisites

### Android SDK

Java (JDK) and Android SDK will be automatically installed on the first run of `flet build` command.

JDK is installed into `$HOME/java/{version}` directory.

If you have Android Studio installed Flet CLI will locate and use Android SDK coming with the studio; otherwise Android SDK will be installed to `$HOME/Android/sdk` directory.

### Android wheels for binary Python packages

Binary Python packages (vs "pure" Python packages written in Python only) are packages that partially written in C, Rust or other languages producing native code. Example packages are `numpy`, `cryptography`, or `pydantic-core`.

Make sure all non-pure (binary) packages used in your Flet app have [pre-built wheels for Android](../binary-packages-android-ios.md).

## `flet build apk`

Build an Android APK file from your app.

This command builds release version. 'release' builds don't support debugging and are suitable for deploying to app stores. If you are deploying the app to the Play Store, it's recommended to use Android App Bundles (AAB) or split the APK to reduce the APK size.

* https://developer.android.com/guide/app-bundle
* https://developer.android.com/studio/build/configure-apk-splits#configure-abi-split

### Building platform-specific APKs

By default, Flet builds "fat" APK which includes binaries for both `arm64-v8a` and `armeabi-v7a` architectures.

You can configure Flet to split fat APK into smaller APKs for each platformby using `--split-per-abi` option or by setting `split_per_abi` in `pyproject.toml`:

```toml
[tool.flet.android]
split_per_abi = true
```

### Installing APK to a device

The easiest way to install APK to your device is to use `adb` (Android Debug Bridge) tool.

`adb` is a part of Android SDK. For example, on macOS, if Android SDK was installed with Android Studio
the location of `adb` tool will be at `~/Library/Android/sdk/platform-tools/adb`.

[Check this article](https://www.makeuseof.com/install-apps-via-adb-android/) for more information about installing and using `adb` tool on various platforms.

To install APK to a device run the following command:

```
adb install <path-to-your.apk>
```

If more than one device is connected to your computer (say, emulator and a physical phone) you can
use `-s` option to specify which device you want to install `.apk` on:

```
adb -s <device> install <path-to-your.apk>
```

where `<device>` can be found with `adb devices` command.

## `flet build aab`

Build an Android App Bundle (AAB) file from your app.

This command builds release version. 'release' builds don't support debugging and are suitable for deploying to app stores. App bundle is the recommended way to publish to the Play Store as it improves your app size.

## Signing Android bundle

TBD

```toml
[tool.flet.android.signing]
# store and key passwords can be passed with `--android-signing-key-store-password`
# and `--android-signing-key-password` options or
# FLET_ANDROID_SIGNING_KEY_STORE_PASSWORD
# and FLET_ANDROID_SIGNING_KEY_PASSWORD environment variables.
key_store = "path/to/store.jks" # --android-signing-key-store
key_alias = "upload"
```

## Splash screen

By default, generated Android app will be showing a splash screen with an image from `assets` directory (see below) or Flet logo. You can disable splash screen for Android app with `--no-android-splash` option.

Configuring splash in `pyproject.toml`:

```toml
[tool.flet.splash]
android = false
```

## Permissions

Configuring Android permissions and features to be written into `AndroidManifest.xml`:

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

Configuring permissions and features in `pyproject.toml` (notice quotes `"` around key names):

```toml
[tool.flet.android.permission] # --android-permissions
"android.permission.CAMERA" = true
"android.permission.CAMERA" = true

[tool.flet.android.feature] # --android-features
"android.hardware.camera" = false
```

## Meta-data

Configuring Android app meta-data to be written into `AndroidManifest.xml`:

```
flet build --android-meta-data name_1=value_1 name_2=value_2 ...
```

Default Android meta-data:

* `io.flutter.embedding.android.EnableImpeller=false`

Configuring meta-data in `pyproject.toml` (notice quotes `"` around key names):

```toml
[tool.flet.android.meta_data]
"com.google.android.gms.ads.APPLICATION_ID" = "ca-app-pub-xxxxxxxxxxxxxxxx~yyyyyyyyyy"
```

## Deep linking

You can configure deep-linking settings for Android app with the following `flet build` options:

* `--deep-linking-scheme` - deep linking URL scheme to configure for Android builds, i.g. "https" or "myapp".
* `--deep-linking-host` - deep linking URL host.

The same can be configured in `pyproject.toml`:

```toml
[tool.flet.android.deep_linking]
scheme = "https"
host = "mydomain.com"
```

See [Deep linking](https://docs.flutter.dev/ui/navigation/deep-linking) section in Flutter docs for more information and complete setup guide.

## Troubleshooting Android

To run interactive commands inside simulator or device:

```
adb shell
```

To overcome "permissions denied" error while trying to browse file system in interactive Android shell:

```
su
```

To download a file from a device to your local computer:

```
adb pull <device-path> <local-path>
```
