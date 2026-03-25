---
class_name: "flet.Markdown"
examples: "controls/markdown"
example_images: "../test-images/examples/core/golden/macos/markdown"
example_media: "../examples/controls/markdown/media"
title: "Markdown"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic Markdown" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/displays/markdown)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic.py'} language="python" />

<Image src={frontMatter.example_media + '/basic.gif'} alt="basic" width="55%" />

### Code syntax highlight

<CodeExample path={frontMatter.examples + '/code_syntax_highlight.py'} language="python" />

<Image src={frontMatter.example_media + '/code_syntax_highlight.png'} alt="code-syntax-highlight" width="55%" />

### Custom text theme

<CodeExample path={frontMatter.examples + '/custom_text_theme.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />
