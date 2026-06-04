---
class_name: "flet.ContextMenu"
examples: "controls/material/context_menu"
example_images: "test-images/examples/controls/material/golden/macos/context_menu"
title: "ContextMenu"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="ContextMenu" imageWidth="30%"/>

## Examples

<CodeExample path={frontMatter.examples + '/triggers/main.py'} language="python" />

<Image src={frontMatter.example_images + '/triggers_flow.gif'} width="30%" />

<CodeExample path={frontMatter.examples + '/programmatic_open/main.py'} language="python" />

<Image src={frontMatter.example_images + '/programmatic_open.png'} width="30%" />

<CodeExample path={frontMatter.examples + '/custom_trigger/main.py'} language="python" />

<Image src={frontMatter.example_images + '/custom_trigger_flow.gif'} width="30%" />

<ClassMembers name={frontMatter.class_name} />
