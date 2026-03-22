---
slug: flet-for-ios
title: Flet for iOS
authors: feodor
tags: [releases]
---

🎉 Whoo-hoo, Flet app is now on App Store! 🎉

<a href="https://apps.apple.com/app/flet/id1624979699" target="_blank"><img src="/img/blog/ios/flet-1080x1080.png" className="screenshot-50 screenshot-rounded"/></a>

With Flet iOS app you can see how your Flet Python app looks and behaves on iPhone or iPad while the app itself is running on your computer.

But it's more than just testing Flet apps on the phone! Flet mobile app itself is written in Python and its publishing to App Store is an important milestone for the entire Flet project. It is a successful proof that you can create awesome mobile apps in Python only and package them so that they are accepted in App Store!

**[Follow this guide](https://docs.flet.dev/getting-started/testing-on-mobile/)** to get started with testing your Flet apps on iPhone or iPad. Explore the app, browse gallery, play with sample projects and app settings.

I would like to thank [Kivy project](https://kivy.org/) for making a [toolchain for iOS](https://github.com/kivy/kivy-ios) which we used to compile Python interpreter and dependencies for iOS devices. We published [serious_python](https://pub.dev/packages/serious_python) package for adding Python runtime to any Flutter app.

<!-- truncate -->

## FAQ

### When Android is supported?

Soon. It has #1 priority now and we've already started working on it.

### How to package my Flet app for App Store?

We are going to provide a project template for bootstrap Flutter app and a guide how to combine Flutter, `serious_python` package and your Python app together to create a standalone iOS app and publish it to App Store.

Later this year we'll create a CI pipeline to fully automate the process.

Check [`serious_python`'s readme](https://github.com/flet-dev/serious-python#usage) for instructions on how create a Flutter bootstrap and package your Python app to run within it. Use [flet_example](https://github.com/flet-dev/serious-python/tree/main/src/serious_python/example/flet_example) project as a starting point.

## Flet v0.8.0 release notes

For testing on iOS you need to upgrade your Flet installation to v0.8.0.

It's been [changed a lot](https://github.com/flet-dev/flet/blob/main/CHANGELOG.md#080) in v0.8.0 and there were some breaking changes. Bear with us while you are upgrading to 0.8.0 and let us know if you have any troubles with it.

Enjoy!
