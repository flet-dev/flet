---
class_name: "flet.Markdown"
examples: "controls/core/markdown"
example_images: "test-images/examples/controls/core/golden/macos/markdown"
example_media: "examples/controls/core/markdown/media"
title: "Markdown"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Markdown" imageWidth="30%"/>

## Examples

<CodeExample path={frontMatter.examples + '/markdown/main.py'} language="python" />

<Image src={frontMatter.example_media + '/basic.gif'} alt="basic" width="55%" />

<CodeExample path={frontMatter.examples + '/code_syntax_highlight/main.py'} language="python" />

<Image src={frontMatter.example_media + '/code_syntax_highlight.png'} alt="code-syntax-highlight" width="65%" />

<CodeExample path={frontMatter.examples + '/custom_text_theme/main.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />
