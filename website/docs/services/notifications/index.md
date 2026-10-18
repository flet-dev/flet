---
class_name: "flet_notifications.LocalNotifications"
examples: "extensions/notifications"
title: "Notifications"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {ClassAll, CodeExample} from '@site/src/components/crocodocs';

# Notifications

Show, schedule and cancel system notifications with Flutter's [`flutter_local_notifications`](https://pub.dev/packages/flutter_local_notifications) plugin.

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
|----------|---------|-------|-------|-----|---------|-----|
| Supported|    ✅    |   ✅   |   ✅   |  ✅  |    ✅    |  ✅  |

## Setup

### Android

Scheduled notifications need permissions in the app's `pyproject.toml`:

```toml
[tool.flet.android.permission]
RECEIVE_BOOT_COMPLETED = true   # restore alarms after reboot
SCHEDULE_EXACT_ALARM = true     # exact schedule modes
```

The plugin also needs its scheduled-notification receivers and the core-library-desugaring Gradle flags, which `[tool.flet.android.*]` cannot declare. Build the Android project, then inject them with the bundled `flet-notifications-patch` script:

```bash
flet build apk --yes --project myapp --org com.example -v
flet-notifications-patch --project-root build/flutter
cd build/flutter/android && ./gradlew assembleRelease -Psplit-per-abi=true
```

### Web

The browser only accepts `Notification.requestPermission()` from a user gesture. Call `request_permissions()` from an `on_click` handler. Notification action buttons work in Chrome and Edge only.

## Usage

Add `flet-notifications` to your project dependencies:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv add flet-notifications
```

</TabItem>
<TabItem value="pip" label="pip">
```bash
pip install flet-notifications  # (1)!
```

1. After this, you will have to manually add this package to your `requirements.txt` or `pyproject.toml`.
</TabItem>
</Tabs>

```python
import flet as ft
from flet_notifications import LocalNotifications


def main(page: ft.Page):
    notifications = LocalNotifications()

    async def on_tap(e):
        print("tapped:", e.payload)

    notifications.on_tap = on_tap

    async def notify(e):
        if await notifications.request_permissions():
            await notifications.show(id=1, title="Build finished", body="Android #42 succeeded")

    page.add(ft.OutlinedButton("Notify", on_click=notify))


ft.run(main)
```

The service registers itself with the page when constructed. Taps that arrive while the app was not running are replayed on the next start.

## Platform Notes

- Linux and Web have no OS scheduler, and Windows schedules one-shot notifications only.
- `cancel` and the query methods need package identity (MSIX) on Windows.
- Interruption levels beyond `passive` on Apple platforms need Xcode capabilities.

## Example

<CodeExample path={frontMatter.examples + '/notifications/main.py'} language="python" />

## Description

<ClassAll name={frontMatter.class_name} />
