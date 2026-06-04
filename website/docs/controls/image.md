---
class_name: "flet.Image"
examples: "controls/core/image"
example_images: "test-images/examples/controls/core/golden/macos/image"
example_media: "examples/controls/core/image/media"
title: "Image"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Image" imageWidth="10%" />

## Examples

<CodeExample path={frontMatter.examples + '/gallery/main.py'} language="python" />

<Image src={frontMatter.example_media + '/gallery.gif'} width="45%" />

<CodeExample path={frontMatter.examples + '/fade_in/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/src_base64_and_bytes/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/static_svg/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/dynamic_svg/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/lucide_icons/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/gapless_playback/main.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />
