---
class_name: "flet.Page"
examples: "controls/core/page"
example_images: "examples/controls/core/page/media"
title: "Page"
---

import {ClassMembers, ClassSummary, CodeExample} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} />

## Examples

<CodeExample path={frontMatter.examples + '/keyboard_events/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/device_orientation/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/app_exit_confirm_dialog/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/window_hidden_on_start/main.py'} language="python" />

If you need this feature when packaging a desktop app using
[`flet build`](../cli/flet-build.md), see [this](../publish/index.md#hidden-app-window-on-startup).

<CodeExample path={frontMatter.examples + '/semantics_debugger/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/device_locale/main.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />
