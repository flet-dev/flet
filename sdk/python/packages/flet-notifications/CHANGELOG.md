# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## 1.1.3

### Fixed

- The "Action buttons and replies" example's notification staying stuck with a spinner after an inline reply on Android; `NotificationActionInput` and `NotificationAction.cancel_notification` now document how to update a notification after a reply ([#7058](https://github.com/flet-dev/flet/discussions/7058), [#7060](https://github.com/flet-dev/flet/pull/7060)) by @ItsRenjiii.

## 1.1.0

### Added

- Initial release: a `Notifications` service that shows, schedules and cancels local notifications on Android, iOS, macOS, Windows, Linux and Web, wrapping the [`flutter_local_notifications`](https://pub.dev/packages/flutter_local_notifications) plugin, with permission requests, Android channels, rich styles, inline-reply actions and typed tap and action handlers ([#6948](https://github.com/flet-dev/flet/issues/6948), [#6999](https://github.com/flet-dev/flet/pull/6999)) by @Nwokike.
