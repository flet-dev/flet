---
class_name: "flet.Page"
examples: "../../examples/controls/page"
example_images: "../examples/controls/page/media"
title: "Page"
---

import {ClassMembers, ClassSummary, CodeExample} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} />

## Examples

### Listening to keyboard events

<CodeExample path={frontMatter.examples + '/keyboard_events.py'} language="python" />

### Mobile device orientation configuration

Shows how to lock your app to specific device orientations
(e.g., portrait up, landscape right) and listen for orientation changes on mobile devices.

<CodeExample path={frontMatter.examples + '/device_orientation.py'} language="python" />

### App exit confirmation

<CodeExample path={frontMatter.examples + '/app_exit_confirm_dialog.py'} language="python" />

### Hidden app window on startup

A Flet desktop app (Windows, macOS, or Linux) can start with its window hidden.
This lets your app perform initial setup (for example, add content, resize
or position the window) before showing it to the user.

In the example below, the window is resized and centered before becoming visible:

<CodeExample path={frontMatter.examples + '/window_hidden_on_start.py'} language="python" />

If you need this feature when packaging a desktop app using
[`flet build`](../cli/flet-build.md), see [this](../publish/index.md#hidden-app-window-on-startup).

### Toggle semantics debugger

<CodeExample path={frontMatter.examples + '/semantics_debugger.py'} language="python" />

### Get device locales

<CodeExample path={frontMatter.examples + '/device_locale.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />
