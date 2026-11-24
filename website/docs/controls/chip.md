---
class_name: "flet.Chip"
examples: "controls/material/chip"
example_images: "test-images/examples/controls/material/golden/macos/chip"
example_media: "examples/controls/material/chip/media"
title: "Chip"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Chip" imageWidth="20%"/>

## Examples

<CodeExample path={frontMatter.examples + '/assist_chips/main.py'} language="python" />

<Image src={frontMatter.example_images + '/assist_chips.png'} alt="assist-chips" width="50%" />

<CodeExample path={frontMatter.examples + '/filter_chips/main.py'} language="python" />

<Image src={frontMatter.example_images + '/filter_chips.png'} alt="filter-chips" width="80%" />

<ClassMembers name={frontMatter.class_name} />
