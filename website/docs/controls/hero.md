---
class_name: "flet.Hero"
examples: "controls/hero"
example_images: "test-images/examples/core/golden/macos/hero"
title: "Hero"
---

import {ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} />

## Examples

### Basic Example

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<Image src={frontMatter.example_images + '/basic.gif'} width="55%" />

### Gallery

<CodeExample path={frontMatter.examples + '/gallery/main.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />
