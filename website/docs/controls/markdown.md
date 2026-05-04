---
class_name: "flet.Markdown"
examples: "controls/core/markdown"
example_images: "test-images/examples/controls/core/golden/macos/markdown"
example_media: "examples/controls/core/markdown/media"
title: "Markdown"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic Markdown" imageWidth="30%"/>

## Examples

[Live example](https://flet-controls-gallery.fly.dev/displays/markdown)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<Image src={frontMatter.example_media + '/basic.gif'} alt="basic" width="55%" />

### Code syntax highlight

<CodeExample path={frontMatter.examples + '/code_syntax_highlight/main.py'} language="python" />

<Image src={frontMatter.example_media + '/code_syntax_highlight.png'} alt="code-syntax-highlight" width="65%" />

### Custom text theme

<CodeExample path={frontMatter.examples + '/custom_text_theme/main.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />
