---
title: Packaging app for iOS
---

Instructions for packaging a Flet app into an iOS archive bundle and IPA for distribution.

**See complementary information [here](index.md).**

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

## <code class="doc-symbol doc-symbol-command"></code> `flet build ipa`

/// admonition | Note
This command can be run on a **macOS only**.
///

Builds an iOS app archive (`.ipa`) for testing and distribution.

To generate an `.ipa` for testing on your device or uploading to App Store Connect
for distribution, you will need the following:

- [Apple Developer Program](https://developer.apple.com/programs/) subscription with 
  access to [App Store Connect](https://appstoreconnect.apple.com/)
- [Application Indentifier](#application-identifier-app-id)
- [Signing Certificate](#signing-certificate)
- [Provisioning Profile](#provisioning-profile)

## Application Identifier (App ID)

A unique string that identifies your app within the Apple ecosystem.
It is required to sign and distribute an iOS app and is used for various services like
Push Notifications, App Groups, iCloud, and In-App Purchases.

It consists of two parts:

1. **Team ID**: A unique 10-character string assigned by Apple to your developer account.
2. **Bundle ID**: A reverse domain-style identifier for your app (e.g., `com.example.myapp`).

```mermaid
graph TD
    A[App ID: ABCDEFE234.com.example.myapp] --> B[Team ID: ABCDEFE234]
    A --> C[Bundle ID: com.example.myapp]
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

Now you have **Bundle ID** and **Team ID** that will be used to identify your app.

### Configuration

#### Team ID

The developer team ID to export iOS app.

/// tab | `flet build`
```bash
flet build ipa --ios-team-id ABCDEFE234
```
///
/// tab | `pyproject.toml`

/// tab | `[tool.flet.ios]`
```toml
[tool.flet.ios]
team_id = "ABCDEFE234"
```
///

///

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

### Configuration
The certificate name, SHA-1 hash, or automatic selector to use for signing iOS app bundle.
Automatic selectors allow Xcode to pick the newest installed certificate of a particular type.

The available automatic selectors are `"Apple Development"`, `"Apple Distribution"`,
`"Developer ID Application"`, `"iOS Developer"`, `"iOS Distribution"`, `"Mac App Distribution"`,
and `"Mac Developer"`.

/// tab | `flet build`
```bash
flet build ipa --ios-signing-certificate "Apple Distribution"
```
///
/// tab | `pyproject.toml`

/// tab | `[tool.flet.ios]`
```toml
[tool.flet.ios]
signing_certificate = "Apple Distribution"
```
///

///

## Provisioning Profile

A **Provisioning Profile** is a file that allows an iOS app to run on physical devices and be
distributed through the App Store or internally. It links your **App ID**,
**Developer/Distribution Certificate**, and **Registered Devices**.

There are different types of provisioning profiles:

- **Development Profile** – Used for testing on physical devices.
- **Ad Hoc Profile** – Used for distributing an app outside the App Store to specific devices.
- **App Store Profile** – Used for submitting an app to the App Store.
- **Enterprise Profile** – Used for internal distribution within an organization.

### Creating a New Provisioning Profile

Follow these steps to create a provisioning profile via the Apple Developer Portal:

#### Step 1: Go to Apple Developer Portal

- Visit the [Apple Developer Portal](https://developer.apple.com/account/resources/profiles/list);
- Sign in with your **Apple Developer Account**

#### Step 2: Create a New Provisioning Profile

- Click the **"+"** button to add a new provisioning profile;
- Choose the **type of profile**:
    - **iOS App Development** – for testing on devices
    - **Ad Hoc** – for distributing to specific devices
    - **App Store** – for submitting an app to the App Store
    - **In-House** – for internal distribution (Enterprise accounts only)
- Click **Continue**

#### Step 3: Select an App ID

- Choose the **App ID** that matches your app;
- Click **Continue**.

#### Step 4: Select a Distribution Certificate

- Choose the appropriate certificate:
    - **iOS Development Certificate** - for **iOS App Development** profile
    - **iOS Distribution Certificate** - for **Ad Hoc** or **App Store** profiles
- Click **Continue**.

#### Step 5: Select Registered Devices (for Development & Ad Hoc)

- If you selected an **iOS App Development** or **Ad Hoc** profile, select the devices to include;
- Click **Continue**.

#### Step 6: Name and Generate the Profile

- Enter a **Profile Name** (e.g., `MyApp Development Profile`);
- Click **Generate**;
- Click **Download** to get the `.mobileprovision` file.

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

Finally, you can use the below command to list all installed provisioning profiles, with their names and UUIDs:

```bash
for profile in ~/Library/MobileDevice/Provisioning\ Profiles/*.mobileprovision; do security cms -D -i "$profile" | grep -E -A1 '<key>(Name|UUID)</key>' | sed -n 's/.*<string>\(.*\)<\/string>/\1/p' | paste -d ' | ' - -; done
```

### Configuration

The provisioning profile name or UUID that used to sign and export the iOS app.

/// tab | `flet build`
```bash
flet build ipa --ios-provisioning-profile "release-testing com.mycompany.example-app"
```
///
/// tab | `pyproject.toml`

/// tab | `[tool.flet.ios]`
```toml
[tool.flet.ios]
provisioning_profile = "release-testing com.mycompany.example-app"
```
///

///

## Additional Configuration

Some additional configuration to successfully generate a "runnable" IPA:

/// admonition | Development package
To build `.ipa` for testing on your developer device you need to provide 
[provisioning profile](#provisioning-profile) option only. `flet build` will assume `debugging` as an 
export method and automatically choose the most recent "Apple Development" certificate in your keychain. 
Team ID is not required.
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

- `debugging` (or deprecated `development`): used for debugging and testing on development devices.
- `release-testing` (or deprecated `ad-hoc`): used for distributing the app outside the App Store to specific registered devices.
- `app-store-connect` (or deprecated `app-store`): used for submitting the app to the App Store.
- `enterprise`: used for internal distribution within an organization (requires an enterprise account).

To configure build settings for one or more export methods, see [export methods](#export-methods).

**Default:** `"debugging"`

/// tab | `flet build`
```bash
flet build ipa --ios-export-method debugging
```
///
/// tab | `pyproject.toml`

/// tab | `[tool.flet.ios]`
```toml
[tool.flet.ios]
export_method = "debugging"
```
///

///

### Export methods

Configure signing settings per export methods.

When building, the specified [export method](#export-method)
and its respective configuration above will be used.

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

## Deploying an App to an Apple Device for Testing

You can deploy `.ipa` files directly to an iPhone or iPad on macOS—ideal for 
internal testing without publishing to the App Store.

Follow the following steps:

### Step 1: Install and Launch Apple Configurator

- Install [Apple Configurator](https://apps.apple.com/ca/app/apple-configurator/id1037126344?mt=12) from App Store;
- Find and open it from your Applications folder.

### Step 2: Connect Your iOS Device

- Connect your device (iPhone or iPad) to your Mac via USB;
- Unlock the connected device, and tap **Trust This Computer**, if prompted;
- Wait for this device to appear in the Apple Configurator.

### Step 3: Add the `.ipa` File

- Either drag the `.ipa` file onto the connected device in Apple Configurator;
- Or click **Add → Apps**, then browse and select the `.ipa` file from your Mac.

### Step 4: Install the App

- Click **Prepare** or **Install** to begin the deployment/installation;
- Apple Configurator will install the app on the connected device.

### Step 5: Trust the Developer (for Ad Hoc or Enterprise apps)

If your app is signed with an **Ad Hoc** or **Enterprise** [provisioning profile](), 
you'll need to manually trust the developer:

- On the iOS device, go to **Settings → General → VPN & Device Management**;
- Under **Developer App**, tap your **Developer Profile**;
- Tap **Trust [Your Developer Name]**, then confirm.

## Uploading app to App Store Connect for distribution

### Step 1: Install and Sign in to Transporter

- Install and open [**Transporter**](https://apps.apple.com/us/app/transporter/id1450874784) from the Mac App Store.
- Sign in using your **Apple Developer Account** credentials (the same account used for App Store Connect).

### Step 2: Prepare Your `.ipa` File

- Build your app and export an `.ipa` file using either the **app-store-connect** or **release-testing** export options.

### Step 3: Upload the `.ipa` File in Transporter

- Drag and drop the `.ipa` file directly into the Transporter window, or click "Add App" and select your `.ipa` file from your Mac.
- Click the "..." button next to "Deliver", and select "Verify".
- Wait for Transporter to complete the verification process.
- After successful verification, click "Deliver" to upload your `.ipa` file to App Store Connect.

### Step 4: Check Upload Status

- Transporter will display a success message upon completion.
- If errors occur, carefully review the details provided, correct the issues, and repeat the upload process.

### Step 5: Confirm Upload in App Store Connect

- Go to [App Store Connect](https://appstoreconnect.apple.com/).
- Navigate to **Apps → Your App → TestFlight or App Store Version**.
- Your newly uploaded build will initially appear under **Processing** (processing typically takes a few minutes to an hour).
- Once processing completes, your build will become available for submission. You can now **submit the app for review**.

## Permissions

Setting iOS permissions which are written into `Info.plist` file:

```
flet build ipa --info-plist permission_1=True|False|description permission_2=True|False|description ...
```

For example:

```
flet build ipa --info-plist NSLocationWhenInUseUsageDescription="This app uses location service when in use."
```

Configuring iOS permissions in `pyproject.toml`:

```toml
[tool.flet.ios.info] # --info-plist
NSCameraUsageDescription = "This app uses the camera to ..."
```

## Disable splash screen

The [splash screen](index.md#splash-screen) is enabled/shown by default.

It can be disabled as follows:

/// tab | `flet build`
```bash
flet build apk --no-ios-splash
```
///
/// tab | `pyproject.toml`

/// tab | `[tool.flet]`
```toml
[tool.flet]
splash.ios = false
```
///
/// tab | `[tool.flet.splash]`
```toml
[tool.flet.splash]
ios = false
```
///

///