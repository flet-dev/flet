---
class_name: "flet.ProgressBar"
examples: "controls/progress_bar"
example_media: "examples/controls/progress_bar/media"
example_images: "test-images/examples/material/golden/macos/progress_bar"
title: "ProgressBar"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Fixed progress bar" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/displays/progressbar)

### Determinate and indeterminate progress bars

<CodeExample path={frontMatter.examples + '/determinate_and_indeterminate/main.py'} language="python" />

<Image src={frontMatter.example_media + '/determinate_and_indeterminate.gif'} alt="determinate-and-indeterminate" width="55%" />

<ClassMembers name={frontMatter.class_name} />
