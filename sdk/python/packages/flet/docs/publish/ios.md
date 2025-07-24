---
title: Packaging app for iOS
---

Flet CLI provides `flet build ipa` command that allows packaging
Flet app into an iOS archive bundle and IPA for distribution.

/// admonition | Note
The command can be run on macOS only.
///

/// admonition | Important
    type: danger
## Prerequisites

### Rosetta 2

[Flutter](https://flutter.dev), which we use for packaging,
requires [Rosetta 2](https://support.apple.com/en-us/HT211861) on Apple Silicon:
```
sudo softwareupdate --install-rosetta --agree-to-license
```

### Xcode

[Xcode](https://developer.apple.com/xcode/) 15 or later to compile native Swift or ObjectiveC code.

### CocoaPods

[CocoaPods](https://cocoapods.org/) 1.16 to compile and enable Flutter plugins.

### iOS wheels for binary Python packages

Binary Python packages (vs "pure" Python packages written in Python only)
are packages that partially written in C, Rust or other languages producing native code.
Example packages are `numpy`, `cryptography`, or `pydantic-core`.

Make sure all non-pure (binary) packages used in your Flet app have
[pre-built wheels for iOS](../contributing/binary-packages-android-ios.md).
///

## `flet build ipa`

Build an iOS app archive (`.ipa`) for testing and distribution (macOS host only).

To generate an `.ipa `file for testing on your device or uploading to App Store Connect
for distribution, you will need:

- [**Apple Developer Program**](https://developer.apple.com/programs/) subscription with access to [App Store Connect](https://appstoreconnect.apple.com/).
- **Application Indentifier**
- **Signing Certificate**
- **Provisioning Profile**

## Application Identifier

An **Application Identifier (App ID)** is a unique string that identifies your app within the Apple ecosystem.
It is required to sign and distribute an iOS app and is used for various services like
**Push Notifications, App Groups, iCloud, and In-App Purchases**.

An App ID consists of two parts:

1. **Team ID**: A unique 10-character string assigned by Apple to your developer account.
2. **Bundle ID**: A reverse domain-style identifier for your app (e.g., `com.example.myapp`).

Example of a full App ID:

```
TeamID.com.example.myapp
```

### Creating a new App ID

1. Visit [Apple Developer Portal](https://developer.apple.com/account/resources/identifiers/list).
2. Sign in with your **Apple Developer Account**.
3. Click the **"+"** button to add a new identifier.
4. Select **"App IDs"** and click **Continue**.
5. **Enter a Description** – This is just for reference (e.g., "MyApp Identifier").
6. **Choose the App ID Type:**
   - Select **"App"** for a standard iOS/macOS app.
   - If you need an identifier for services like Apple Pay or Passbook, select the appropriate option.
7. **Bundle ID** – Choose:
   - **Explicit Bundle ID** (`com.example.myapp`) – Recommended for most apps.
   - **Wildcard Bundle ID** (`com.example.*`) – Allows multiple apps to use the same identifier (rarely used).
8. **Enable App Services** – Check the boxes for any services your app needs (e.g., Push Notifications, Sign in with Apple, etc.).
9. Click **Continue** and **Register**.

Now you have **Bundle ID** and **Team ID** that must be used to sign iOS bundle.

The next step is creating a **Certificate** and a **Provisioning Profile** to install and distribute your app.

## Signing Certificate

### Generating a Certificate Signing Request (CSR)

Before creating a development or distribution certificate, you need a **CSR (Certificate Signing Request)**.

1. **Open Keychain Access** on your Mac (++cmd+space++, then search for "Keychain Access").
2. In the top menu, go to **Keychain Access → Certificate Assistant → Request a Certificate From a Certificate Authority…**
3. Fill in:
   - **User Email Address:** Your Apple Developer email.
   - **Common Name:** A descriptive name (e.g., "My App Distribution").
   - **CA Email Address:** Leave this blank.
   - **Request is for:** Select "**Saved to disk**".
4. Click **Continue**, choose a location to save the `.certSigningRequest` file, and click **Save**.

### Creating a Certificate in Apple Developer Portal

1. Go to [Apple Developer Certificates Page](https://developer.apple.com/account/resources/certificates/list).
2. Click the **"+"** button to create a new certificate.
3. Select **"Apple Distribution"** (for App Store & Ad Hoc) or **"Apple Development"**
   (for development) and click **Continue**.
4. Upload the **CSR file** you created earlier and click **Continue**.
5. Apple will generate the certificate. Click **Download** to get the `.cer` file.
6. Double-click the downloaded `.cer` file to install it in **Keychain Access**.
7. Open **Keychain Access** app and ensure the certificate is installed under **"login"** keychain.
   The name of development certificate usually starts with **"Apple development:"** and the name of
   distribution certificate starts with **"Apple distribution:"**.

## Provisioning Profile

A **Provisioning Profile** is a file that allows an iOS app to run on physical devices and be
distributed through the App Store or internally. It links your **App ID**,
**Developer/Distribution Certificate**, and **Registered Devices**.

There are different types of provisioning profiles:

- **Development Profile** – Used for testing on physical devices.
- **Ad Hoc Profile** – Used for distributing an app outside the App Store to specific devices.
- **App Store Profile** – Used for submitting an app to the App Store.
- **Enterprise Profile** – Used for internal distribution within an organization.

### Creating a new Provisioning Profile

**Step 1: Go to Apple Developer Portal**

1. Visit [Apple Developer Portal](https://developer.apple.com/account/resources/profiles/list).
2. Sign in with your **Apple Developer Account**.

**Step 2: Create a New Provisioning Profile**

1. Click the **"+"** button to add a new provisioning profile.
2. Choose the **type of profile**:
   - Select **"iOS App Development"** for testing on devices.
   - Select **"Ad Hoc"** for distributing to specific devices.
   - Select **"App Store"** for submitting an app to the App Store.
   - Select **"In-House"** (Enterprise accounts only) for internal distribution.
3. Click **Continue**.

**Step 3: Select an App ID**

1. Choose the **App ID** that matches your app.
2. Click **Continue**.

**Step 4: Select a Distribution Certificate**

1. Choose the **iOS Distribution Certificate** or **Development Certificate** (depending on the profile type).
2. Click **Continue**.

**Step 5: Select Registered Devices (For Development & Ad Hoc)**

1. If you selected **Development** or **Ad Hoc**, choose the devices that can run the app.
2. Click **Continue**.

**Step 6: Name and Generate the Profile**

1. Enter a **Profile Name** (e.g., "MyApp Development Profile").
2. Click **Generate**.
3. Click **Download** to get the `.mobileprovision` file.

### Installing Provisioning Profile

Provisioning profiles are stored in `~/Library/MobileDevice/Provisioning Profiles` directory.

To install downloaded provisioning profile just copy it to `~/Library/MobileDevice/Provisioning\ Profiles`
directory with a new `{UUID}.mobileprovision` name.

Run the following command to get profile UUID:

```bash
profile_uuid=$(security cms -D -i ~/Downloads/{profile-name}.mobileprovision | xmllint --xpath "string(//key[.='UUID']/following-sibling::string[1])" -)
echo $profile_uuid
```

Run this command to copy profile to `~/Library/MobileDevice/Provisioning Profiles` with a new name `{UUID}.mobileprovision`:

```bash
cp ~/Downloads/{profile-name}.mobileprovision ~/Library/MobileDevice/Provisioning\ Profiles/${profile_uuid}.mobileprovision
```

/// admonition | Note
If the copied profile disappears from the `~/Library/MobileDevice/Provisioning Profiles` directory,
ensure that the Xcode process is not running in the background.
///

Finally, you can use this command to list all installed provisioning profiles, with their names and UUIDs:

```bash
for profile in ~/Library/MobileDevice/Provisioning\ Profiles/*.mobileprovision; do security cms -D -i "$profile" | grep -E -A1 '<key>(Name|UUID)</key>' | sed -n 's/.*<string>\(.*\)<\/string>/\1/p' | paste -d ' | ' - -; done
```

## Configuring build

To can either pass .ipa build options in the `pyproject.toml` or via `flet build` command line.

### Command line

To successfully generate "runnable" IPA you should provide correct values for the following arguments:

/// admonition | Development package
To build `.ipa` for testing on your developer device you need to provide `--ios-provisioning-profile` option only. `flet build` will assume `debugging` as an export method and automatically choose the most recent "Apple Development" certificate in your keychain. Team ID is not required.
///

/// admonition | Bundle ID or Org?
    type: info
You can specify either `--bundle-id`, `--org`, or both.

* If only the `--bundle-id` is provided and `--org` is not, the organization name is derived from the bundle ID by extracting the part before the last dot.
* If only `--org` is specified and the `--bundle-id` is not, the bundle ID is generated as `{org}.{project_name}`.
///

### Signing certificate

The certificate name, SHA-1 hash, or automatic selector to use for signing iOS app bundle.
Automatic selectors allow Xcode to pick the newest installed certificate of a particular type.

The available automatic selectors are `"Apple Development"`, `"Apple Distribution"`,
`"Developer ID Application"`, `"iOS Developer"`, `"iOS Distribution"`, `"Mac App Distribution"`,
and `"Mac Developer"`.

/// tab | `pyproject.toml`

/// tab | `[tool.flet.ios]`
```toml
[tool.flet.ios]
signing_certificate = "Apple Distribution"
```
///

///
/// tab | `flet build`
```bash
flet build --ios-signing-certificate "Apple Distribution"
```
///

### Team ID

The developer team ID to export iOS app.

/// tab | `pyproject.toml`

/// tab | `[tool.flet.ios]`
```toml
[tool.flet.ios]
team_id = "ABCDEFE234"
```
///

///
/// tab | `flet build`
```bash
flet build --ios-team-id ABCDEFE234
```
///

### Provisioning profile

The provisioning profile name or UUID that used to sign and export the iOS app.

/// tab | `pyproject.toml`

/// tab | `[tool.flet.ios]`
```toml
[tool.flet.ios]
provisioning_profile = "release-testing com.mycompany.example-app"
```
///

///
/// tab | `flet build`
```bash
flet build --ios-provisioning-profile "release-testing com.mycompany.example-app"
```
///

### Project name

The project name in C-style identifier format (lowercase alphanumerics with underscores).
It is used to build [bundle ID](#bundle-id) and as a name for bundle executable.

**Default:** the name of your Flet project directory

/// tab | `pyproject.toml`

/// tab | `[tool.flet]`
```toml
[tool.flet]
project = "my-app"
```
///

///
/// tab | `flet build`
```bash
flet build --project my-app
```
///

### Organization name

The organization name in reverse domain name notation, typically in the form `com.mycompany`.

If the [bundle ID](#bundle-id) is not explicitly specified, the value of the organization name
is combined with the [project name](#project-name) to form it.

**Default:** `"com.flet"`

/// tab | `pyproject.toml`

/// tab | `[tool.flet]`
```toml
[tool.flet]
org = "com.mycompany"
```
///

///
/// tab | `flet build`
```bash
flet build --org com.mycompany
```
///

### Bundle ID

The bundle ID for the application, typically in the form `"com.mycompany.app-name"`.

If not explicitly specified, it is formed by combining the [organization name](#organization-name)
and the [project name](#project-name).

**Default:** `"[organization-name](#organization-name).[project-name](#project-name)"`

/// tab | `pyproject.toml`

/// tab | `[tool.flet]`
```toml
[tool.flet]
bundle_id = "com.mycompany.example-app"
```
///
/// tab | `[tool.flet.ios]`
```toml
[tool.flet.ios]
bundle_id = "com.mycompany.example-app-ios"
```
///

///
/// tab | `flet build`
```bash
flet build --bundle-id com.mycompany.example-app
```
///

### Export options

/// tab | `pyproject.toml`

/// tab | `[tool.flet.ios]`
```toml
[tool.flet.ios]
export_options = { uploadSymbols = false }
```
///

///

### Export method

Defines how the app should be packaged when exporting the `.ipa` file.

Can be one of the following:

- `"debugging"` (or deprecated `"development"`): used for debugging and testing on development devices.
- `"release-testing"` (or deprecated `"ad-hoc"`): used for distributing the app outside the App Store to specific registered devices.
- `"app-store-connect"` (or deprecated `"app-store"`): used for submitting the app to the App Store.
- `"enterprise"`: used for internal distribution within an organization (requires an enterprise account).

To configure build settings for one or more export methods, see [export methods](#export-methods).

**Default:** `"debugging"`

/// tab | `pyproject.toml`

/// tab | `[tool.flet.ios]`
```toml
[tool.flet.ios]
export_method = "debugging"
```
///

///
/// tab | `flet build`
```bash
flet build --ios-export-method debugging
```
///

### Export methods

Configure signing settings per export methods.

/// tab | `pyproject.toml`

/// tab | `[tool.flet.ios.export_methods."EXPORT_METHOD"]`
```toml
[tool.flet.ios.export_methods."debugging"]
provisioning_profile = "debugging com.mycompany.example-app"
signing_certificate = "Apple Development"

[tool.flet.ios.export_methods."release-testing"]
provisioning_profile = "release-testing com.mycompany.example-app"
team_id = "ABCDEFE234"
signing_certificate = "Apple Distribution"
export_options = { uploadSymbols = false }

[tool.flet.ios.export_methods."app-store-connect"]
provisioning_profile = "app-store-connect com.mycompany.example-app"
team_id = "ABCDEFE234"
signing_certificate = "Apple Distribution"
export_options = { uploadSymbols = true }
```
///

///

When building, the specified [export method](#export-method)
and its respective configuration above will be used.

## Deploying app to an Apple device for testing

Apple Configurator for macOS allows you to install `.ipa` files on iOS devices without using the App Store.

Follow these steps to deploy an `.ipa` file to your device:

**Step 1: Install Apple Configurator**

1. Install [Apple Configurator](https://apps.apple.com/ca/app/apple-configurator/id1037126344?mt=12) from App Store.

**Step 2: Connect the iOS Device**

1. Connect the **iPhone** or **iPad** to your Mac using a USB cable.
2. Unlock the device and **Trust** the computer if prompted.

**Step 3: Open Apple Configurator**

1. Launch **Apple Configurator** on your Mac.
2. The connected device should appear in the main window.

**Step 4: Add the `.ipa` File**

1. Drag and drop the `.ipa` file onto the connected device in Apple Configurator.
2. Alternatively, click **Add → Apps**, then choose the `.ipa` file from your Mac.

**Step 5: Install the App**

1. Click **Prepare** or **Install** to begin the deployment.
2. Apple Configurator will install the app on the device.

**Step 6: Trust the Developer Profile (For Ad Hoc or Enterprise Apps)**

If the `.ipa` is installed from an **Ad Hoc or Enterprise profile**, you may need to manually trust the developer:
1. On the iOS device, go to **Settings → General → VPN & Device Management**.
2. Under **Developer App**, select your **Developer Profile**.
3. Tap **Trust** and confirm.

## Uploading app to App Store Connect for distribution


### Step 1: Install and Sign in to Transporter

- Install and open [**Transporter**](https://apps.apple.com/us/app/transporter/id1450874784) from the Mac App Store.
- Sign in using your **Apple Developer Account** credentials (the same account used for App Store Connect).

### Step 2: Prepare Your `.ipa` File

- Build your app and export an `.ipa` file using either the **app-store-connect** or **release-testing** export options.

### Step 3: Upload the `.ipa` File in Transporter

1. Drag and drop the `.ipa` file directly into the Transporter window, or click "Add App" and select your `.ipa` file from your Mac.
2. Click the "..." button next to "Deliver", and select "Verify".
3. Wait for Transporter to complete the verification process.
4. After successful verification, click "Deliver" to upload your `.ipa` file to App Store Connect.

### Step 4: Check Upload Status

- Transporter will display a success message upon completion.
- If errors occur, carefully review the details provided, correct the issues, and repeat the upload process.

### Step 5: Confirm Upload in App Store Connect

1. Go to [App Store Connect](https://appstoreconnect.apple.com/).
2. Navigate to **Apps → Your App → TestFlight or App Store Version**.
3. Your newly uploaded build will initially appear under **Processing** (processing typically takes a few minutes to an hour).
4. Once processing completes, your build will become available for submission. You can now **submit the app for review**.

## Permissions

Setting iOS permissions which are written into `Info.plist` file:

```
flet build --info-plist permission_1=True|False|description permission_2=True|False|description ...
```

For example:

```
flet build --info-plist NSLocationWhenInUseUsageDescription="This app uses location service when in use."
```

Configuring iOS permissions in `pyproject.toml`:

```toml
[tool.flet.ios.info] # --info-plist
NSCameraUsageDescription = "This app uses the camera to ..."
```

## Deep linking

You can configure the [deep-linking]() settings for iOS bundle.

- **Scheme**: deep linking URL scheme to configure for iOS and Android builds, i.g. "https" or "myapp".
- **Host**: deep linking URL host.

The same can be configured as follows:

/// tab | `pyproject.toml`

/// tab | `[tool.flet]`
```toml
[tool.flet]
deep_linking.scheme = "https"
deep_linking.host = "mydomain.com"
```
///
/// tab | `[tool.flet.deep_linking]`
```toml
[tool.flet.deep_linking]
scheme = "https"
host = "mydomain.com"
```
///
/// tab | `[tool.flet.ios.deep_linking]`
```toml
[tool.flet.ios.deep_linking]
scheme = "https"
host = "mydomain.com"
```
///

///
/// tab | `flet build`
```bash
flet build --deep-linking-scheme "https" --deep-linking-host "mydomain.com"
```
///

See [Deep linking](https://docs.flutter.dev/ui/navigation/deep-linking) section in Flutter docs for more information and complete setup guide.
