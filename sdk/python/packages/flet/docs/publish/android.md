---
title: Packaging app for Android
---

Instructions for packaging a Flet app into an
Android APK and Android App Bundle (AAB).

**See complementary information [here](index.md).**

## Prerequisites

### Android SDK

The build process requires both **Java** ([JDK](https://de.wikipedia.org/wiki/Java_Development_Kit))
and the **Android SDK**.

If either component is missing or an incompatible version is detected, the required tools will be
**automatically installed** during the first run of the [`flet build`](../cli/flet-build.md) command.

- The JDK will be installed in `$HOME/java/{version}`.
- If **Android Studio** is installed, Flet CLI will automatically use the Android SDK bundled with it.
  Otherwise, a standalone Android SDK will be installed in:
  `$HOME/Android/sdk`

### Android wheels for binary Python packages

Binary Python packages (in contrast to "pure" Python packages written in Python only) are packages that partially
written in C, Rust or other languages producing native code. Example packages are `numpy`, `cryptography`, or `pydantic-core`.

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

Different Android devices use different CPUs, which in turn support different instruction sets.
Each combination of CPU and instruction set has its own [Application Binary Interface (ABI)](https://developer.android.com/ndk/guides/abis).

By default, Flet will build a "fat" APK which includes binaries for both
[`arm64-v8a`](https://developer.android.com/ndk/guides/abis#arm64-v8a) and
[`armeabi-v7a`](https://developer.android.com/ndk/guides/abis#v7a) architectures. This can be useful when
deploying to a wide range of devices, but it can also result in a large APK file.

Splitting the APK allows you to build separate APKs for each target architecture.
The resulting APKs will be individually smaller.

When targeting specific architectures, make sure to distribute the correct
resulting executable/bundle to users based on their device's CPU architecture,
as installing an incompatible one will result in errors.

The following target architectures are supported:

- [`arm64-v8a`](https://developer.android.com/ndk/guides/abis#v7a)
- [`armeabi-v7a`](https://developer.android.com/ndk/guides/abis#v7a)
- [`x86_64`](https://developer.android.com/ndk/guides/abis#86-64)
- [`x86`](https://developer.android.com/ndk/guides/abis#x86)

#### Resolution order

Its value is determined in the following order of precedence:

1. `--split-per-abi`
2. `[tool.flet.android].split_per_abi`
3. `false`

When enabled, it will, by default, produce the following ABIs:
[`arm64-v8a`](https://developer.android.com/ndk/guides/abis#v7a),
[`armeabi-v7a`](https://developer.android.com/ndk/guides/abis#v7a) and
[`x86_64`](https://developer.android.com/ndk/guides/abis#86-64).
More information on how to customize the target architecture(s) can be
found [here](index.md#target-architecture).

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

### Installing APK to a device

The easiest way to install APK to your device is to use the
[Android Debug Bridge](https://developer.android.com/tools/adb) (adb) tool,
a command-line tool that can communicate between your computer and your Android device.

`adb` is a part of the Android SDK. On macOS, for example, if the Android SDK was
installed with Android Studio its location will be at `~/Library/Android/sdk/platform-tools/adb`.

Refer to this [guide](https://www.makeuseof.com/install-apps-via-adb-android/) for
more information about installing and using `adb` on various platforms.

To install an APK to a device run the following command:

```bash
adb install <path-to-your.apk>
```

If more than one device is connected to your computer (say, emulator and a physical phone) you can
use `-s` option to specify which device you want to install `.apk` on:

```bash
adb -s <device> install <path-to-your.apk>
```

where `<device>` can be found with `adb devices` command.

## <code class="doc-symbol doc-symbol-command"></code> `flet build aab`

Builds a **release** [Android App Bundle (AAB)](https://developer.android.com/guide/app-bundle) file.

Release builds are optimized for production, meaning they **don’t support debugging**
and are intended for publishing to app stores such as the [Google Play Store](https://play.google.com/store/).

It is recommended to use this AAB format (instead of [APK](#flet-build-apk)) for publishing to the
Google Play Store due to its optimized app size.

## Signing an Android bundle

Android requires that all APKs be digitally signed with a certificate before they are installed
on a device or updated. When releasing using [Android App Bundles](#flet-build-aab), you need to sign your app bundle
with an upload key before uploading it to the Play Console, and Play App Signing takes care of the rest.
For apps distributing using APKs on the Play Store or on other stores, you must manually sign your APKs for upload.

For detailed information, see this [guide](https://developer.android.com/studio/publish/app-signing).

To publish on the Play Store, you need to sign your app with a digital certificate.

Android uses two signing keys: upload and app signing.

- Developers upload an .aab or .apk file signed with an upload key to the Play Store.
- The end-users download the .apk file signed with an app signing key.

To create your app signing key, use Play App Signing as described in the
[official Play Store documentation](https://support.google.com/googleplay/android-developer/answer/7384423?hl=en).

To sign your app, use the following instructions.

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
    a key alias, your names and location. Remember the password and alias
    for use in the [configuration](#configuration) step below.

    A file named `upload-keystore.jks` will be created in your home directory.
    If you want to store it elsewhere, change the argument passed to the `-keystore` parameter.
    The location of the keystore file is equally important for the [configuration](#configuration) step below.

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

### Configuration

#### Key alias

An alias name for the key within the keystore.

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

#### Key store

The path to the keystore file (with extension `.jks`).

If you used the cli commands above as-is, this file might be located at `/Users/<user name>/upload-keystore.jks` on macOS
or `C:\\Users\\<user name>\\upload-keystore.jks` on Windows.

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

#### Key store password

A password to unlock the keystore file (can contain multiple key entries).

If not provided, defaults to the [key password](#key-password)

/// tab | `flet build`
```bash
flet build aab --android-signing-key-store-password value
```
///
/// tab | `pyproject.toml`

For security reasons, the keystore password is not read from `pyproject.toml` to
prevent accidental exposure in source control. See the other tabs for supported alternatives.

///
/// tab | Environment Variable
```bash
FLET_ANDROID_SIGNING_KEY_STORE_PASSWORD="value"
```
///

#### Key password

A password used to access the private key inside the keystore.

If not provided, defaults to the [key store password](#key-store-password)

/// tab | `flet build`
```bash
flet build aab --android-signing-key-password value
```
///
/// tab | `pyproject.toml`

For security reasons, the keystore password is not read from `pyproject.toml` to
prevent accidental exposure in source control. See the other tabs for supported alternatives.

///
/// tab | Environment Variable
```bash
FLET_ANDROID_SIGNING_KEY_PASSWORD="value"
```
///

## Disable splash screen

The [splash screen](index.md#splash-screen) is enabled/shown by default.

It can be disabled as follows:

/// tab | `flet build`
```bash
flet build apk --no-android-splash
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.splash]
android = false
```
///

## Android Manifest

The [Android Manifest](https://developer.android.com/guide/topics/manifest/manifest-intro) describes
essential information about your app to the Android build tools,
the Android operating system, and Google Play. The file in which this information is written
is `AndroidManifest.xml`, which gets populated with the information you provide.

### Meta-data

A name-value pair for an item of additional, arbitrary data that can be supplied to the parent component.
More information [here](https://developer.android.com/guide/topics/manifest/meta-data-element).

A meta-data item is composed of:

- `name`: A unique name for the item, usually with a Java-style naming convention, for example `"com.sample.project.activity.fred"`.
- `value`: The value of the item. The following types are supported:
    - **String**: use double backslashes (`\\`) to escape characters, such as `\\n` for a new line and `\\uxxxxx` for a Unicode character
    - **Integer**: for example `123`
    - **Boolean**: either `"true"` or `"false"`
    - **Float**: for example `1.23`

You can configure meta-data as follows:

/// tab | `flet build`
```bash
flet build apk --android-meta-data name_1=value_1 name_2=value_2
```
///
/// tab | `pyproject.toml`
/// tab | `[tool.flet.android.meta_data]`
```toml
[tool.flet.android.meta_data]
"name_1" = value_1
"name_2" = value_2
```
///

And it will be translated accordingly into this in the `AndroidManifest.xml`:

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

You can configure features as follows:

/// tab | `flet build`
```bash
flet build apk --android-features name_1=required_1 name_2=required_2
```
///
/// tab | `pyproject.toml`
```toml
[tool.flet.android.meta_data]
"name_1" = required_1
"name_2" = required_2
```
///

And it will be translated accordingly into this in the `AndroidManifest.xml`:

```xml
<manifest>
    <uses-feature android:name="name_1" android:required="required_1" />
    <uses-feature android:name="name_2" android:required="required_2" />
</manifest>
```

Where the `required` value is either `true` or `false`.

Below are default/pre-configured features:

- `"android.software.leanback" = False`
- `"android.hardware.touchscreen" = False`

### Permissions

Configuring Android permissions and features to be written into `AndroidManifest.xml`:

```bash
flet build --android-permissions permission=True|False ... --android-features feature_name=True|False
```

For example:

```bash
flet build \
    --android-permissions android.permission.READ_EXTERNAL_STORAGE=True \
      android.permission.WRITE_EXTERNAL_STORAGE=True \
    --android-features android.hardware.location.network=False
```

Default Android permissions:

* `android.permission.INTERNET`

Default permissions can be disabled with `--android-permissions` option and `False` value, for example:

```bash
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

## ADB Tips

To run interactive commands inside simulator or device:

```bash
adb shell
```

To overcome "permissions denied" error while trying to browse file system in interactive Android shell:

```bash
su
```

To download a file from a device to your local computer:

```bash
adb pull <device-path> <local-path>
```
