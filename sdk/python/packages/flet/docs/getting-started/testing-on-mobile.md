Start building awesome mobile apps in Python using just your computer and mobile phone!

/// admonition | Important
    type: danger
- Make sure your computer fullfills [these requirements](installation.md#prerequisites).
- Your device and computer must be connected to the same Wi-Fi or local network.
- We recommend starting with the [creation of a new virtual environment](installation.md#creating-a-virtual-environment-venv).
///


/// tab | iOS

Install the [Flet iOS app](https://apps.apple.com/app/flet/id1624979699) on your iOS device.
You will be using this app to see how your Flet project is working on iPhone or iPad.

{{ image("../assets/getting-started/testing-on-mobile/ios/qr-code.jpg", alt="Get it on App Store", width="300", caption="[View on App Store](https://apps.apple.com/app/flet/id1624979699)", link="https://apps.apple.com/app/flet/id1624979699") }}


Run the following command to start Flet development server with your app:

/// tab | uv
```bash
uv run flet run --ios [script]  # (1)!
```

1. [`flet run`](../cli/flet-run.md) starts your app in hot reload mode. More info [here](running-app.md).
///
/// tab | pip
```bash
flet run --ios [script]  # (1)!
```

1. [`flet run`](../cli/flet-run.md) starts your app in hot reload mode. More info [here](running-app.md#watching-for-changes).
///
/// tab | poetry
```bash
poetry run flet run --ios [script]  # (1)!
```

1. [`flet run`](../cli/flet-run.md) starts your app in hot reload mode. More info [here](running-app.md#watching-for-changes).
///

///
/// tab | Android

Install the [Flet Android app](https://play.google.com/store/apps/details?id=com.appveyor.flet) on your Android device.
You will be using this app to see how your Flet project is working on Android device.

{{ image("../assets/getting-started/testing-on-mobile/android/google-play-badge.png", alt="Get it on Google Play", width="300", caption="[View on PlayStore](https://play.google.com/store/apps/details?id=com.appveyor.flet)", link="https://play.google.com/store/apps/details?id=com.appveyor.flet") }}


Run the following command to start Flet development server with your app:

/// tab | uv
```bash
uv run flet run --android [script]  # (1)!
```

1. [`flet run`](../cli/flet-run.md) starts your app in hot reload mode. More info [here](running-app.md).
///
/// tab | pip
```bash
flet run --android [script]  # (1)!
```

1. [`flet run`](../cli/flet-run.md) starts your app in hot reload mode. More info [here](running-app.md#watching-for-changes).
///
/// tab | poetry
```bash
poetry run flet run --android [script]  # (1)!
```

1. [`flet run`](../cli/flet-run.md) starts your app in hot reload mode. More info [here](running-app.md#watching-for-changes).
///

///

A QR code with encoded project URL will be displayed in the terminal:

{{ image("../assets/getting-started/testing-on-mobile/ios/app-qr-code.png", alt="app-qr-code", width="300") }}


Open **Camera** app on your Android device, point to QR code you got and click URL to open it in Flet app.

Try updating your `[script]` - the app will be instantly refreshed on your Android device.

To return to "Home" tab either:

* Long-press anywhere on the screen with 3 fingers or
* Shake your Android device.

You can also "manually" add a new project by clicking **"+"** floating action button in the app and typing in its URL.

/// admonition | Examples
    type: example

- Below is a URL to a "Counter" Flet app that we hosted for testing purposes:
    ```
    https://flet-counter-test-ios.fly.dev
    ```
- The "Gallery" tab of the app has some more examples that you can try out.
- Explore [Flet examples](https://github.com/flet-dev/flet/blob/main/sdk/python/examples) for even more examples.
///
