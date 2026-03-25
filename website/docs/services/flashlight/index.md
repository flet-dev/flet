---
class_name: "flet_flashlight.Flashlight"
examples: "../../../examples/services/flashlight"
title: "Flashlight"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {ClassAll, CodeExample} from '@site/src/components/crocodocs';

# Flashlight

Control the device torch/flashlight in your [Flet](https://flet.dev) app via the `flet-flashlight` extension, built on top of Flutter's [`flashlight`](https://pub.dev/packages/flashlight) package.

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ❌    |   ❌   |   ❌   |  ✅  |    ✅    |  ❌  |

## Usage

Add `flet-flashlight` to your project dependencies:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add flet-flashlight
```

</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install flet-flashlight  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
</TabItem>
</Tabs>
## Example

<CodeExample path={frontMatter.examples + '/example_1.py'} language="python" />

## Description

<ClassAll name={frontMatter.class_name} />
