---
slug: tap-into-native-android-and-ios-apis-with-Pyjnius-and-pyobjus
title: Tap into native Android and iOS APIs with Pyjnius and Pyobjus
authors: feodor
tags: [news]
---

When building mobile apps with Flet, you may need to interact directly with platform-specific APIs. Whether it’s accessing system information, managing Bluetooth devices, or working with user preferences, **Pyjnius** and **Pyobjus** by Kivy provide a seamless way to bridge Python with Java (for Android) and Objective-C (for iOS).

You can now integrate both Pyjnius and Pyobjus into your Flet apps! 🚀

<!-- truncate -->

## Pyjnius for Android

Pyjnius is a Python library for accessing Java classes using the **Java Native Interface** (JNI).

### Adding to a project

Add `pyjnius` dependency for Android builds only (other settings in `pyproject.toml` were omitted for brevity):

```toml
[project]
name = "pyjnius_demo"
version = "0.1.0"
dependencies = [
  "flet==0.27.1"
]

[tool.flet.android]
dependencies = [
  "pyjnius"
]
```

### Usage examples

Here are some example of how Pyjnius can be used in your Flet Android app.

#### Getting Android OS details

```python
from jnius import autoclass

# Get Build and Build.VERSION classes
Build = autoclass('android.os.Build')
Version = autoclass('android.os.Build$VERSION')

# Get OS details
device_model = Build.MODEL
manufacturer = Build.MANUFACTURER
brand = Build.BRAND
hardware = Build.HARDWARE
product = Build.PRODUCT
device = Build.DEVICE
os_version = Version.RELEASE
sdk_version = Version.SDK_INT
```

#### Listing Bluetooth devices

```python
from jnius import autoclass

# Get BluetoothAdapter instance
BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
bluetooth_adapter = BluetoothAdapter.getDefaultAdapter()

if bluetooth_adapter is None:
    print("Bluetooth not supported on this device")
else:
    if not bluetooth_adapter.isEnabled():
        print("Bluetooth is disabled. Please enable it.")
    else:
        print("Bluetooth is enabled.")

        # Get paired devices
        paired_devices = bluetooth_adapter.getBondedDevices()
        for device in paired_devices.toArray():
            print(f"Device Name: {device.getName()}, MAC Address: {device.getAddress()}")
```

### Accessing the Activity

App main activity instance can be retrieved with the following code:

```python
import os
from jnius import autoclass

activity_host_class = os.getenv("MAIN_ACTIVITY_HOST_CLASS_NAME")
assert activity_host_class
activity_host = autoclass(activity_host_class)
activity = activity_host.mActivity
```

Heck, you can basically call any Android API using Pyjnius - endless posibilities!

Check complete [Flet Pyjnius example](https://github.com/flet-dev/python-package-tests/tree/main/pyjnius).

For more Pyjnius examples and API refer to the [Pyjnius Documentation](https://Pyjnius.readthedocs.io/en/latest/quickstart.html).

...or just use ChatGPT (or your favorite LLM) to get more ideas and solutions! 😅

## Pyobjus for iOS

Pyobjus is a library for accessing Objective-C classes as Python classes using Objective-C runtime reflection.

### Adding to a project

Add `pyobjus` dependency for iOS builds only (other settings in `pyproject.toml` were omitted for brevity):

```toml
[project]
name = "Pyjnius"
version = "0.1.0"
dependencies = [
  "flet==0.27.1"
]

[tool.flet.ios]
dependencies = [
  "pyobjus"
]
```

### Usage examples

#### The simplest example

```python
from pyobjus import autoclass

NSString = autoclass('NSString')
text = NSString.alloc().initWithUTF8String_('Hello world')
print(text.UTF8String())
```

#### Getting OS details

```python
from pyobjus import autoclass
from pyobjus.dylib_manager import load_framework, INCLUDE

# Load Foundation framework
load_framework(INCLUDE.Foundation)

# Get NSProcessInfo instance
NSProcessInfo = autoclass('NSProcessInfo')
process_info = NSProcessInfo.processInfo()

# Retrieve OS version as a string
os_version = process_info.operatingSystemVersionString.UTF8String()

print(f"iOS Version: {os_version}")
```

#### Working with app user settings

```python
from pyobjus import autoclass, objc_str

NSUserDefaults = autoclass('NSUserDefaults')

key = "pyobjus_hello_world_key"
value = "Hello, world!"

# set key
NSUserDefaults.standardUserDefaults().setObject_forKey_(objc_str(value), objc_str(key))

# get key
ret = NSUserDefaults.standardUserDefaults().stringForKey_(objc_str(key))

assert ret.UTF8String() == value
```

Check complete [Flet Pyobjus example](https://github.com/flet-dev/python-package-tests/tree/main/pyobjus).

For more Pyobjus examples and API refer to the [Pyobjus Documentation](https://pyobjus.readthedocs.io/en/latest/quickstart.html).

## Plyer challenge

There is a [Plyer](https://github.com/kivy/plyer) project by Kivy team which uses both Pyjnius and Pyobjus under the hood.

It's not ported to Flet yet. You can either get more usage examples for [Android](https://github.com/kivy/plyer/tree/master/plyer/platforms/android) and [iOS](https://github.com/kivy/plyer/tree/master/plyer/platforms/ios) from there or help us with porting it to Flet.
