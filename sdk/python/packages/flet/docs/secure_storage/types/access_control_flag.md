{{ class_all_options("flet_secure_storage.types.AccessControlFlag", separate_signature=False) }}


## Usage example
Require biometrics OR device passcode:

```python
options = IOSOptions(
    access_control_flags=[
        AccessControlFlag.BIOMETRY_ANY,
        AccessControlFlag.OR,
        AccessControlFlag.DEVICE_PASSCODE
    ]
)
```
