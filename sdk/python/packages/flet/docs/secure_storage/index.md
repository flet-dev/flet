---
class_name: flet_secure_storage.SecureStorage
examples: ../../examples/services/secure_storage
---

# Secure Storage

A service for safely storing sensitive key–value data using the platform’s native secure storage mechanisms—Keychain on iOS/macOS, Windows Credential Manager, libsecret on Linux, and Keystore on Android.

Powered by Flutter's [`flutter_secure_storage`](https://pub.dev/packages/flutter_secure_storage) package.

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅   |  ✅  |    ✅    |  ✅  |

## Configuration

Each platform provides its own set of configuration options to tailor secure storage behavior. For example, on iOS, the `IOSOptions` class includes an `accessibility` option that determines when the app can access secure values stored in the Keychain.

The `accessibility` option allows you to specify conditions under which secure values are accessible. For instance:

- `FIRST_UNLOCK`: Enables access to secure values after the device is unlocked for the first time after a reboot.
- `FIRST_UNLOCK_THIS_DEVICE`: Allows access to secure values only after the device is unlocked for the first time since installation on this device.
- `UNLOCKED` (default): Values are accessible only when the device is unlocked.

Here’s an example of configuring the accessibility option on iOS:

```python
options = IOSOptions(accessibility=KeychainAccessibility.FIRST_UNLOCK)
await storage.set(key=key, value=value, ios_options=options)
```

By setting `accessibility`, you can control when secure values are accessible, enhancing security and usability for your app on iOS. Similar platform-specific options are available for other platforms as well.

### Android

#### Disabling Auto Backup

By default Android backups data on Google Drive. It can cause exception `java.security.InvalidKeyException: Failed to unwrap key`.
You need to:

- [Disable autobackup](https://developer.android.com/guide/topics/data/autobackup#EnablingAutoBackup), [details](https://github.com/juliansteenbakker/flutter_secure_storage/issues/13#issuecomment-421083742)
- [Exclude sharedprefs](https://developer.android.com/guide/topics/data/autobackup#IncludingFiles) used by `SecureStorage`

Add the following to your `pyproject.toml`:

```toml
[tool.flet.android.manifest_application]
"allowBackup" = "false"
"fullBackupContent" = "false"
```

#### Encryption Options

##### Default
```python
AndroidOptions()
```

- **Key Cipher:** RSA/ECB/OAEPWithSHA-256AndMGF1Padding
- **Storage Cipher:** AES/GCM/NoPadding
- **Biometric Support:** No
- **Description:** Standard secure storage with RSA OAEP key wrapping. Strong authenticated encryption without biometrics. Recommended for most use cases.

##### Optional Biometrics
```python
AndroidOptions(
    enforce_biometrics=False,
    key_cipher_algorithm=KeyCipherAlgorithm.AES_GCM_NO_PADDING,
)
```

- **Key Cipher:** AES/GCM/NoPadding
- **Storage Cipher:** AES/GCM/NoPadding
- **Biometric Support:** Optional
- **Description:** KeyStore-based with optional biometric authentication. Gracefully degrades if biometrics unavailable.


##### Required Biometrics
```python
AndroidOptions(
    enforce_biometrics=True,
    key_cipher_algorithm=KeyCipherAlgorithm.AES_GCM_NO_PADDING,
)
```

- **Key Cipher:** AES/GCM/NoPadding
- **Storage Cipher:** AES/GCM/NoPadding
- **Biometric Support:** Required (API 28+)
- **Description:** KeyStore-based requiring biometric/PIN authentication. Throws error if device security not available.

#### Custom Cipher Combinations

For advanced users, all combinations below are supported using the `AndroidOptions()` constructor with custom parameters:

| Key Cipher Algorithm                        | Storage Cipher Algorithm | Implementation  | Biometric Support                   |
|---------------------------------------------|--------------------------|-----------------|-------------------------------------|
| `RSA_ECB_PKCS1_PADDING`                     | `AES_CBC_PKCS7_PADDING`  | RSA-wrapped AES | No                                  |
| `RSA_ECB_PKCS1_PADDING`                     | `AES_GCM_NO_PADDING`     | RSA-wrapped AES | No                                  |
| `RSA_ECB_OAEP_WITH_SHA256_AND_MGF1_PADDING` | `AES_CBC_PKCS7_PADDING`  | RSA-wrapped AES | No                                  |
| `RSA_ECB_OAEP_WITH_SHA256_AND_MGF1_PADDING` | `AES_GCM_NO_PADDING`     | RSA-wrapped AES | No                                  |
| `AES_GCM_NO_PADDING`                        | `AES_CBC_PKCS7_PADDING`  | KeyStore AES    | Optional (via `enforce_biometrics`) |
| `AES_GCM_NO_PADDING`                        | `AES_GCM_NO_PADDING`     | KeyStore AES    | Optional (via `enforce_biometrics`) |

/// admonition | Note
    - **RSA key ciphers** wrap the AES encryption key with RSA. No biometric support.
    - **AES key cipher** stores the key directly in Android KeyStore. Supports optional biometric authentication.
    - **`enforce_biometrics` parameter** (default: `False`):
        - `False`: Gracefully degrades if biometrics unavailable
        - `True`: Strictly requires device security (PIN/pattern/biometric), throws exception if unavailable

#### Biometric Authentication

Secure Storage supports biometric authentication (fingerprint, face recognition, etc.) on Android API 23+.

##### Required Permissions

To use biometric authentication on Android, you need to grant the necessary permissions (`USE_BIOMETRIC` and optionally `USE_FINGERPRINT`) in your project.

For configure permissions in your `pyproject.toml` or when building the app using `flet build`.

See the official Flet documentation for details: [Android Permissions in Flet](https://docs.flet.dev/publish/android/#permissions)

Example configuration in `pyproject.toml`:

```toml
[tool.flet.android.permission]
"android.permission.USE_BIOMETRIC" = true
"android.permission.USE_FINGERPRINT" = true
```

You can also pass permissions when building your Android app:

```bash
flet build \
  --android-permissions android.permission.USE_BIOMETRIC=True \
  android.permission.USE_FINGERPRINT=True
```

This ensures that biometric authentication works correctly on all supported Android devices.

##### Using Biometric Authentication

You can enable biometric authentication:

```python
# Optional biometric authentication (graceful degradation)
storage = SecureStorage(
  android_options=AndroidOptions(
    enforce_biometrics=False, # Default - works without biometrics
    biometric_prompt_title='Unlock to access your data',
    biometric_prompt_subtitle='Use fingerprint or face unlock',
  ),
)

# Strict biometric enforcement (requires device security)
storage = SecureStorage(
  android_options=AndroidOptions(
    enforce_biometrics=True, # Requires biometric/PIN/pattern
    biometric_prompt_title: 'Biometric authentication required',
  ),
)
```

/// admonition | Note
    When `enforce_biometrics = True`, the app will throw an exception if the device has no PIN, pattern, password, or biometric enrolled.

##### Requirements

- **API Level**: Android 6.0 (API 23) minimum for basic encryption
- **API Level**: Android 9.0 (API 28) minimum for enforced biometric authentication
- **Device Security**: Device must have a PIN, pattern, password, or biometric enrolled (when using `enforce_biometrics = True`)
- **Permissions**: `USE_BIOMETRIC` permission in [pyproject.toml](#required-permissions)

#### Migration from Version 9.x

Version 10 automatically migrates data from older cipher algorithms when `migrate_on_algorithm_change = True` (enabled by default).

To disable automatic migration:

```python
storage = SecureStorage(
  android_options=AndroidOptions(
    migrate_on_algorithm_change=False,
  ),
)
```

### Web

Secure Storage uses an experimental implementation using WebCrypto. Use at your own risk at this time. Feedback welcome to improve it. The intent is that the browser is creating the private key, and as a result, the encrypted strings in local_storage are not portable to other browsers or other machines and will only work on the same domain.

**It is VERY important that you have HTTP Strict Forward Secrecy enabled and the proper headers applied to your responses or you could be subject to a javascript hijack.**

Please see:

- https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security
- https://www.netsparker.com/blog/web-security/http-security-headers/

#### application-specific key option

On the web, all keys are stored in LocalStorage. `SecureStorage` has an option for the web to wrap this stored key with an application-specific key to make it more difficult to analyze.

```python
storage = SecureStorage(
  web_options=WebOptions(
    wrap_key=f'{your_application_specific_key}',
    wrap_key_iv=f'{your_application_specific_iv}',
  ),
)
```

### Windows

You need the C++ ATL libraries installed along with the rest of Visual Studio Build Tools. Download them from [here](https://visualstudio.microsoft.com/downloads/?q=build+tools) and make sure the C++ ATL under optional is installed as well.

### Linux

You need `libsecret-1-dev` on your machine to build the project, and `libsecret-1-0` to run the application (add it as a dependency after packaging your app). If you using snapcraft to build the project use the following

```bash
sudo apt-get install libsecret-1-dev libsecret-1-0
```

Apart from `libsecret` you also need a keyring service, for that you need either [`gnome-keyring`](https://wiki.gnome.org/Projects/GnomeKeyring) (for Gnome users) or [`kwalletmanager`](https://wiki.archlinux.org/title/KDE_Wallet) (for KDE users) or other light provider like [`secret-service`](https://github.com/yousefvand/secret-service).


## Usage

Add `flet-secure-storage` to your project dependencies:

/// tab | uv
```bash
uv add flet-secure-storage
```

///
/// tab | pip
```bash
pip install flet-secure-storage  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
///

/// admonition | Hosting Rive files
    type: tip
Host `.riv` files locally or load them from a CDN. Use `placeholder` to keep layouts responsive while animations load.
///

## Example

```python
--8<-- "{{ examples }}/basic.py"
```

## Description

{{ class_all_options(class_name) }}
