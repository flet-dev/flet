---
class_name: "flet.SnackBar"
examples: "controls/snack_bar"
example_images: "test-images/examples/material/golden/macos/snack_bar"
snack_bar_action_class_name: "flet.SnackBarAction"
title: "SnackBar"
---

import {ClassAll, ClassMembers, ClassSummary, CodeExample, Image} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} image={frontMatter.example_images + '/image_for_docs.png'} imageCaption="Opened snack bar" />

## Examples

[Live example](https://flet-controls-gallery.fly.dev/dialogs/snackbar)

### Basic Example

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<Image src={frontMatter.example_images + '/basic.png'} alt="basic" width="55%" />

### Counter

<CodeExample path={frontMatter.examples + '/counter/main.py'} language="python" />

<Image src={frontMatter.example_images + '/snack_bar_flow.gif'} alt="Snack bar with counter" width="50%" caption="Snack bar with counter" />

### Action

<CodeExample path={frontMatter.examples + '/action/main.py'} language="python" />

<Image src={frontMatter.example_images + '/action_simple.png'} alt="Snack bar with a simple action" width="50%" caption="Snack bar with a simple action" />

<Image src={frontMatter.example_images + '/action_custom.png'} alt="Snack bar with a custom action" width="50%" caption="Snack bar with a custom action" />

<ClassMembers name={frontMatter.class_name} />

<ClassAll name={frontMatter.snack_bar_action_class_name} />
