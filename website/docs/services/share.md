---
class_name: "flet.Share"
examples: "services/share"
title: "Share"
---

import {ClassMembers, ClassSummary, CodeExample} from '@site/src/components/crocodocs';

<ClassSummary name={frontMatter.class_name} />

:::warning[Sharing from a web app]
Browsers only open the share sheet while they are handling a click or key press,
which the methods below cannot satisfy - by the time the click has reached your
Python code and the instruction has travelled back, the permission is gone.

Use a [`ShareText`](../types/sharetext.md) action instead, which the client
performs inside the original gesture. See
[Client actions](../cookbook/client-actions.md).
:::

## Sharing with a client action

<CodeExample path={frontMatter.examples + '/share_text_action/main.py'} language="python" />

## Examples

<CodeExample path={frontMatter.examples + '/share/main.py'} language="python" />

<ClassMembers name={frontMatter.class_name} />
