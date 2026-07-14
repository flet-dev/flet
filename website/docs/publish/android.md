---
title: "Packaging app for Android"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';

Instructions for packaging a Flet app into an
Android APK and Android App Bundle (AAB).

:::tip[Info]
This guide provides detailed Android-specific information.
Complementary and more general information is available [here](index.md).
:::

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

:::note[Note]
This command can be run on a **macOS**, **Linux**, or **Windows**.
:::

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

The following target architectures are supported, for every
[bundled Python version](index.md#choosing-a-python-version):

- [`arm64-v8a`](https://developer.android.com/ndk/guides/abis#arm64-v8a) (64-bit)
- [`x86_64`](https://developer.android.com/ndk/guides/abis#x86-64) (64-bit)
- [`armeabi-v7a`](https://developer.android.com/ndk/guides/abis#v7a) (32-bit)

The 32-bit `x86` ABI is not supported — specifying it fails the build since Flet 0.86.0
(see the [migration guide](../updates/breaking-changes/v0-86-0/android-x86-arch-removed.md)).

:::note
Flet bundles [its own CPython builds](https://github.com/flet-dev/python-build) for
Android, published for all three ABIs on every supported Python version — including
32-bit `armeabi-v7a`, which upstream CPython dropped in 3.13
([PEP 738](https://peps.python.org/pep-0738/)). By default, an app is built for all
supported architectures.
:::

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--split-per-abi`](../cli/flet-build.md#--split-per-abi)
2. `[tool.flet.android].split_per_abi`
3. `false`

When enabled, one APK is produced per ABI — by default, one for each
architecture the bundled Python version supports (see above). These can be
customized by setting [`target architectures`](index.md#target-architecture).

#### Example

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build apk --split-per-abi
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.android]
split_per_abi = true
```
</TabItem>
</Tabs>
## `flet build aab`

:::note[Note]
This command can be run on a **macOS**, **Linux**, or **Windows**.
:::

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

:::note[Note]
If you don't provide an upload keystore, release builds are signed with the
debug key. This is fine for local testing but cannot be uploaded to the Play Store.
:::

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

:::note[Note]
    - The `keytool` command might not be in your path—it's part of Java, which is installed as part of Android Studio.
    For the concrete path, run `flutter doctor -v` and locate the path printed after 'Java binary at:'.
    Then use that fully qualified path replacing `java` (at the end) with `keytool`.
    If your path includes space-separated names, such as Program Files, use platform-appropriate notation
    for the names. For example, on macOS and Linux use `Program\ Files`, and on Windows use `"Program Files"`.

    - The `-storetype JKS` tag is only required for Java 9 or newer.
    As of the Java 9 release, the keystore type defaults to PKCS12.
:::

:::warning[Important]
Keep your `keystore` file private; never check it into public source control!
:::

### Key alias

An alias name for the key within the keystore.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--android-signing-key-alias`](../cli/flet-build.md#--android-signing-key-alias)
2. `FLET_ANDROID_SIGNING_KEY_ALIAS`
3. `[tool.flet.android.signing].key_alias`
4. `"upload"`

#### Example

<Tabs groupId="flet-build--pyproject-toml--env">
<TabItem value="flet-build" label="flet build">
```bash
flet build aab --android-signing-key-alias value
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.android.signing]
key_alias = "value"
```
</TabItem>
<TabItem value="env" label=".env">
```dotenv
FLET_ANDROID_SIGNING_KEY_ALIAS="value"
```
</TabItem>
</Tabs>
### Key store

The path to the keystore file (with extension `.jks`).

If you used the CLI commands [above](#create-an-upload-keystore) as-is, this file might be
located at `/Users/<user name>/upload-keystore.jks` on macOS
or `C:\Users\<user name>\upload-keystore.jks` on Windows.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--android-signing-key-store`](../cli/flet-build.md#--android-signing-key-store)
2. `[tool.flet.android.signing].key_store`
3. `FLET_ANDROID_SIGNING_KEY_STORE`

#### Example

<Tabs groupId="flet-build--pyproject-toml--env">
<TabItem value="flet-build" label="flet build">
```bash
flet build aab --android-signing-key-store path/to/store.jks
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.android.signing]
key_store = "path/to/store.jks"
```
</TabItem>
<TabItem value="env" label=".env">
```dotenv
FLET_ANDROID_SIGNING_KEY_STORE="path/to/store.jks"
```
</TabItem>
</Tabs>
### Key store password

A password to unlock the keystore file (can contain multiple key entries).

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--android-signing-key-store-password`](../cli/flet-build.md#--android-signing-key-store-password)
2. `FLET_ANDROID_SIGNING_KEY_STORE_PASSWORD`
3. [key password](#key-password)

#### Example

<Tabs groupId="flet-build--pyproject-toml--env">
<TabItem value="flet-build" label="flet build">
```bash
flet build aab --android-signing-key-store-password value
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
For security reasons, the keystore password is not read from `pyproject.toml` to
prevent accidental exposure in source control. See the other tabs for supported alternatives.
</TabItem>
<TabItem value="env" label=".env">
```dotenv
FLET_ANDROID_SIGNING_KEY_STORE_PASSWORD="value"
```
</TabItem>
</Tabs>
### Key password

A password used to access the private key inside the keystore.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--android-signing-key-password`](../cli/flet-build.md#--android-signing-key-password)
2. `FLET_ANDROID_SIGNING_KEY_PASSWORD`
3. [key store password](#key-store-password)

#### Example

<Tabs groupId="flet-build--pyproject-toml--env">
<TabItem value="flet-build" label="flet build">
```bash
flet build aab --android-signing-key-password value
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
For security reasons, the keystore password is not read from `pyproject.toml` to
prevent accidental exposure in source control. See the other tabs for supported alternatives.
</TabItem>
<TabItem value="env" label=".env">
```dotenv
FLET_ANDROID_SIGNING_KEY_PASSWORD="value"
```
</TabItem>
</Tabs>
## Android Manifest

The [Android Manifest](https://developer.android.com/guide/topics/manifest/manifest-intro) describes
essential information about your app to the Android build tools,
the Android operating system, and Google Play. The file in which this information is written
is `AndroidManifest.xml`, which gets populated with the information you provide.

### Application attributes

You can add or override attributes on the `<application>` element of the
`AndroidManifest.xml` file in the [build template](index.md#build-template).

See also:

- [`<application>` element](https://developer.android.com/guide/topics/manifest/application-element)

#### Resolution order

Its value is determined in the following order of precedence:

1. `[tool.flet.android.manifest_application]`

#### Example

<Tabs groupId="pyproject-toml">
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.android.manifest_application]
usesCleartextTraffic = "true"
allowBackup = "false"
```
</TabItem>
</Tabs>
<details>
<summary>Template translation</summary>

In the [`AndroidManifest.xml`](index.md#build-template),
the `pyproject.toml` example above will be translated accordingly into this:

```xml
<application
    android:usesCleartextTraffic="true"
    android:allowBackup="false">
</application>
```
</details>

### Meta-data

A name-value pair for an item of additional, arbitrary data that can be supplied to the parent component.
More information [here](https://developer.android.com/guide/topics/manifest/meta-data-element).

A meta-data item is composed of:

- `name`: A unique name for the item, usually with a Java-style naming convention, for example `"com.sample.project.activity.fred"`.
- `value`: The value of the item. Android supports strings, integers, booleans, and floats.
  Flet writes values as strings, so pass the literal value you want Android to read
  (for example `"true"`, `"123"`, `"1.23"`).

See also:

- [`<meta-data>` element](https://developer.android.com/guide/topics/manifest/meta-data-element)

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--android-meta-data`](../cli/flet-build.md#--android-meta-data)
2. `[tool.flet.android.meta_data]`

#### Example

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build apk \
  --android-meta-data firebase_analytics_collection_enabled=true \
  --android-meta-data default_timeout_seconds=30
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.android.meta_data]
"firebase_analytics_collection_enabled" = "true"
"default_timeout_seconds" = "30"
```
</TabItem>
</Tabs>
<details>
<summary>Template translation</summary>

In the [`AndroidManifest.xml`](index.md#build-template),
the `pyproject.toml` example above will be translated accordingly into this:

```xml
<application>
    <meta-data android:name="firebase_analytics_collection_enabled" android:value="true" />
    <meta-data android:name="default_timeout_seconds" android:value="30" />
</application>
```
</details>

### Providers

A content provider component that supplies app data to other apps or components.
More information [here](https://developer.android.com/guide/topics/manifest/provider-element).

Each provider is declared as a TOML table whose key is the provider's
`android:name` (the fully-qualified class name). The table's entries become
extra `android:<key>="<value>"` attributes on the generated `<provider>`
element. A reserved `meta_data` sub-table emits nested `<meta-data>` children
inside the provider.

See also:

- [`<provider>` element](https://developer.android.com/guide/topics/manifest/provider-element)

#### Resolution order

Its value is determined in the following order of precedence:

1. `[tool.flet.android.provider]`

#### Supported value forms

The value for each provider must be a TOML inline table or sub-table of
attributes. A value of `false` skips the entry entirely; `true` is not
accepted (a `<provider>` with no attributes is meaningless). An empty table
`{}` is also treated as `false`.

Attribute values must be strings, booleans, or numbers — they are written
verbatim into the manifest. The `name` key is reserved (the `android:name`
comes from the table key).

The reserved `meta_data` sub-table emits `<meta-data>` children. Each
sub-entry's key is the `android:name`; the value can be either:

- a scalar (string/bool/number) — rendered as `android:value="…"`, or
- an inline table — its entries become `android:<key>="<value>"` attributes
  on the `<meta-data>` element (useful for `android:resource="@xml/…"`).

#### Example

<Tabs groupId="pyproject-toml">
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.android.provider]
"rikka.shizuku.ShizukuProvider" = { authorities = "${applicationId}.shizuku", multiprocess = "false", enabled = "true", exported = "true", permission = "android.permission.INTERACT_ACROSS_USERS_FULL" }

[tool.flet.android.provider."com.example.MyProvider"]
authorities = "${applicationId}.myprovider"
exported = false
grantUriPermissions = true

[tool.flet.android.provider."com.example.MyProvider".meta_data]
"android.support.FILE_PROVIDER_PATHS" = { resource = "@xml/file_paths" }
"some.other.key" = "some-value"
```
</TabItem>
</Tabs>
<details>
<summary>Template translation</summary>

In the [`AndroidManifest.xml`](index.md#build-template),
the `pyproject.toml` example above will be translated accordingly into this:

```xml
<application>
    <provider android:name="rikka.shizuku.ShizukuProvider"
              android:authorities="${applicationId}.shizuku"
              android:multiprocess="false"
              android:enabled="true"
              android:exported="true"
              android:permission="android.permission.INTERACT_ACROSS_USERS_FULL" />
    <provider android:name="com.example.MyProvider"
              android:authorities="${applicationId}.myprovider"
              android:exported="false"
              android:grantUriPermissions="true">
        <meta-data android:name="android.support.FILE_PROVIDER_PATHS" android:resource="@xml/file_paths" />
        <meta-data android:name="some.other.key" android:value="some-value" />
    </provider>
</application>
```
</details>

:::note
Flet already declares a built-in `androidx.core.content.FileProvider` with
authorities `${applicationId}.provider`. Declaring another provider that
uses the same authorities will cause the Android manifest merger to fail —
pick a different `android:authorities` value for your custom provider.
:::

### Features

A hardware or software feature that is used by the application.
More information [here](https://developer.android.com/guide/topics/manifest/uses-feature-element).

- `name`: Specifies a single hardware or software feature used by the application as a descriptor string.
    Valid attribute values are listed in the Hardware features and Software features sections.
    These attribute values are case-sensitive.
- `required`: A boolean value (`true` or `false`) that indicates whether the application requires the feature specified by the `name`.

See also:

- [`<uses-feature>` element](https://developer.android.com/guide/topics/manifest/uses-feature-element)
- [Features reference](https://developer.android.com/guide/topics/manifest/uses-feature-element#features-reference)

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--android-features`](../cli/flet-build.md#--android-features)
2. `[tool.flet.android.feature]`
3. Values injected by [cross-platform permission bundles](index.md#permissions), if any.
4. defaults: `android.software.leanback=false`, `android.hardware.touchscreen=false`

#### Supported value forms

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
Accepts repeated `<name>=<required>` entries.
The `<required>` value can be `true` or `false` (case-insensitive).
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
Use boolean values. TOML booleans must be lowercase: `true` or `false`.
</TabItem>
</Tabs>
#### Example

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build apk \
  --android-features android.hardware.camera=true \
  --android-features android.hardware.location.gps=false
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.android.feature]
"android.hardware.camera" = true
"android.hardware.location.gps" = false
```
</TabItem>
</Tabs>
<details>
<summary>Template translation</summary>

In the [`AndroidManifest.xml`](index.md#build-template),
the example above will be translated accordingly into this:

```xml
<manifest>
    <uses-feature android:name="android.hardware.camera" android:required="true" />
    <uses-feature android:name="android.hardware.location.gps" android:required="false" />
</manifest>
```
</details>

### Permissions

Use cross-platform permissions from [Permissions](index.md#permissions) when possible,
and add Android-specific permissions or features here.

See also:

- [`Manifest.permission` constants](https://developer.android.com/reference/android/Manifest.permission)
- [Request app permissions](https://developer.android.com/training/permissions/requesting)

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--android-permissions`](../cli/flet-build.md#--android-permissions)
2. `[tool.flet.android.permission]`
3. Values injected by [cross-platform permission bundles](index.md#permissions), if any.
4. defaults: `android.permission.INTERNET=true`

#### Supported value forms

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
Accepts repeated `<name>=<enabled>` entries.
The `<enabled>` value can be `true` or `false` (case-insensitive).
Permissions with `false` are omitted from the generated manifest.
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
Use boolean values. TOML booleans must be lowercase: `true` or `false`.
Permissions set to `false` are omitted from the generated manifest.

A value can also be a TOML inline table whose entries become extra
`android:<key>="<value>"` attributes on the generated `<uses-permission>`
element — useful for attributes like `maxSdkVersion` or `usesPermissionFlags`.
A non-empty table is always emitted; an empty table `{}` is treated as `false`.
</TabItem>
</Tabs>
#### Example

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build apk \
  --android-permissions android.permission.READ_EXTERNAL_STORAGE=true \
  --android-permissions android.permission.WRITE_EXTERNAL_STORAGE=true
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.android.permission]
"android.permission.READ_EXTERNAL_STORAGE" = true
"android.permission.WRITE_EXTERNAL_STORAGE" = true
"android.permission.ACCESS_FINE_LOCATION" = { maxSdkVersion = "30" }
"android.permission.BLUETOOTH_SCAN" = { usesPermissionFlags = "neverForLocation" }
```
</TabItem>
</Tabs>
<details>
<summary>Template translation</summary>

In the [`AndroidManifest.xml`](index.md#build-template),
the `pyproject.toml` example above will be translated accordingly into this:

```xml
<manifest>
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" android:maxSdkVersion="30" />
    <uses-permission android:name="android.permission.BLUETOOTH_SCAN" android:usesPermissionFlags="neverForLocation" />
</manifest>
```
</details>

### Minimum SDK version

The minimum Android API level your app can be installed on.

See also:

- [`<uses-sdk>` element (`minSdkVersion`)](https://developer.android.com/guide/topics/manifest/uses-sdk-element)
- [Android API level reference](https://developer.android.com/guide/topics/manifest/uses-sdk-element#ApiLevels)

#### Resolution order

Its value is determined in the following order of precedence:

1. `[tool.flet.android].min_sdk_version`
2. Flutter default: `flutter.minSdkVersion`

#### Example

<Tabs groupId="pyproject-toml">
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.android]
min_sdk_version = 24
```
</TabItem>
</Tabs>
<details>
<summary>Template translation</summary>

In the [`android/app/build.gradle.kts`](index.md#build-template),
the `pyproject.toml` example above will be translated accordingly into this:

```kotlin
defaultConfig {
    val resolvedMinSdk = 24
    minSdk = resolvedMinSdk
}
```
</details>

### Target SDK version

The Android API level your app targets for runtime behavior and compatibility.

See also:

- [`<uses-sdk>` element (`targetSdkVersion`)](https://developer.android.com/guide/topics/manifest/uses-sdk-element)
- [Target API level requirements and behavior changes](https://developer.android.com/google/play/requirements/target-sdk)

#### Resolution order

Its value is determined in the following order of precedence:

1. `[tool.flet.android].target_sdk_version`
2. Flutter default: `flutter.targetSdkVersion`

#### Example

<Tabs groupId="pyproject-toml">
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.android]
target_sdk_version = 35
```
</TabItem>
</Tabs>
<details>
<summary>Template translation</summary>

In the [`android/app/build.gradle.kts`](index.md#build-template),
the `pyproject.toml` example above will be translated accordingly into this:

```kotlin
defaultConfig {
    val resolvedTargetSdk = 35
    targetSdk = resolvedTargetSdk
}
```
</details>

### Adaptive icon background

The background color used for the Android adaptive launcher icon.

This value is applied when app icons are generated for Android.

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--android-adaptive-icon-background`](../cli/flet-build.md#--android-adaptive-icon-background)
2. `[tool.flet.android].adaptive_icon_background`
3. [Build template](index.md#build-template) default: `#ffffff`

#### Example

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build apk --android-adaptive-icon-background "#0B6BFF"
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.android]
adaptive_icon_background = "#0B6BFF"
```
</TabItem>
</Tabs>

## Extract packages

On Android, pure Python code is packaged into stored zip assets and imported in place with
[`zipimport`](https://docs.python.org/3/library/zipimport.html). Native extension modules are
loaded memory-mapped directly from the APK. This keeps APKs smaller and avoids unpacking all
site-packages on first launch.

Most packages work from inside the zip. But packages that read bundled **data files** through a real
filesystem path — for example with `__file__` or `pkg_resources`, instead of the zip-safe
[`importlib.resources`](https://docs.python.org/3/library/importlib.resources.html) — may fail at
runtime because their data lives inside `sitepackages.zip`, where plain `open()` cannot read it.

List such packages in `extract_packages` to ship them extracted to the app's files directory
instead of inside `sitepackages.zip`. Flet extracts the listed package directories and everything
under them, so `__file__`-relative reads work again.

Most packages that bundle data (such as `flet` or `certifi`) read it through `importlib.resources`, which
is zip-safe, so they need no entry here. Only add packages that actually fail to find their data
when imported from the zip.

### Symptoms

The build succeeds, but the app crashes or errors on the device when the package is imported or
first used. The traceback usually contains a path where `sitepackages.zip` or `stdlib.zip` appears
as a directory component, for example (`matplotlib`):

```bash
FileNotFoundError: [Errno 2] No such file or directory:
  '/data/user/0/<applicationId>/files/.../sitepackages.zip/matplotlib/mpl-data/matplotlibrc'
```

`NotADirectoryError` or `OSError` with a similar `sitepackages.zip/...` path is also a common sign
that the package computed a data path from `__file__` and tried to read it as a regular file.

If this happens with one of your dependencies, add that package to `extract_packages` and consider
reporting it in [Flet discussions](https://github.com/flet-dev/flet/discussions) or opening a PR so
it can be added to the known packages list.

### Resolution order

1. [`--android-extract-packages`](../cli/flet-build.md#--android-extract-packages)
2. `[tool.flet.android].extract_packages`
3. `[tool.flet].extract_packages`

### Example

Each entry is the package's **import name** — its top-level directory under site-packages — not
necessarily its PyPI distribution name. For example, use `sklearn`, not `scikit-learn`; use `cv2`,
not `opencv-python`.

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build apk --android-extract-packages package1 package2
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.android]
extract_packages = ["package1", "package2"]
```
</TabItem>
</Tabs>

### Wildcards

An entry is a path relative to site-packages and matches that path and everything under it.
Entries may also contain `*` and `?` wildcards, matched against the top-level directory name:

```toml
[tool.flet.android]
extract_packages = ["somepackage*"]
```

The wildcard form can also extract a sibling `somepackage-<version>.dist-info/` directory.
Use it for packages that read their metadata or data files through `pkg_resources`.

### Affected packages

Below are known packages that need to be extracted to work on Android:

| Package (PyPI)  | Entry              | Reason                                                                                 |
|-----------------|--------------------|----------------------------------------------------------------------------------------|
| `matplotlib`    | `"matplotlib"`     | reads `mpl-data` (fonts, `matplotlibrc`) relative to `__file__`                        |
| `scikit-learn`  | `"sklearn"`        | loads bundled data files through `__file__`-relative paths                             |
| `opencv-python` | `"cv2"`            | resolves config files and loads its native extension through `__file__`-relative paths |
| `astropy`       | `"astropy"`        | reads `astropy/CITATION` via `__file__` at import                                      |
| `thinc`         | `"thinc"`          | reads `thinc/backends/_custom_kernels.cu` via `__file__` at import                     |
| `spacy`         | `"spacy", "thinc"` | imports `thinc` at load and reads its own language data via `__file__`; list both      |

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
