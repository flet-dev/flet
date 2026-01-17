{{ class_all_options("flet_secure_storage.types.IOSOptions") }}

## Usage Example

### Usage with accessibility control
```python
from flet_secure_storage import SecureStorage
from flet_secure_storage.types import IOSOptions, KeychainAccessibility

storage = SecureStorage(
    ios_options=IOSOptions(
        accessibility=KeychainAccessibility.FIRST_UNLOCK
    )
)

await storage.set(key="token", value="secret_value")
```

### Biometric authentication:
```python
from flet_secure_storage.types import IOSOptions, AccessControlFlag

options = IOSOptions(
    access_control_flags=[
        AccessControlFlag.BIOMETRY_ANY,
        AccessControlFlag.OR,
        AccessControlFlag.DEVICE_PASSCODE
    ]
)

await storage.set(key="secure_key", value="secure_value", ios=options)
```
