fastlane documentation
----

# Installation

Make sure you have the latest version of the Xcode command line tools installed:

```sh
xcode-select --install
```

For _fastlane_ installation instructions, see [Installing _fastlane_](https://docs.fastlane.tools/#installing-fastlane)

# Available Actions

## iOS

### ios update_version

```sh
[bundle exec] fastlane ios update_version
```

Update project version

### ios build_flutter

```sh
[bundle exec] fastlane ios build_flutter
```

Build Flutter without codesign

### ios config_flutter

```sh
[bundle exec] fastlane ios config_flutter
```

Configure Flutter project without building it

### ios build_ipa

```sh
[bundle exec] fastlane ios build_ipa
```

Build for internal testing

### ios upload_appstore

```sh
[bundle exec] fastlane ios upload_appstore
```

Upload to App Store

----

This README.md is auto-generated and will be re-generated every time [_fastlane_](https://fastlane.tools) is run.

More information about _fastlane_ can be found on [fastlane.tools](https://fastlane.tools).

The documentation of _fastlane_ can be found on [docs.fastlane.tools](https://docs.fastlane.tools).
