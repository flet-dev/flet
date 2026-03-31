---
class_name: "flet_code_editor.CodeEditor"
examples: "controls/code_editor"
example_images: "test-images/examples/extensions/code_editor/golden/macos/code_editor"
title: "CodeEditor"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic CodeEditor" />

## Usage

Add `flet-code-editor` to your project dependencies:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add flet-code-editor
```

</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install flet-code-editor  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
</TabItem>
</Tabs>
## Examples

### Basic example
<CodeExample path={frontMatter.examples + '/example_1.py'} language="python" />

<Image src={frontMatter.example_images + '/example_1.png'} alt="code-editor-example-1" width="55%" />

### Selection handling

<CodeExample path={frontMatter.examples + '/example_2.py'} language="python" />

<Image src={frontMatter.example_images + '/example_2.png'} alt="code-editor-example-2" width="55%" />

### Folding and initial selection

<CodeExample path={frontMatter.examples + '/example_3.py'} language="python" />

<Image src={frontMatter.example_images + '/example_3.png'} alt="code-editor-example-3" width="55%" />

<ClassMembers name={frontMatter.class_name} />
