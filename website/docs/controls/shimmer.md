---
class_name: "flet.Shimmer"
examples: "controls/shimmer"
example_images: "test-images/examples/core/golden/macos/shimmer"
title: "Shimmer"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.gif'} imageCaption="Basic shimmer" />

## Examples

### Basic

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<Image src={frontMatter.example_images + '/image_for_docs.gif'} alt="custom-label" width="50%" />

### Skeleton list placeholders

<CodeExample path={frontMatter.examples + '/basic_placeholder/main.py'} language="python" />

<Image src={frontMatter.example_images + '/basic_placeholder.png'} alt="custom-label" width="50%" />

### Custom gradients and directions

<CodeExample path={frontMatter.examples + '/custom_gradient/main.py'} language="python" />

<Image src={frontMatter.example_images + '/custom_gradient.png'} alt="custom-label" width="50%" />

<ClassMembers name={frontMatter.class_name} />
