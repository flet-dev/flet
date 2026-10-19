---
class_name: "flet_notifications.LocalNotifications"
examples: "extensions/notifications"
title: "Notifications"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {ClassAll, CodeExample} from '@site/src/components/crocodocs';

Show, schedule, and cancel system notifications in your [Flet](https://flet.dev) app
using the `flet-notifications` extension. It wraps Flutter's
[`flutter_local_notifications`](https://pub.dev/packages/flutter_local_notifications) package.

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ✅       | ✅     | ✅     | ✅   | ✅       | ✅   |

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

## Requirements

The following sections describe the configuration required for each platform.

### Android

Configure the native dependency, compile option, permissions, and receivers in
your app's `pyproject.toml` before building:

<Tabs groupId="pyproject-toml">
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.android]
gradle_dependencies = '''
coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.4")
''' # (1)!

[tool.flet.android.compile_options]
isCoreLibraryDesugaringEnabled = "true" # (2)!

[tool.flet.android.permission]
POST_NOTIFICATIONS = true # (3)!
VIBRATE = true # (4)!
RECEIVE_BOOT_COMPLETED = true # (5)!
SCHEDULE_EXACT_ALARM = true # (6)!

[tool.flet.android.receiver."com.dexterous.flutterlocalnotifications.ActionBroadcastReceiver"]
exported = false # (7)!

[tool.flet.android.receiver."com.dexterous.flutterlocalnotifications.ScheduledNotificationReceiver"]
exported = false # (8)!

[tool.flet.android.receiver."com.dexterous.flutterlocalnotifications.ScheduledNotificationBootReceiver"]
exported = false # (9)!

[[tool.flet.android.receiver."com.dexterous.flutterlocalnotifications.ScheduledNotificationBootReceiver".intent_filter]]
actions = [ # (10)!
    "android.intent.action.BOOT_COMPLETED",
    "android.intent.action.MY_PACKAGE_REPLACED",
    "android.intent.action.QUICKBOOT_POWERON",
    "com.htc.intent.action.QUICKBOOT_POWERON",
]
```

1. Adds the Java compatibility library used by the notifications plugin's scheduling implementation.
2. Enables core-library desugaring so those Java APIs work on older Android versions. The plugin requires this together with the dependency above, even if the app does not schedule notifications.
3. Allows notification permission requests on Android 13+. Request permission at runtime with [`request_permissions()`][flet_notifications.LocalNotifications.request_permissions].
4. Allows notification vibration.
5. Lets scheduled notifications be restored after a reboot.
6. Allows exact schedule modes. Omit this permission for inexact scheduling only. Use [`request_exact_alarm_permission()`][flet_notifications.LocalNotifications.request_exact_alarm_permission] to request exact-alarm access when needed.
7. Registers the receiver that handles notification action buttons and triggers [`on_action`][flet_notifications.LocalNotifications.on_action]. It is needed when using [`NotificationAction`][flet_notifications.NotificationAction]. `exported = false` keeps it private to the app.
8. Registers the receiver that delivers scheduled notifications. Include it when using [`schedule()`][flet_notifications.LocalNotifications.schedule] or [`periodically_show()`][flet_notifications.LocalNotifications.periodically_show].
9. Registers the receiver that restores scheduled notifications after reboot or app updates. A non-exported receiver can still receive the system broadcasts listed below.
10. Subscribes the boot receiver to normal boot, app replacement, and device-specific quick-boot events.
</TabItem>
</Tabs>

See also:

- [Android publishing guide](../../publish/android.md)
- [Java compile options](../../publish/android.md#java-compile-options)
- [Gradle dependencies](../../publish/android.md#gradle-dependencies)
- [Android permissions](../../publish/android.md#permissions)
- [Receiver configuration](../../publish/android.md#receivers)

### Web

The browser only accepts
[`Notification.requestPermission()`](https://developer.mozilla.org/en-US/docs/Web/API/Notification/requestPermission_static)
from a user gesture. The current bridge does not call this browser API:
[`request_permissions()`][flet_notifications.LocalNotifications.request_permissions]
currently returns `True` on Web without prompting or checking browser permission.
The upstream backend requires an existing permission grant before
[`show()`][flet_notifications.LocalNotifications.show] can succeed.

The bridge also does not forward custom notification action buttons or
[`WebOptions`][flet_notifications.WebOptions].

## Examples

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/notifications/main.py'} language="python" />

## Description

<ClassAll name={frontMatter.class_name} />
