---
class_name: flet.Router
examples: ../../examples/apps/router
---

{{ class_summary(class_name) }}

`Router` matches the current page route against a tree of [`Route`][flet.Route] definitions
and renders the matched component chain with nested outlet contexts.

Navigation is done via [`page.push_route()`][flet.Page.push_route].

## Examples

### Basic

```python
--8<-- "{{ examples }}/basic.py"
```

### Layout with outlet

```python
--8<-- "{{ examples }}/layout_outlet.py"
```

### Dynamic segments

```python
--8<-- "{{ examples }}/dynamic_segments.py"
```

### Loaders

```python
--8<-- "{{ examples }}/loaders.py"
```

### Active links

```python
--8<-- "{{ examples }}/active_links.py"
```

### Featured

```python
--8<-- "{{ examples }}/featured.py"
```

{{ class_members(class_name) }}
