---
class_name: "flet.Tabs"
examples: "controls/material/tabs"
example_images: "test-images/examples/controls/material/golden/macos/tabs"
example_media: "examples/controls/material/tabs/media"
title: "Tabs"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Tabs" imageWidth="70%"/>

## Examples

<CodeExample path={frontMatter.examples + '/tabs/main.py'} language="python" />

<Image src={frontMatter.example_media + '/basic.gif'} width="55%" />

<CodeExample path={frontMatter.examples + '/nested/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/dynamic_tab_addition/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/custom_indicator/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/move_to/main.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />
