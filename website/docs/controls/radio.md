---
class_name: "flet.Radio"
examples: "controls/material/radio"
example_images: "test-images/examples/controls/material/golden/macos/radio"
title: "Radio"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Simple radio buttons" imageWidth="80%"/>

## Examples

<CodeExample path={frontMatter.examples + '/radio/main.py'} language="python" />

<Image src={frontMatter.example_images + '/basic.gif'} alt="basic" width="40%" />

<CodeExample path={frontMatter.examples + '/handling_selection_changes/main.py'} language="python" />

<Image src={frontMatter.example_images + '/handling_selection_changes.gif'} alt="handling-selection-changes" width="40%" />

<CodeExample path={frontMatter.examples + '/styled/main.py'} language="python" />

<Image src={frontMatter.example_images + '/styled.gif'} alt="styled" width="50%" />

<ClassMembers name={frontMatter.class_name} />
