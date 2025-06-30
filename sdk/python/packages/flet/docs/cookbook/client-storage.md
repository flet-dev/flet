---
title: Client storage
sidebar_label: Client storage
---

Flet's client storage API allows storing key-value data on a client side in a persistent storage. 
Flet implementation uses [`shared_preferences`](https://pub.dev/packages/shared_preferences) Flutter package.

The actual storage mechanism depends on a platform where Flet app is running:

* Web - [Local storage](https://developer.mozilla.org/en-US/docs/Web/API/Storage).
* Desktop - JSON file.
* iOS - [NSUserDefaults](https://developer.apple.com/documentation/foundation/nsuserdefaults).
* Android - [SharedPreferences](https://developer.android.com/reference/android/content/SharedPreferences).

Writing data to the storage:
```python
# strings
page.client_storage.set("key", "value")

# numbers, booleans
page.client_storage.set("number.setting", 12345)
page.client_storage.set("bool_setting", True)

# lists
page.client_storage.set("favorite_colors", ["red", "green", "blue"])
```

/// admonition
    type: note
Each Flutter application using `shared_preferences` plugin has its own set of preferences. As the same Flet client (which is a Flutter app) is used to run UI for multiple Flet apps any values stored in one Flet application are visible/available to another Flet app running by the same user.

To distinguish one application settings from another it is recommended to use some unique prefix for all storage keys, for example `{company}.{product}.`. For example to store auth token in one app you could use `acme.one_app.auth_token` key and in another app use `acme.second_app.auth_token`.
///

/// admonition | Caution
    type: caution
It is responsibility of Flet app developer to encrypt sensitive data before sending it to a client storage, so it's not read/tampered by another app or an app user.
///

Reading data:
```python
# The value is automatically converted back to the original type
value = page.client_storage.get("key")

colors = page.client_storage.get("favorite_colors")
# colors = ["red", "green", "blue"]
```

Check if a key exists:
```python
page.client_storage.contains_key("key") # True if the key exists
```

Get all keys:
```python
page.client_storage.get_keys("key-prefix.")
```

Remove a value:
```python
page.client_storage.remove("key")
```

Clear the storage:
```python
page.client_storage.clear()
```

/// admonition | Caution
    type: caution
`clear()` is a dangerous function that removes all preferences of all Flet apps ever run by the same user and serves as a heads-up that permanent application data shouldn't be stored in the client storage.
///
