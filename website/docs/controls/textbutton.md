---
class_name: "flet.TextButton"
examples: "controls/material/text_button"
example_images: "test-images/examples/controls/material/golden/macos/text_button"
title: "TextButton"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Simple text button" imageWidth="20%"/>

## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/textbutton)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<Image src={frontMatter.example_images + '/basic.png'} alt="basic" width="20%" />

### Icons

<CodeExample path={frontMatter.examples + '/icons/main.py'} language="python" />

<Image src={frontMatter.example_images + '/icons.png'} alt="icons" width="30%" />

### Handling clicks

<CodeExample path={frontMatter.examples + '/handling_clicks/main.py'} language="python" />

<Image src={frontMatter.example_images + '/handling_clicks.png'} alt="handling-clicks" width="30%" />

### Custom content

<CodeExample path={frontMatter.examples + '/custom_content/main.py'} language="python" />

<Image src={frontMatter.example_images + '/custom_content.png'} alt="custom-content" width="30%" />

<ClassMembers name={frontMatter.class_name} />
