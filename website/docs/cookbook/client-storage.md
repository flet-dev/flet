---
title: "Client Storage"
---

Flet's client storage API allows storing key-value data on a client side in a persistent storage.
Flet implementation uses [`shared_preferences`](https://pub.dev/packages/shared_preferences) Flutter package.

The actual storage mechanism depends on a platform where Flet app is running:

* Web - [Local storage](https://developer.mozilla.org/en-US/docs/Web/API/Storage).
* Desktop - JSON file.
* iOS - [NSUserDefaults](https://developer.apple.com/documentation/foundation/nsuserdefaults).
* Android - [SharedPreferences](https://developer.android.com/reference/android/content/SharedPreferences).

Client storage is provided by the [`SharedPreferences`][flet.SharedPreferences]
service. Create one and keep a reference to it for as long as you need it - a
service is unregistered once no live Python reference to it remains:

```python
import flet as ft

def main(page: ft.Page):
    prefs = ft.SharedPreferences()
```

Writing data to the storage:
```python
# strings
await prefs.set("key", "value")

# numbers, booleans
await prefs.set("number.setting", 12345)
await prefs.set("bool_setting", True)

# lists
await prefs.set("favorite_colors", ["red", "green", "blue"])
```

:::note
Each Flutter application using `shared_preferences` plugin has its own set of preferences. As the same Flet client (which is a Flutter app) is used to run UI for multiple Flet apps any values stored in one Flet application are visible/available to another Flet app running by the same user.

To distinguish one application settings from another it is recommended to use some unique prefix for all storage keys, for example `{company}.{product}.`. For example to store auth token in one app you could use `acme.one_app.auth_token` key and in another app use `acme.second_app.auth_token`.
:::

:::caution[Caution]
It is responsibility of Flet app developer to encrypt sensitive data before sending it to a client storage, so it's not read/tampered by another app or an app user.
:::

Reading data:
```python
# The value is automatically converted back to the original type
value = await prefs.get("key")

colors = await prefs.get("favorite_colors")
# colors = ["red", "green", "blue"]
```

Check if a key exists:
```python
await prefs.contains_key("key") # True if the key exists
```

Get all keys:
```python
await prefs.get_keys("key-prefix.")
```

Remove a value:
```python
await prefs.remove("key")
```

Clear the storage:
```python
await prefs.clear()
```

:::caution[Caution]
`clear()` is a dangerous function that removes all preferences of all Flet apps ever run by the same user and serves as a heads-up that permanent application data shouldn't be stored in the client storage.
:::
