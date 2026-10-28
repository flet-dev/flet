---
class_name: "flet_notifications.Notifications"
examples: "extensions/notifications"
title: "Notifications"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';
import {ClassAll, CodeExample} from '@site/src/components/crocodocs';

Show, schedule, and cancel system notifications in your [Flet](https://flet.dev) app
using the `flet-notifications` extension. It wraps Flutter's
[`flutter_local_notifications`](https://pub.dev/packages/flutter_local_notifications) package.

The notifications are local: your app posts them itself, either at once or scheduled
ahead of time, in which case the operating system delivers them even while the app isn't
running. Push notifications sent from a server, through Firebase Cloud Messaging or the
Apple Push Notification service, are not supported by this extension.

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

The extension adds the receivers that deliver
action buttons and scheduled notifications, and restore schedules after a reboot
or an app update, to your app's manifest, with the `POST_NOTIFICATIONS`,
`VIBRATE` and `RECEIVE_BOOT_COMPLETED` permissions. [`flet build`](../../cli/flet-build.md)
also enables the core library desugaring the notifications plugin requires,
through the extension's [build settings](../../extend/user-extensions.md#build-settings).

Some features need permissions only your app can decide to request:
exact schedules (see [`AndroidScheduleMode`][flet_notifications.AndroidScheduleMode]),
full-screen notifications (see [`AndroidOptions.full_screen_intent`][flet_notifications.AndroidOptions.full_screen_intent]),
and foreground services (see [`start_foreground_service()`][flet_notifications.Notifications.start_foreground_service]).

See also:

- [Android publishing guide](../../publish/android.md)
- [Android permissions](../../publish/android.md#permissions)
- [Android Resources](../../publish/android.md#resources)

### Windows

Building the app with [`flet build windows`](../../publish/windows.md) needs
Visual Studio's **C++ ATL for latest build tools** component, for the
architecture you build for. The Visual Studio Installer selects the x86 & x64
one with the [Desktop development with C++](../../publish/windows.md#visual-studio)
workload, but not in Build Tools installations, and the ARM64 one, needed on
Windows on Arm, is never selected. Without it, the build fails with
`Cannot open include file: 'atlbase.h'`. Add it in the Visual Studio Installer,
under **Modify** > **Individual components**.

### Web

The browser only accepts
[`Notification.requestPermission()`](https://developer.mozilla.org/en-US/docs/Web/API/Notification/requestPermission_static)
from a user gesture. Call
[`request_permissions()`][flet_notifications.Notifications.request_permissions]
from an [`on_click`][flet.OutlinedButton.on_click] handler before calling
[`show()`][flet_notifications.Notifications.show]. Serve the app over HTTPS
or a trusted localhost origin. If permission was denied, the user must change
the site's browser permissions before requesting again.

[`are_notifications_enabled()`][flet_notifications.Notifications.are_notifications_enabled]
checks browser permission without prompting. It returns `False` when permission
is denied, undecided, or notifications are unsupported.

Use [`WebOptions`][flet_notifications.WebOptions] to customize browser notifications.
The browser and operating system determine which presentation options are honored.
[`NotificationAction`][flet_notifications.NotificationAction] buttons are forwarded
on Web, but browser support and the number of visible buttons vary. Inline action
inputs are not supported; provide essential actions within the app as well.

## Examples

<CodeExample path={frontMatter.examples + '/basic/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/permissions/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/actions/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/scheduling/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/exact_alarms/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/progress/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/active_notifications/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/android_styles/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/channels/main.py'} language="python" />

<CodeExample path={frontMatter.examples + '/foreground_service/main.py'} language="python" />

## Description

<ClassAll name={frontMatter.class_name} />
