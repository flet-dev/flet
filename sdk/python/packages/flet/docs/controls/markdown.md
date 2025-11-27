---
class_name: flet.Markdown
examples: ../../examples/controls/markdown
example_images: ../test-images/examples/core/golden/macos/markdown
example_media: ../examples/controls/markdown/media
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Basic Markdown") }}

## Examples

### Basic Example

```python
--8<-- "{{ examples }}/basic.py"
```

{{ demo("markdown/basic", height="420", width="80%") }}

### Code syntax highlight

```python
--8<-- "{{ examples }}/code_syntax_highlight.py"
```

{{ demo("markdown/code_syntax_highlight", height="420", width="80%") }}

### Custom text theme

```python
--8<-- "{{ examples }}/custom_text_theme.py"
```

{{ demo("markdown/custom_text_theme", height="420", width="80%") }}


{{ class_members(class_name) }}
