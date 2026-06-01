---
class_name: "flet.OutlinedButton"
examples: "controls/material/outlined_button"
example_media: "examples/controls/material/outlined_button/media"
example_images: "test-images/examples/controls/material/golden/macos/outlined_button"
title: "OutlinedButton"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Simple Outlined Button" imageWidth="25%"/>

## Examples

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<Image src={frontMatter.example_images + '/basic.png'} alt="basic" width="25%" />

<CodeExample path={frontMatter.examples + '/handling_clicks/main.py'} language="python" />

<Image src={frontMatter.example_images + '/handling_clicks.gif'} alt="handling-clicks" width="40%" />

<CodeExample path={frontMatter.examples + '/icons/main.py'} language="python" />

<Image src={frontMatter.example_images + '/icons.png'} alt="icons" width="35%" />

<CodeExample path={frontMatter.examples + '/custom_content/main.py'} language="python" />

<Image src={frontMatter.example_images + '/custom_content.png'} alt="custom-content" width="35%" />

<ClassMembers name={frontMatter.class_name} />
