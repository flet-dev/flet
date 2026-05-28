---
class_name: "flet.Switch"
examples: "controls/material/switch"
example_images: "test-images/examples/controls/material/golden/macos/switch"
title: "Switch"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Switch" imageWidth="20%"/>

## Examples

### Switch

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<Image src={frontMatter.example_images + '/basic.png'} alt="basic" width="40%" />

### Handling change events

<CodeExample path={frontMatter.examples + '/handling_events/main.py'} language="python" />

<Image src={frontMatter.example_images + '/handling_events.gif'} alt="handling-events" width="40%" />

<ClassMembers name={frontMatter.class_name} />
