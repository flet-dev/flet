---
class_name: "flet_lottie.Lottie"
examples: "controls/core/lottie"
title: "Lottie"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {ClassAll, CodeExample} from '@site/src/components/crocodocs';

# Lottie

Render rich [Lottie](https://airbnb.design/lottie/) animations inside your [Flet](https://flet.dev) apps with a simple control.

It is backed by the [lottie](https://pub.dev/packages/lottie) Flutter package.

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅   |  ✅  |    ✅    |  ✅  |

## Usage

Add the `flet-lottie` package to your project dependencies:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add flet-lottie
```

</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install flet-lottie  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
</TabItem>
</Tabs>
## Example

<CodeExample path={frontMatter.examples + '/example_1/main.py'} language="python" />

## Description

<ClassAll name={frontMatter.class_name} />
