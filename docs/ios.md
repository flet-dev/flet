# Building and publishing iOS Flutter app on AppVeyor

## Ruby

Ensure you have a proper Ruby installed:

```
ruby --version
```

## Installing Fastlane

Switch to `<flutter-app-root>/ios` directory:

```
cd ios
```

Create `Gemfile` with the following contents:

```
source "https://rubygems.org"

gem "cocoapods"
gem "fastlane"
```

Append the following line to `.gitignore`:

```
vendor/
```

Run the following command to install Fastlane and Cocoapods:

```
bundle install --path vendor/bundle
```

`Gemfile.lock` must be checked into repository - that will ensure you have the same versions in CD environment.

Always run Fastlane with `bundle exec fastlane <args>` command. Let's check the version of installed Fastlane:

```
bundle exec fastlane --version
```

Every time you need to update Fastlane to the latest version run:

```
bundle update fastlane
```

Init Fastlane by running:

```
bundle exec fastlane init
```

A new `fastlane` directory will be create with two files in it:

* `Appfile` - the information about your app, such as `app_identifier`.
* `Fastfile` - file with build targets or "lanes".

Update `Appfile` and change `app_identifier` with your App's ID, e.g. `com.{your-company}.{your-product}`.

Leave the contents of `Fastfile` as is for now.

## Configuring Match on your machine

[Match](https://docs.fastlane.tools/actions/match/) is Fastlane action for synchronizing iOS/macOS certificates and provisioning profiles between development environments.

With Match you maintain just the details to access configured Match storage and Match passphrase used to encrypt the contents of that storage. At the time of writing Match supports the following storages:

* Git repo
* GitHub repo
* Amazon S3
* Google Cloud Storage

In this guide we use GitHub repository to store certificates and provisioning profiles.

Create a new **PRIVATE** GitHub (or your favorite source control provider) repository named `fastlane-match` (or choose your name).

To init Match run:

```
bundle exec fastlane match init
```

and follow the wizard. You'll be asked for "passphrase" to encrypt/decrypt the contents of Git repo. Make sure you remember that passphrase - you'll need it later for setting up CD process.

A new `Matchfile` will be created inside `Fastlane` directory.

Generate "development" (used to test the app on your machine only) certificates and provisioning profiles by running:

```
bundle exec fastlane match development
```

Generate "ad-hoc" (for internal testing within your team without using XCode) certificates and profiles:

```
bundle exec fastlane match adhoc
```

More about internal distribution [here](https://help.apple.com/xcode/mac/current/#/dev7ccaf4d3c).

Finally, generate "appstore" (for distributing via TestFlight and App Store) certificates and profiles:

```
bundle exec fastlane match appstore
```

Check the contents of Git repo - you should see two folders there: `certs` and `profiles`.

Open "Keychain access" application, choose "login" keychain and click "My certificates" tab - those certificates were installed by Match. This is, if you ever need that, the place where you can export your signing certificates in `.p12` format (including private key).

## Configuring iOS project

You are still in `ios` directory.

Open XCode project by running:

```
open Runner.xcodeproj
```

Select "Runner" in the left project tree, then "Signing and Capabilities" tab.

Uncheck "Automatically mamage signing".

Update "Bundle identifier" and choose "match Development {identifier}" as "Provisioning profile":

[SCREENSHOT]

Ensure you can build a project without signing with:

```
flutter build ios --release --no-codesign
```

### Complying with Encryption Export Regulations

If your app is compliant with [US cryptography export laws](https://developer.apple.com/documentation/security/complying_with_encryption_export_regulations) you can avoid a warning in App Store by adding the following lines at the bottom of `<dict>` section in `Runner/Info.plist` file:

```
<key>ITSAppUsesNonExemptEncryption</key>
<false/>
```

Open "Runner -> Runner -> Info.plist" in the left tree and make sure "App Uses Non-Exempt Encryption" contains "NO" value:

[SCREENSHOT]

## Configuring CI/CD

### Testing Fastlane locally

```
bundle exec fastlane build_ipa
```