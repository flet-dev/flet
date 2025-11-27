---
class_name: flet.TextField
examples: ../../examples/controls/text_field
example_images: ../test-images/examples/material/golden/macos/textfield
example_media: ../examples/controls/text_field/media
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Basic TextField") }}

## Examples

### Basic Example

```python
--8<-- "{{ examples }}/basic.py"
```

{{ demo("text_field/basic", height="420", width="80%") }}

### Handling change events

```python
--8<-- "{{ examples }}/handling_change_events.py"
```

{{ demo("text_field/handling_change_events", height="420", width="80%") }}

### Handling selection changes

```python
--8<-- "{{ examples }}/selection_change.py"
```

{{ demo("text_field/selection_change", height="420", width="80%") }}

### Password with reveal button

```python
--8<-- "{{ examples }}/password.py"
```

{{ demo("text_field/password", height="420", width="80%") }}

### Multiline fields

```python
--8<-- "{{ examples }}/multiline.py"
```

{{ demo("text_field/multiline", height="420", width="80%") }}

### Underlined and borderless TextFields

```python
--8<-- "{{ examples }}/underlined_and_borderless.py"
```

{{ demo("text_field/underlined_and_borderless", height="420", width="80%") }}

### Setting prefixes and suffixes

```python
--8<-- "{{ examples }}/prefix_and_suffix.py"
```

{{ demo("text_field/prefix_and_suffix", height="420", width="80%") }}

### Styled TextField

```python
--8<-- "{{ examples }}/styled.py"
```

{{ demo("text_field/styled", height="420", width="80%") }}

### Custom label, hint, helper, and counter texts and styles

```python
--8<-- "{{ examples }}/label_hint_helper_counter.py"
```

{{ demo("text_field/label_hint_helper_counter", height="420", width="80%") }}


{{ class_members(class_name) }}
