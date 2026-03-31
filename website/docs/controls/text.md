---
class_name: "flet.Text"
examples: "controls/text"
example_images: "test-images/examples/core/golden/macos/text"
example_media: "examples/controls/text/media"
title: "Text"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Basic Text control" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/displays/text)

### Custom text styles

<CodeExample path={frontMatter.examples + '/custom_styles/main.py'} language="python" />

<Image src={frontMatter.example_media + '/custom_styles.gif'} width="55%" />

### Pre-defined theme text styles

<CodeExample path={frontMatter.examples + '/text_theme_styles/main.py'} language="python" />

<Image src={frontMatter.example_media + '/text_theme_styles.png'} width="55%" />

### Font with variable weight

<CodeExample path={frontMatter.examples + '/variable_font_weight/main.py'} language="python" />

<Image src={frontMatter.example_media + '/variable_font_weight.gif'} width="55%" />

### Basic rich text example

<CodeExample path={frontMatter.examples + '/rich_text_basic/main.py'} language="python" />

<Image src={frontMatter.example_media + '/rich_text_basic.png'} width="55%" />

### Rich text with borders and stroke

<CodeExample path={frontMatter.examples + '/rich_text_border_stroke/main.py'} language="python" />

<Image src={frontMatter.example_media + '/rich_text_border_stroke.png'} width="55%" />

### Rich text with gradient

<CodeExample path={frontMatter.examples + '/rich_text_gradient/main.py'} language="python" />

<Image src={frontMatter.example_media + '/rich_text_gradient.png'} width="55%" />

<ClassMembers name={frontMatter.class_name} />
