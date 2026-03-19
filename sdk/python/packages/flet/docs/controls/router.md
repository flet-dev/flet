---
class_name: flet.Router
examples: ../../examples/apps/router
---

{{ class_summary(class_name) }}

`Router` matches the current page route against a tree of [`Route`][flet.Route] definitions
and renders the matched component chain with nested outlet contexts.

Navigation is done via [`page.navigate()`][flet.Page.navigate] or [`page.push_route()`][flet.Page.push_route].

## Examples

### Basic

```python
--8<-- "{{ examples }}/basic/main.py"
```

### Layout with outlet

```python
--8<-- "{{ examples }}/layout_outlet/main.py"
```

### Dynamic segments

```python
--8<-- "{{ examples }}/dynamic_segments/main.py"
```

### Loaders

```python
--8<-- "{{ examples }}/loaders/main.py"
```

### Active links

```python
--8<-- "{{ examples }}/active_links/main.py"
```

### Featured

```python
--8<-- "{{ examples }}/featured/main.py"
```

{{ class_members(class_name) }}
