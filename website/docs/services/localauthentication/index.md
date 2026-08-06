---
class_name: "flet_local_auth.LocalAuthentication"
examples: "extensions/local_auth"
title: "LocalAuthentication"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {ClassAll, CodeExample} from '@site/src/components/crocodocs';

# Local Authentication

Authenticate users on-device with biometrics, PIN, passcode, or pattern using Flutter's [`local_auth`](https://pub.dev/packages/local_auth) package.

For storing secrets protected by biometrics, see [`SecureStorage`](../securestorage/index.md).

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ❌   |  ✅  |    ✅    |  ❌  |

## Setup

### iOS and macOS

Add a Face ID usage description using the [`biometric` permission bundle](../../publish/index.md#predefined-cross-platform-permission-bundles) or `[tool.flet.ios.info]` / `[tool.flet.macos.info]`:

```toml
[tool.flet]
permissions = ["biometric"]
```

### Android

`USE_BIOMETRIC` is declared by the `local_auth` plugin and merged automatically. Flet apps use `FlutterFragmentActivity` and an AppCompat `LaunchTheme` by default.

## Usage

Add `flet-local-auth` to your project dependencies:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add flet-local-auth
```

</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install flet-local-auth  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
</TabItem>
</Tabs>

## Example

<CodeExample path={frontMatter.examples + '/local_auth/main.py'} language="python" />

## Description

<ClassAll name={frontMatter.class_name} />
