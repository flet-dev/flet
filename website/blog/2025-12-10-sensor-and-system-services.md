---
slug: sensor-and-system-services
title: Sensor and system services
authors: feodor
tags: [news]
toc_max_heading_level: 2
---

We've just merged a [pull request](https://github.com/flet-dev/flet/pull/5846) introducing 10 new device and platform services to the Flet SDK, significantly expanding access to hardware sensors and system capabilities.

### New sensor services

* [Accelerometer](https://docs.flet.dev/services/accelerometer/) – Reads raw acceleration along the X, Y, and Z axes, including gravity.
* [Barometer](https://docs.flet.dev/services/barometer/) – Provides atmospheric pressure readings useful for altitude estimation.
* [Gyroscope](https://docs.flet.dev/services/gyroscope/) – Measures device rotation around each axis.
* [Magnetometer](https://docs.flet.dev/services/magnetometer/) – Detects magnetic field strength, commonly used for compass functionality.
* [UserAccelerometer](https://docs.flet.dev/services/useraccelerometer/) – Reports acceleration data with gravity filtered out for cleaner motion detection.

### New system services

* [Battery](https://docs.flet.dev/services/battery/) – Monitors battery level, charging state, and power source changes.
* [Connectivity](https://docs.flet.dev/services/connectivity/) – Detects network status and connection type (Wi-Fi, mobile, offline).
* [ScreenBrightness](https://docs.flet.dev/services/screenbrightness/) – Allows reading and adjusting the device screen brightness.
* [Share](https://docs.flet.dev/services/share/) – Invokes the system share sheet to share text, files, or URLs.
* [Wakelock](https://docs.flet.dev/services/wakelock/) – Prevents the device screen from dimming or sleeping while active.

<img src="/img/blog/sensors/flet-sensor-services.png" alt="Flet sensor and system services" className="screenshot screenshot-70" />

<!-- truncate -->

Sensor services mostly work on iOS and Android devices. Using them in a web app is also possible to some extent, but only under specific browser and hardware conditions.

System services are supported on all mobile and desktop platforms.

## How to test

Install the latest [Flet 0.70.0.devXYZ](https://pypi.org/project/flet/#history) pre-release.

Use the [`flet debug`](/blog/flet-debug-the-new-cli-for-testing-flet-apps-on-mobile-devices) command to run your app on a real iOS/Android device or emulator.

Testing in the Android emulator is especially convenient, as it allows you to experiment with virtually all available sensors:

<img src="/img/blog/sensors/flet-sensor-android-emulator.png" alt="Flet sensors testing in Android emulator" className="screenshot screenshot-70" />

## Services API

Previously, some services were exposed as page properties, such as `page.clipboard` or `page.shared_preferences`.

All services are now standalone and should be used by creating their own instances. For example:

```py
clipboard = ft.Clipboard()
await clipboard.set("Hello, world!")
```

or simply:

```py
await ft.Clipboard().set("Hello, world!")
```

When you create a new instance of a service, it is automatically registered within the page and disposed of when it is no longer referenced - for example, at the end of a method call.

However, if you need to assign an event handler to a service that must persist across method calls, you must keep a reference to that service to prevent it from being disposed.

In an imperative Flet app, you can use the `page.services` list, which holds service instances. For example:

```py
async def main(page: ft.Page):
    battery = ft.Battery()
    page.services.append(battery)  # need to keep a reference to the service

    async def on_state_change(e: ft.BatteryStateChangeEvent):
        print(f"State changed: {e.state}")

    battery.on_state_change = on_state_change

    ...
```

In a declarative Flet app, you can use the `use_ref` or `use_state` hook to hold a service reference. For example:

```py
import flet as ft

@ft.component
def App():
    async def on_state_change(e: ft.BatteryStateChangeEvent):
        print(f"State changed: {e.state}")

    ft.use_ref(lambda: ft.Battery(on_state_change=on_state_change))

    return ft.Text("Battery status app")

ft.run(lambda page: page.render(App))
```

That's all for today, folks! Happy Fletting!
