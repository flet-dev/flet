Flet provides an API for storing key-value data in user's session on a server side.

/// admonition
    type: caution
In the current Flet implementation the data stored in a session store
is transient and is not preserved between app restarts.
///

### Write data

```python
# strings
page.session.store.set("key", "value")

# numbers
page.session.store.set("number.setting", 12345)

# booleans
page.session.store.set("bool_setting", True)

# lists
page.session.store.set("favorite_colors", ["red", "green", "blue"])
```

### Read data

```python
# The value is automatically converted back to the original type
value = page.session.store.get("key")

colors = page.session.store.get("favorite_colors")
# colors = ["red", "green", "blue"]
```

### Check key existence

```python
page.session.store.contains_key("key") # True if the key exists
```

### Get all keys

```python
page.session.store.get_keys()
```

#### Remove data by key

```python
page.session.store.remove("key")
```

#### Clear all data

```python
page.session.store.clear()
```
