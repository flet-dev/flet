---
class_name: flet.Text
examples: ../../examples/controls/text
example_images: ../test-images/examples/core/golden/macos/text
example_media: ../examples/controls/text/media
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Basic Text control") }}

## Examples

### Custom text styles

```python
--8<-- "{{ examples }}/custom_styles.py"
```

{{ demo("text/custom_styles", height="420", width="80%") }}

### Pre-defined theme text styles

```python
--8<-- "{{ examples }}/text_theme_styles.py"
```

{{ demo("text/text_theme_styles", height="420", width="80%") }}

### Font with variable weight

```python
--8<-- "{{ examples }}/variable_font_weight.py"
```

{{ demo("text/variable_font_weight", height="420", width="80%") }}

### Basic rich text example

```python
--8<-- "{{ examples }}/rich_text_basic.py"
```

{{ demo("text/rich_text_basic", height="420", width="80%") }}

### Rich text with borders and stroke

```python
--8<-- "{{ examples }}/rich_text_border_stroke.py"
```

{{ demo("text/rich_text_border_stroke", height="420", width="80%") }}

### Rich text with gradient

```python
--8<-- "{{ examples }}/rich_text_gradient.py"
```

{{ demo("text/rich_text_gradient", height="420", width="80%") }}


{{ class_members(class_name) }}
