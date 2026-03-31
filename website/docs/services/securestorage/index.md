---
class_name: "flet_secure_storage.SecureStorage"
examples: "services/secure_storage"
title: "SecureStorage"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {ClassAll, CodeExample} from '@site/src/components/crocodocs';

# Secure Storage

A service for safely storing sensitive key–value data using the platform’s native secure storage mechanisms—Keychain on iOS/macOS, Windows Credential Manager, libsecret on Linux, and Keystore on Android.

Powered by Flutter's [`flutter_secure_storage`](https://pub.dev/packages/flutter_secure_storage) package.

:::note
You need `libsecret-1-dev` on your machine to build the project, and `libsecret-1-0` to run the application (add it as a dependency after packaging your app). If you using snapcraft to build the project use the following.

Apart from `libsecret` you also need a keyring service, for that you need either [`gnome-keyring`](https://wiki.gnome.org/Projects/GnomeKeyring) (for Gnome users) or [`kwalletmanager`](https://wiki.archlinux.org/title/KDE_Wallet) (for KDE users) or other light provider like [`secret-service`](https://github.com/yousefvand/secret-service).

```bash
sudo apt-get install libsecret-1-dev libsecret-1-0
```
:::

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅   |  ✅  |    ✅    |  ✅  |

## Usage

Add `flet-secure-storage` to your project dependencies:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add flet-secure-storage
```

</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install flet-secure-storage  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
</TabItem>
</Tabs>
## Example

<CodeExample path={frontMatter.examples + '/basic.py'} language="python" />

## Description

<ClassAll name={frontMatter.class_name} />
