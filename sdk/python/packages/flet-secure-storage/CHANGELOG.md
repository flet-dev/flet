# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## 0.86.0

### Fixed

- Writes failing with error `-34018` on macOS apps without signing entitlements, such as during development, even with `MacOsOptions(uses_data_protection_keychain=False)`: the Flutter [`flutter_secure_storage`](https://pub.dev/packages/flutter_secure_storage) plugin is updated to 10.3.1 ([#6586](https://github.com/flet-dev/flet/issues/6586), [#6591](https://github.com/flet-dev/flet/pull/6591)) by @EH-MLS.

## 0.83.0

### Fixed

- `WebOptions` storing data under `FlutterEncryptedStorage` and `FlutterSecureStorage` instead of its documented `db_name` and `public_key` defaults, `FletEncryptedStorage` and `FletSecureStorage` ([#6329](https://github.com/flet-dev/flet/issues/6329), [#6330](https://github.com/flet-dev/flet/pull/6330)) by @FeodorFitsner.

## 0.80.3

### Added

- Initial release: a `SecureStorage` service that stores key-value data encrypted with each platform's secure storage, such as the Keychain on iOS and macOS, wrapping the Flutter [`flutter_secure_storage`](https://pub.dev/packages/flutter_secure_storage) plugin ([#6001](https://github.com/flet-dev/flet/pull/6001)) by @7576457.
