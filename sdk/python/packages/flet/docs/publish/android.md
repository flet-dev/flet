---
title: Packaging app for Android
---

Instructions for packaging a Flet app into an
Android APK and Android App Bundle (AAB).

/// admonition | Info
    type: tip
This guide provides detailed on Android-specific information.
Complementary and more general information is available [here](index.md).
///

## Prerequisites

### Android SDK

The build process requires both **Java** (JDK 17) and the **Android SDK**.

If either component is missing or an incompatible version is detected, the required tools will be
**automatically installed** during the first run of the [`flet build`](../cli/flet-build.md) command.

- The JDK is installed in `$HOME/java/<version>` (for example, `17.0.13+11`).
- If [**Android Studio**](https://developer.android.com/studio) is installed, Flet CLI will use its SDK:
    - macOS: `~/Library/Android/sdk`
    - Windows: `%LOCALAPPDATA%\Android\Sdk`
    - Linux: `~/Android/Sdk`
- Otherwise, a standalone Android SDK is installed in:
    - macOS/Linux: `~/Android/sdk`
    - Windows: `%USERPROFILE%\Android\sdk`

`ANDROID_HOME` and `ANDROID_SDK_ROOT` are also respected if set.

### Android wheels for binary Python packages

Binary Python packages (in contrast to "pure" Python packages written in Python only)
are packages that are partially written in C, Rust, or other languages producing native code.
Example packages are `numpy`, `cryptography`, or `pydantic-core`.

Make sure all non-pure (binary) packages used in your Flet app have
[pre-built wheels for Android](../reference/binary-packages-android-ios.md).

## `flet build apk`

/// admonition | Note
This command can be run on a **macOS**, **Linux**, or **Windows**.
///

Builds a **release** Android APK.

Release builds are optimized for production, meaning they **don’t support debugging**
and are intended for publishing to app stores such as Google Play.

For Play Store deployment, it’s recommended to:

- Use an [**Android App Bundle (AAB)**](#flet-build-aab) for more efficient delivery and smaller install size
- Or [**split the APK by ABI**](#split-apk-per-abi) to reduce the APK size

### Split APK per ABI

Android devices use different CPUs, so APKs can target different
[Application Binary Interfaces (ABIs)](https://developer.android.com/ndk/guides/abis).

By default, Flet builds a single "fat" APK that contains
native binaries for all supported ABIs. This maximizes
device compatibility but increases APK size.

Enabling ABI splits produces one APK per ABI, which reduces file size but
requires distributing the correct APK for each device.

#### Supported target architectures

The following target architectures are supported:

- [`arm64-v8a`](https://developer.android.com/ndk/guides/abis#arm64-v8a)
- [`armeabi-v7a`](https://developer.android.com/ndk/guides/abis#v7a)
- [`x86_64`](https://developer.android.com/ndk/guides/abis#86-64)
- [`x86`](https://developer.android.com/ndk/guides/abis#x86)

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--split-per-abi`](../cli/flet-build.md#-split-per-abi)
2. `[tool.flet.android].split_per_abi`
3. `false`

When enabled, 3 APKs are produced by default, one for each of the following ABIs: `arm64-v8a`,
`armeabi-v7a`, and `x86_64`. These can be customized by setting [`target architectures`](index.md#target-architecture).

#### Example

/// tab | `flet build`
```bash
flet build apk --split-per-abi
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.android]
split_per_abi = true
```
///

## `flet build aab`

/// admonition | Note
This command can be run on a **macOS**, **Linux**, or **Windows**.
///

Builds a **release** [Android App Bundle (AAB)](https://developer.android.com/guide/app-bundle) file.

Release builds are optimized for production, meaning they **don’t support debugging**
and are intended for publishing to app stores such as the [Google Play Store](https://play.google.com/store/).

It is recommended to use this AAB format (instead of [APK](#flet-build-apk)) for publishing to the
Google Play Store due to its optimized app size.

If you need to limit the ABIs included in the bundle, use
[`--arch`](index.md#target-architecture) / `[tool.flet.android].target_arch`
while `split_per_abi` is `false`.

## Signing an Android bundle

Android requires that all APKs be digitally signed with a certificate before they are installed
on a device or updated. When releasing using [Android App Bundles](#flet-build-aab), you need to sign your app bundle
with an upload key before uploading it to the Play Console, and Play App Signing takes care of the rest.
For apps distributing using APKs on the Play Store or on other stores, you must manually sign your APKs for upload.

For detailed information, see this [guide](https://developer.android.com/studio/publish/app-signing).

To publish on the Play Store, you need to sign your app with a digital certificate.

Android uses two signing keys: upload and app signing.

- Developers upload an `.aab` or `.apk` file signed with an upload key to the Play Store.
- The end-users download the `.apk` file signed with an app signing key.

To create your app signing key, use Play App Signing as described in the
[official Play Store documentation](https://support.google.com/googleplay/android-developer/answer/7384423?hl=en).

To sign your app, use the following instructions.

/// admonition | Note
If you don't provide an upload keystore, release builds are signed with the
debug key. This is fine for local testing but cannot be uploaded to the Play Store.
///

### Create an upload keystore

If you have an existing keystore, skip to the next step.
If not, create one using one of the following methods:

1. Follow the [Android Studio key generation steps](https://developer.android.com/studio/publish/app-signing#generate-key).
2. Run the following command at the command line:
    On macOS or Linux, use the following command:

    ```bash
    keytool -genkey -v -keystore ~/upload-keystore.jks -keyalg RSA \
        -keysize 2048 -validity 10000 -alias upload
    ```

    On Windows, use the following command in PowerShell:

    ```powershell
    keytool -genkey -v -keystore $env:USERPROFILE\upload-keystore.jks `
        -storetype JKS -keyalg RSA -keysize 2048 -validity 10000 `
        -alias upload
    ```
    You will be prompted for several details, such as a keystore password,
    a key alias, your names, and location. Remember the password and alias
    for use in the configuration steps below.

    A file named `upload-keystore.jks` will be created in your home directory.
    If you want to store it elsewhere, change the argument passed to the `-keystore` parameter.
    The location of the keystore file is equally important for the [key store](#key-store) step below.

    /// admonition | Note
    - The `keytool` command might not be in your path—it's part of Java, which is installed as part of Android Studio.
    For the concrete path, run `flutter doctor -v` and locate the path printed after 'Java binary at:'.
    Then use that fully qualified path replacing `java` (at the end) with `keytool`.
    If your path includes space-separated names, such as Program Files, use platform-appropriate notation
    for the names. For example, on macOS and Linux use `Program\ Files`, and on Windows use `"Program Files"`.

    - The `-storetype JKS` tag is only required for Java 9 or newer.
    As of the Java 9 release, the keystore type defaults to PKS12.
    ///

/// admonition | Important
    type: warning
Keep your `keystore` file private; never check it into public source control!
///

### Key alias

An alias name for the key within the keystore.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--android-signing-key-alias`](../cli/flet-build.md#-android-signing-key-alias)
2. `FLET_ANDROID_SIGNING_KEY_ALIAS`
3. `[tool.flet.android.signing].key_alias`
4. `"upload"`

#### Example

/// tab | `flet build`
```bash
flet build aab --android-signing-key-alias value
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.android.signing]
key_alias = "value"
```
///
/// tab | `.env`
```dotenv
FLET_ANDROID_SIGNING_KEY_ALIAS="value"
```
///

### Key store

The path to the keystore file (with extension `.jks`).

If you used the CLI commands [above](#create-an-upload-keystore) as-is, this file might be
located at `/Users/<user name>/upload-keystore.jks` on macOS
or `C:\Users\<user name>\upload-keystore.jks` on Windows.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--android-signing-key-store`](../cli/flet-build.md#-android-signing-key-store)
2. `[tool.flet.android.signing].key_store`
3. `FLET_ANDROID_SIGNING_KEY_STORE`

#### Example

/// tab | `flet build`
```bash
flet build aab --android-signing-key-store path/to/store.jks
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.android.signing]
key_store = "path/to/store.jks"
```
///
/// tab | `.env`
```dotenv
FLET_ANDROID_SIGNING_KEY_STORE="path/to/store.jks"
```
///

### Key store password

A password to unlock the keystore file (can contain multiple key entries).

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--android-signing-key-store-password`](../cli/flet-build.md#-android-signing-key-store-password)
2. `FLET_ANDROID_SIGNING_KEY_STORE_PASSWORD`
3. [key password](#key-password)

#### Example

/// tab | `flet build`
```bash
flet build aab --android-signing-key-store-password value
```
///
/// tab | `pyproject.toml`
For security reasons, the keystore password is not read from `pyproject.toml` to
prevent accidental exposure in source control. See the other tabs for supported alternatives.
///
/// tab | `.env`
```dotenv
FLET_ANDROID_SIGNING_KEY_STORE_PASSWORD="value"
```
///

### Key password

A password used to access the private key inside the keystore.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--android-signing-key-password`](../cli/flet-build.md#-android-signing-key-password)
2. `FLET_ANDROID_SIGNING_KEY_PASSWORD`
3. [key store password](#key-store-password)

#### Example

/// tab | `flet build`
```bash
flet build aab --android-signing-key-password value
```
///
/// tab | `pyproject.toml`
For security reasons, the keystore password is not read from `pyproject.toml` to
prevent accidental exposure in source control. See the other tabs for supported alternatives.
///
/// tab | `.env`
```dotenv
FLET_ANDROID_SIGNING_KEY_PASSWORD="value"
```
///

## Android Manifest

The [Android Manifest](https://developer.android.com/guide/topics/manifest/manifest-intro) describes
essential information about your app to the Android build tools,
the Android operating system, and Google Play. The file in which this information is written
is `AndroidManifest.xml`, which gets populated with the information you provide.

### Application attributes

You can add or override attributes on the `<application>` element of the
`AndroidManifest.xml` file in the [build template](index.md#build-template).

#### Resolution order

Its value is determined in the following order of precedence:

1. `[tool.flet.android.manifest_application]`

#### Example

/// tab | `pyproject.toml`
```toml
[tool.flet.android.manifest_application]
usesCleartextTraffic = "true"
allowBackup = "false"
```
///

In the [`AndroidManifest.xml`](index.md#build-template), it will be translated accordingly into this:

```xml
<application
    android:usesCleartextTraffic="true"
    android:allowBackup="false">
</application>
```

### Meta-data

A name-value pair for an item of additional, arbitrary data that can be supplied to the parent component.
More information [here](https://developer.android.com/guide/topics/manifest/meta-data-element).

A meta-data item is composed of:

- `name`: A unique name for the item, usually with a Java-style naming convention, for example `"com.sample.project.activity.fred"`.
- `value`: The value of the item. Android supports strings, integers, booleans, and floats.
  Flet writes values as strings, so pass the literal value you want Android to read
  (for example `"true"`, `"123"`, `"1.23"`).

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--android-meta-data`](../cli/flet-build.md#-android-meta-data)
2. `[tool.flet.android.meta_data]`

#### Example

/// tab | `flet build`
```bash
flet build apk --android-meta-data name_1=value_1 name_2=value_2
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.android.meta_data]
"name_1" = "value_1"
"name_2" = "value_2"
```
///

In the [`AndroidManifest.xml`](index.md#build-template), it will be translated accordingly into this:

```xml
<application>
    <meta-data android:name="name_1" android:value="value_1" />
    <meta-data android:name="name_2" android:value="value_2" />
</application>
```

### Features

A hardware or software feature that is used by the application.
More information [here](https://developer.android.com/guide/topics/manifest/uses-feature-element).

- `name`: Specifies a single hardware or software feature used by the application as a descriptor string.
    Valid attribute values are listed in the Hardware features and Software features sections.
    These attribute values are case-sensitive.
- `required`: A boolean value (`True` or `False`) that indicates whether the application requires the feature specified by the `name`.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--android-features`](../cli/flet-build.md#-android-features)
2. `[tool.flet.android.feature]`
3. [`Permissions`](index.md#permissions)
4. defaults: `android.software.leanback=false`, `android.hardware.touchscreen=false`

#### Example

/// tab | `flet build`
```bash
flet build apk --android-features android.hardware.camera=True android.hardware.location.gps=False
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.android.feature]
"android.hardware.camera" = true
"android.hardware.location.gps" = false
```
///

In the [`AndroidManifest.xml`](index.md#build-template), it will be translated accordingly into this:

```xml
<manifest>
    <uses-feature android:name="android.hardware.camera" android:required="true" />
    <uses-feature android:name="android.hardware.location.gps" android:required="false" />
</manifest>
```

### Permissions

Use cross-platform permissions from [Permissions](index.md#permissions) when possible,
and add Android-specific permissions or features here.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--android-permissions`](../cli/flet-build.md#-android-permissions)
2. `[tool.flet.android.permission]`
3. [`--permissions`](index.md#permissions) / `[tool.flet].permissions`
4. defaults: `android.permission.INTERNET=true`

CLI values are `True` or `False` (case-sensitive). In `pyproject.toml`, use `true`/`false`.

#### Example

/// tab | `flet build`
```bash
flet build apk --android-permissions android.permission.READ_EXTERNAL_STORAGE=True android.permission.WRITE_EXTERNAL_STORAGE=True
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.android.permission]
"android.permission.READ_EXTERNAL_STORAGE" = true
"android.permission.WRITE_EXTERNAL_STORAGE" = true
```
///

In the [`AndroidManifest.xml`](index.md#build-template), it will be translated accordingly into this:

```xml
<manifest>
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
</manifest>
```

### Minimum SDK version

The minimum Android API level your app can be installed on.

#### Resolution order

Its value is determined in the following order of precedence:

1. `[tool.flet.android].min_sdk_version`
2. Flutter default: `flutter.minSdkVersion`

#### Example

/// tab | `pyproject.toml`
```toml
[tool.flet.android]
min_sdk_version = 24
```
///

### Target SDK version

The Android API level your app targets for runtime behavior and compatibility.

#### Resolution order

Its value is determined in the following order of precedence:

1. `[tool.flet.android].target_sdk_version`
2. Flutter default: `flutter.targetSdkVersion`

#### Example

/// tab | `pyproject.toml`
```toml
[tool.flet.android]
target_sdk_version = 35
```
///

### Adaptive icon background

The background color used for the Android adaptive launcher icon.

This value is applied when app icons are generated for Android.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--android-adaptive-icon-background`](../cli/flet-build.md#-android-adaptive-icon-background)
2. `[tool.flet.android].adaptive_icon_background`
3. [Build template](index.md#build-template) default: `#ffffff`

#### Example

/// tab | `flet build`
```bash
flet build apk --android-adaptive-icon-background "#0B6BFF"
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.android]
adaptive_icon_background = "#0B6BFF"
```
///

## ADB Tips

[Android Debug Bridge (adb)](https://developer.android.com/tools/adb) is a
command-line tool included in the Android SDK that lets you communicate
with Android devices and emulators.

If you installed Android Studio on macOS,
`adb` is typically located at: `~/Library/Android/sdk/platform-tools/adb`.

See this [guide](https://www.makeuseof.com/install-apps-via-adb-android/) for
help installing and using adb on different platforms.

1. To run interactive commands inside an Android simulator or device:
    ```bash
    adb shell
    ```

2. To overcome "permissions denied" error while trying to browse file system in interactive Android shell:
    ```bash
    su
    ```

3. To download a file from a device to your local computer:
    ```bash
    adb pull <device-path> <local-path>
    ```

4. To install an APK on an Android device:
    ```bash
    adb install <path-to-your.apk>
    ```

    This works for both physical devices and emulators. If more than one device is connected, specify the target device:
    ```bash
    adb -s <device> install <path-to-your.apk>
    ```

    You can list available devices with:
    ```bash
    adb devices
    ```
