---
class_name: "flet.Column"
examples: "controls/core/column"
example_images: "test-images/examples/controls/core/golden/macos/column"
example_media: "examples/controls/core/column/media"
title: "Column"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Column" imageWidth="25%"/>

## Examples

<CodeExample path={frontMatter.examples + '/spacing/main.py'} language="python" />

<Image src={frontMatter.example_media + '/spacing.gif'} alt="spacing" width="55%" />

<CodeExample path={frontMatter.examples + '/wrap/main.py'} language="python" />

<Image src={frontMatter.example_media + '/wrap.gif'} alt="wrap" width="55%" />

<CodeExample path={frontMatter.examples + '/alignment/main.py'} language="python" />

<Image src={frontMatter.example_media + '/alignment.png'} alt="alignment" width="55%" />

<CodeExample path={frontMatter.examples + '/horizontal_alignment/main.py'} language="python" />

<Image src={frontMatter.example_media + '/horizontal_alignment.png'} alt="horizontal-alignment" width="40%" />

<CodeExample path={frontMatter.examples + '/infinite_scrolling/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/programmatic_scroll/main.py'} language="python" />

<Image src={frontMatter.example_media + '/programmatic_scroll.png'} alt="programmatic-scroll" width="55%" />

[//]: # (### Custom scrollbar)

<ClassMembers name={frontMatter.class_name} />
