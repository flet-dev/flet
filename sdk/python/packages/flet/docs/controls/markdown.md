---
class_name: flet.Markdown
examples: ../../examples/controls/markdown
example_images: ../test-images/examples/core/golden/macos/markdown
example_media: ../examples/controls/markdown/media
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Basic Markdown") }}

## Examples

[Live example](https://flet-controls-gallery.fly.dev/displays/markdown)

### Basic Example

```python
--8<-- "{{ examples }}/basic.py"
```

{{ image(example_media + "/basic.gif", alt="basic", width="80%") }}


### Code syntax highlight

```python
--8<-- "{{ examples }}/code_syntax_highlight.py"
```

{{ image(example_media + "/code_syntax_highlight.png", alt="code-syntax-highlight", width="80%") }}


### Custom text theme

```python
--8<-- "{{ examples }}/custom_text_theme.py"
```

{{ class_members(class_name) }}
