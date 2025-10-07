---
class_name: flet.TextField
examples: ../../examples/controls/text_field
example_images: ../test-images/examples/material/golden/macos/textfield
example_media: ../examples/controls/text_field/media
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Basic TextField") }}

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/textfield)

### Basic Example

```python
--8<-- "{{ examples }}/basic.py"
```

{{ image(example_media + "/basic.gif", alt="basic", width="80%") }}


### Handling change events

```python
--8<-- "{{ examples }}/handling_change_events.py"
```

{{ image(example_media + "/handling_change_events.gif", alt="handling-change-events", width="80%") }}


### Password with reveal button

```python
--8<-- "{{ examples }}/password.py"
```

{{ image(example_media + "/password.gif", alt="password", width="80%") }}


### Multiline fields

```python
--8<-- "{{ examples }}/multiline.py"
```

{{ image(example_media + "/multiline.gif", alt="multiline", width="80%") }}


### Underlined and borderless TextFields

```python
--8<-- "{{ examples }}/underlined_and_borderless.py"
```

{{ image(example_media + "/underlined_and_borderless.gif", alt="underlined-and-borderless", width="80%") }}


### Setting prefixes and suffixes

```python
--8<-- "{{ examples }}/prefix_and_suffix.py"
```

{{ image(example_media + "/prefix_and_suffix.gif", alt="prefix-and-suffix", width="80%") }}


### Styled TextField

```python
--8<-- "{{ examples }}/styled.py"
```

### Custom label, hint, helper, and counter texts and styles

```python
--8<-- "{{ examples }}/label_hint_helper_counter.py"
```

{{ class_members(class_name) }}
