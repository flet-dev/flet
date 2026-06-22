---
class_name: "flet.TextField"
examples: "controls/material/text_field"
example_images: "test-images/examples/controls/material/golden/macos/textfield"
example_media: "examples/controls/material/text_field/media"
title: "TextField"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="TextField" imageWidth="30%"/>

## Examples

<CodeExample path={frontMatter.examples + '/text_field/main.py'} language="python" />

<Image src={frontMatter.example_images + '/basic.png'} alt="basic" width="30%" />

<CodeExample path={frontMatter.examples + '/handling_change_events/main.py'} language="python" />

<Image src={frontMatter.example_images + '/handling_change_events.gif'} alt="handling-change-events" width="55%" />

<CodeExample path={frontMatter.examples + '/selection_change/main.py'} language="python" />

<Image src={frontMatter.example_images + '/selection_change.gif'} alt="selection-change" width="65%" />

<CodeExample path={frontMatter.examples + '/password/main.py'} language="python" />

<Image src={frontMatter.example_images + '/password.gif'} alt="password" width="45%" />

<CodeExample path={frontMatter.examples + '/multiline/main.py'} language="python" />

<Image src={frontMatter.example_images + '/multiline.gif'} alt="multiline" width="55%" />

<CodeExample path={frontMatter.examples + '/underlined_and_borderless/main.py'} language="python" />

<Image src={frontMatter.example_images + '/underlined_and_borderless.gif'} alt="underlined-and-borderless" width="55%" />

<CodeExample path={frontMatter.examples + '/prefix_and_suffix/main.py'} language="python" />

<Image src={frontMatter.example_images + '/prefix_and_suffix.gif'} alt="prefix-and-suffix" width="55%" />

<CodeExample path={frontMatter.examples + '/styled/main.py'} language="python" />

<Image src={frontMatter.example_images + '/styled.gif'} alt="styled" width="45%" />

<CodeExample path={frontMatter.examples + '/label_hint_helper_counter/main.py'} language="python" />

<Image src={frontMatter.example_images + '/label_hint_helper_counter.gif'} alt="label-hint-helper-counter" width="55%" />

<ClassMembers name={frontMatter.class_name} />
