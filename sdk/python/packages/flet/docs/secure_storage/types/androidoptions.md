{{ class_all_options("flet_secure_storage.types.AndroidOptions") }}

## Disabling Auto Backup

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

## Encryption Options

### Default
```python
AndroidOptions()
```

- **Key Cipher:** RSA/ECB/OAEPWithSHA-256AndMGF1Padding
- **Storage Cipher:** AES/GCM/NoPadding
- **Biometric Support:** No
- **Description:** Standard secure storage with RSA OAEP key wrapping. Strong authenticated encryption without biometrics. Recommended for most use cases.

### Optional Biometrics
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

### Required Biometrics
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

## Custom Cipher Combinations

For advanced users, all combinations below are supported using the `AndroidOptions()` constructor with custom parameters:

| Key Cipher Algorithm                        | Storage Cipher Algorithm | Implementation  | Biometric Support                   |
|---------------------------------------------|--------------------------|-----------------|-------------------------------------|
| `RSA_ECB_PKCS1_PADDING`                     | `AES_CBC_PKCS7_PADDING`  | RSA-wrapped AES | No                                  |
| `RSA_ECB_PKCS1_PADDING`                     | `AES_GCM_NO_PADDING`     | RSA-wrapped AES | No                                  |
| `RSA_ECB_OAEP_WITH_SHA256_AND_MGF1_PADDING` | `AES_CBC_PKCS7_PADDING`  | RSA-wrapped AES | No                                  |
| `RSA_ECB_OAEP_WITH_SHA256_AND_MGF1_PADDING` | `AES_GCM_NO_PADDING`     | RSA-wrapped AES | No                                  |
| `AES_GCM_NO_PADDING`                        | `AES_CBC_PKCS7_PADDING`  | KeyStore AES    | Optional (via `enforce_biometrics`) |
| `AES_GCM_NO_PADDING`                        | `AES_GCM_NO_PADDING`     | KeyStore AES    | Optional (via `enforce_biometrics`) |


## Biometric Authentication

Secure Storage supports biometric authentication (fingerprint, face recognition, etc.) on Android API 23+.

### Required Permissions

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

### Using Biometric Authentication

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

### Requirements

- **API Level**: Android 6.0 (API 23) minimum for basic encryption
- **API Level**: Android 9.0 (API 28) minimum for enforced biometric authentication
- **Device Security**: Device must have a PIN, pattern, password, or biometric enrolled (when using `enforce_biometrics = True`)
- **Permissions**: `USE_BIOMETRIC` permission in [pyproject.toml](#required-permissions)
