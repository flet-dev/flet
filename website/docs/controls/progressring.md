---
class_name: "flet.ProgressRing"
examples: "controls/progress_ring"
example_images: "test-images/examples/material/golden/macos/progress_ring"
example_media: "examples/controls/progress_ring/media"
title: "ProgressRing"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Fixed progress ring" imageWidth="10%"/>

## Examples

[Live example](https://flet-controls-gallery.fly.dev/displays/progressring)

### Determinate and indeterminate progress rings

<CodeExample path={frontMatter.examples + '/determinate_and_indeterminate/main.py'} language="python" />

<Image src={frontMatter.example_media + '/determinate_and_indeterminate.gif'} alt="determinate-and-indeterminate" width="40%" />

### Gauge with progress

<CodeExample path={frontMatter.examples + '/gauge_with_progress/main.py'} language="python" />

<Image src={frontMatter.example_images + '/gauge_with_progress.png'} alt="determinate-and-indeterminate" width="13%" />

<ClassMembers name={frontMatter.class_name} />
