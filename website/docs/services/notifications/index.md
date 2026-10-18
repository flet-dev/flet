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

#### Foreground services

If you use [`LocalNotifications.start_foreground_service()`][flet_notifications.LocalNotifications.start_foreground_service],
add the native service declaration and permissions for its actual work. For a
`dataSync` service, merge these entries into your app's configuration, extending
the existing permission table from above:

<Tabs groupId="pyproject-toml">
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"] # (1)!
exported = false # (2)!
foregroundServiceType = "dataSync" # (3)!

[tool.flet.android.permission]
FOREGROUND_SERVICE = true # (4)!
FOREGROUND_SERVICE_DATA_SYNC = true # (5)!
```

1. Registers the plugin's Android service used by [`start_foreground_service()`][flet_notifications.LocalNotifications.start_foreground_service].
2. Prevents other apps from starting or binding to this service.
3. Declares data-transfer work, such as uploads, downloads, or backup. Choose a [foreground-service type](https://developer.android.com/develop/background-work/services/fgs/service-types) matching the actual work.
4. Declares the base permission needed to run foreground services.
5. Declares the type-specific permission for data-sync foreground services when targeting Android 14 or later.

</TabItem>
</Tabs>

Choose the service type and corresponding permissions for your app. A `specialUse`
service additionally needs a subtype property; use this configuration instead
of the `dataSync` example when that type applies:

<Tabs groupId="pyproject-toml">
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"] # (1)!
exported = false # (2)!
foregroundServiceType = "specialUse" # (3)!

[tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService".property]
"android.app.PROPERTY_SPECIAL_USE_FGS_SUBTYPE" = "Describe the service's actual work" # (4)!

[tool.flet.android.permission]
FOREGROUND_SERVICE = true # (5)!
FOREGROUND_SERVICE_SPECIAL_USE = true # (6)!
```

1. Registers the same plugin foreground service; use this declaration instead of the data-sync declaration.
2. Keeps the service private to the app.
3. Selects `specialUse` for qualifying foreground work not covered by another [service type](https://developer.android.com/develop/background-work/services/fgs/service-types#special-use).
4. Describes the specific work performed by the service. Replace the placeholder with your app's actual use; Android requires this property for `specialUse`.
5. Declares the base foreground-service permission.
6. Declares the type-specific permission for special-use foreground services when targeting Android 14 or later.

</TabItem>
</Tabs>

See also:

- [Android service configuration](../../publish/android.md#services)

### Web

The browser only accepts
[`Notification.requestPermission()`](https://developer.mozilla.org/en-US/docs/Web/API/Notification/requestPermission_static)
from a user gesture. Call
[`request_permissions()`][flet_notifications.LocalNotifications.request_permissions]
from an [`on_click`][flet.OutlinedButton.on_click] handler. Notification action
buttons work in Chrome and Edge only.

## Platform Notes

- Linux and Web have no OS scheduler, and Windows schedules one-shot notifications only.
- [`cancel()`][flet_notifications.LocalNotifications.cancel] and the query methods need package identity (MSIX) on Windows.
- Interruption levels beyond [`InterruptionLevel.PASSIVE`][flet_notifications.InterruptionLevel.PASSIVE] on Apple platforms need Xcode capabilities.

## Examples

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/notifications/main.py'} language="python" />

## Description

<ClassAll name={frontMatter.class_name} />
