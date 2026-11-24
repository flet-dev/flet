---
title: "AccessControlFlag"
---

import {ClassAll} from '@site/src/components/crocodocs';

<ClassAll name="flet_secure_storage.types.AccessControlFlag" separateSignature={false} />

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
