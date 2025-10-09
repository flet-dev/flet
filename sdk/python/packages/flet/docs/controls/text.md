---
class_name: flet.Text
examples: ../../examples/controls/text
example_images: ../test-images/examples/core/golden/macos/text
example_media: ../examples/controls/text/media
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Basic Text control") }}

## Examples

[Live example](https://flet-controls-gallery.fly.dev/displays/text)

### Custom text styles

```python
--8<-- "{{ examples }}/custom_styles.py"
```

{{ image(example_media + "/custom_styles.gif", alt="custom-styles", width="80%") }}


### Pre-defined theme text styles

```python
--8<-- "{{ examples }}/text_theme_styles.py"
```

{{ image(example_media + "/text_theme_styles.png", alt="text-theme-styles", width="80%") }}


### Font with variable weight

```python
--8<-- "{{ examples }}/variable_font_weight.py"
```

{{ image(example_media + "/variable_font_weight.gif", alt="variable-font-weight", width="80%") }}


### Basic rich text example

```python
--8<-- "{{ examples }}/rich_text_basic.py"
```

{{ image(example_media + "/rich_text_basic.png", alt="rich-text-basic", width="80%") }}


### Rich text with borders and stroke

```python
--8<-- "{{ examples }}/rich_text_border_stroke.py"
```

{{ image(example_media + "/rich_text_border_stroke.png", alt="rich-text-border-stroke", width="80%") }}


### Rich text with gradient

```python
--8<-- "{{ examples }}/rich_text_gradient.py"
```

{{ image(example_media + "/rich_text_gradient.png", alt="rich-text-gradient", width="80%") }}


{{ class_members(class_name) }}
