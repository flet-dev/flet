Flet provides an API for storing key-value data in user's session on a server side.

Writing data to the session:

```python
# strings
page.session.set("key", "value")

# numbers, booleans
page.session.set("number.setting", 12345)
page.session.set("bool_setting", True)

# lists
page.session.set("favorite_colors", ["red", "green", "blue"])
```

/// admonition
    type: caution
In the current Flet implementation the data stored in a session store is transient and is not preserved between app restarts.
///

Reading data:

```python
# The value is automatically converted back to the original type
value = page.session.get("key")

colors = page.session.get("favorite_colors")
# colors = ["red", "green", "blue"]
```

Check if a key exists:

```python
page.session.contains_key("key") # True if the key exists
```

Get all keys:

```python
page.session.get_keys()
```

Remove a value:

```python
page.session.remove("key")
```

Clear the session storage:

```python
page.session.clear()
```
