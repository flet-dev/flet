---
class_name: "flet.Clipboard"
examples: "services/clipboard"
title: "Clipboard"
---

import {ClassMembers, ClassSummary, CodeExample} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} />

:::warning[Copying in a web app]
Browsers only let a page write to the clipboard while they are handling a click
or key press, and calling [`set()`](clipboard.md#flet.Clipboard.set) from an
event handler is already too late - the click has travelled to your Python code
and back. Safari refuses silently; Chrome and Firefox are more forgiving, so the
same app often works everywhere except on iPhone and iPad.

Use a [`CopyToClipboard`](../types/copytoclipboard.md) action instead, which the
client performs inside the original gesture. See
[Client actions](../cookbook/client-actions.md).
:::

## Copying with a client action

<CodeExample path={frontMatter.examples + '/copy_action/main.py'} language="python" />

## Examples

<CodeExample path={frontMatter.examples + '/text/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/images/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/files/main.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />
