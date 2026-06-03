---
class_name: "flet.NavigationRail"
examples: "controls/material/navigation_rail"
example_images: "test-images/examples/controls/material/golden/macos/navigation_rail"
title: "NavigationRail"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Navigation rail extended" imageWidth="12%"/>

## Examples

<CodeExample path={frontMatter.examples + '/navigation_rail/main.py'} language="python" />

<Image src={frontMatter.example_images + '/basic.png'} alt="basic" width="45%" />

<CodeExample path={'controls/material/navigation_drawer/adaptive_navigation/main.py'} language="python" />

<Image src={'test-images/examples/controls/material/golden/macos/navigation_drawer/adaptive_navigation.gif'} alt="Adaptive navigation example switching between a navigation bar and a navigation rail with an end drawer" width="55%" />

<ClassMembers name={frontMatter.class_name} />
