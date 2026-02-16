---
class_name: flet_code_editor.CodeEditor
examples: ../../examples/controls/code_editor
example_images: ../test-images/examples/extensions/code_editor/golden/macos/code_editor
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Basic CodeEditor") }}

## Usage

Add `flet-code-editor` to your project dependencies:

/// tab | uv
```bash
uv add flet-code-editor
```

///
/// tab | pip
```bash
pip install flet-code-editor  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
///

## Examples

### Basic example
```python
--8<-- "{{ examples }}/example_1.py"
```

{{ image(example_images + "/example_1.png", alt="code-editor-example-1", width="80%") }}

### Selection handling

```python
--8<-- "{{ examples }}/example_2.py"
```

{{ image(example_images + "/example_2.png", alt="code-editor-example-2", width="80%") }}

### Folding and initial selection

```python
--8<-- "{{ examples }}/example_3.py"
```

{{ image(example_images + "/example_3.png", alt="code-editor-example-3", width="80%") }}

{{ class_members(class_name) }}
