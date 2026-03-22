---
slug: flet-for-android
title: Flet for Android
authors: feodor
tags: [releases]
---

🤖 Android support is here!

<a href="https://play.google.com/store/apps/details?id=com.appveyor.flet" target="_blank"><img src="/img/docs/getting-started/testing-on-android/google-play-badge.png" className="screenshot-40" /></a>

With Flet Android app you can see how your Flet Python app looks and behaves on Android devices while the app itself is running on your computer.

Similar to iOS, Flet for Android is a Flutter app written entirely in Python with the help of two open-source packages: [`serious_python`](https://pub.dev/packages/serious_python) and [`flet`](https://pub.dev/packages/flet). Resulting app package is technically compliant with Google Play requirements, so you can publish awesome Android apps in pure Python.

**[Follow this guide](https://docs.flet.dev/getting-started/testing-on-mobile/)** to get started with testing your Flet apps on Android. Explore the app, browse gallery, play with sample projects and app settings.

<!-- truncate -->

## FAQ

### How to package my Flet app for Google Play?

We are going to provide a project template for bootstrap Flutter app and a guide how to combine Flutter, `serious_python` package and your Python app together to create a standalone Android app and publish it to Google Play.

Check [`serious_python`'s readme](https://github.com/flet-dev/serious-python#usage) for instructions on how create a Flutter bootstrap and package your Python app to run within it. Use [flet_example](https://github.com/flet-dev/serious-python/tree/main/example/flet_example) project as a starting point.

### Will you provide packaging for Windows, macOS and Linux?

Yes! At the moment Flet desktop apps are packaged with `flet pack` command and PyInstaller. Produced app bundle adds performance and size overhead and is hard to customize, so we are going to replace it with native Flutter packaging.

## Flet v0.9.0 release notes

For testing on Android you need to upgrade your Flet installation to v0.9.0.

There were [a few changes](https://github.com/flet-dev/flet/blob/main/CHANGELOG.md#090) mainly to support Android in Flet CLI. Let us know if you notice something unusual.

Enjoy!