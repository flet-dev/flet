---
slug: flet-adaptive-and-custom-controls
title: Flet adaptive UI and custom controls release
authors: feodor
tags: [releases]
---

🥰 Happy Valentine's Day lovely people! 🥰

We just released Flet 0.20.0 with the focus on:

1) Adaptive UI.
2) Extending Flet apps with 3rd-party Flutter packages.
3) New controls: [`Video`](https://docs.flet.dev/video/) (yay!), [`AudioRecorder`](https://docs.flet.dev/audio_recorder/) and a bunch of `Cupertino`-like controls. Flet now includes 97 built-in controls!

<!-- truncate -->

:::warning
Flet 0.20.0 includes a new [`Video`](https://docs.flet.dev/video/) control. While macOS and Windows already include all required media libraries to test Flet apps on Linux, the [libmpv](https://mpv.io/) package must be installed. On Ubuntu/Debian in can be installed with:

```
sudo apt install libmpv-dev mpv
```
:::

## Adaptive UI

Adaptive controls allow writing apps with a single code base which look and behave differently depending on the platform they are running on.

To the date Flet provides 11 adaptive controls. To make control adaptive you should set its `adaptive` property to `True`.

In Flet 0.20.0 we introduce `adaptive` property to all container-alike controls.
Setting `adaptive=True` on a container propagates this property to all child adaptive controls.

Page adds `design` property which enables granular control over controls design language and can have the following values: `ft.PageDesign.ADAPTIVE`, `ft.PageDesign.MATERIAL` or `ft.PageDesign.CUPERTINO`.

By setting just `page.design = ft.PageDesign.ADAPTIVE` you can make you app looking awesome on both iOS and Android devices:

<div className="row">
  <div className="col col--6" style={{textAlign: 'center'}}>
    <h3>iPhone</h3>
    <img src="/img/blog/adaptive/iphone-adaptive-app.png" className="screenshot-60" />
  </div>
  <div className="col col--6" style={{textAlign: 'center'}}>
    <h3>Android</h3>
    <img src="/img/blog/adaptive/android-adaptive-app.png" className="screenshot-60" style={{ width: '57%'}} />
  </div>  
</div>

## Integrating existing Flutter packages

Today Flet offers almost 100 controls, but, as you can imagine, not every Flutter library/widget could be added to the core Flet library and Flet team couldn't do that alone in the acceptable timeframe.

At the same time we do not want to put early adopters, who chose Flet to build their next commercial or corporate app, into a situation where their progress depends on Flet team availability and desire to implement a Flutter control they need.

In Flet 0.20.0 we re-factored Flutter core packages and identified the API that can be used by 3rd-party developers to add their own Flet controls written in Dart.

We are currently working on API docs, but you can learn now how custom Flutter packages are implemented by looking at Dart sources for [`Video`](https://github.com/flet-dev/flet/tree/main/packages/flet_video), and [`Audio`](https://github.com/flet-dev/flet/tree/main/packages/flet_audio) controls.

In short, you have to create a new Flutter package which implements and exports two methods:

```dart
void ensureInitialized();
Widget createControl(CreateControlArgs args);
```

See [`ensureInitialized()`](https://github.com/flet-dev/flet/blob/main/packages/flet_video/lib/src/create_control.dart#L16-L18) and [`createControl()`](https://github.com/flet-dev/flet/blob/main/packages/flet_video/lib/src/create_control.dart#L6-L14) implementations for `Video` control.

On Python side you create a new class inherited from `Control` (non-visual or overlay controls) or `ConstrainedControl`.

See [`Video`](https://github.com/flet-dev/flet/blob/main/sdk/python/packages/flet-core/src/flet_core/video.py#L44) class implementation in Python.

To integrate a custom Flutter package while building your Flet app with `flet build` command you can list extra packages with either `--include-packages` option or in `pubspec.yaml` file put into root of your Flet app.

## `Video` control

`Video` control is implemented in a separate Flutter package.

To build your Flet app with `Video` control add `--include-packages flet_video` to your `flet build` command, for example:

```
flet build apk --include-packages flet_video
```

Flet 0.20.0 is a relatively ["large" release](https://github.com/flet-dev/flet/blob/main/CHANGELOG.md#0200) and could break some things.

Upgrade to Flet 0.20.0, test your apps and let us know what you think by joining [Flet Discord server](https://discord.gg/dzWXP8SHG8) or creating a new thread on [Flet GitHub discussions](https://github.com/flet-dev/flet/discussions).

Enjoy!