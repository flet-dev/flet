---
title: "iOS apps (.ipa and TestFlight)"
---

# iOS apps: .ipa and TestFlight

The iOS section of **Publish** has these actions:

| Action | What you get | For |
|---|---|---|
| **Create an iOS Simulator app** | A `.app` for the iOS Simulator | Trying the app on a Mac. No Apple account needed |
| **Create an iOS app (.ipa)** | A signed `.ipa`: App Store, Ad hoc or Development | Uploading to App Store Connect yourself, or installing on registered iPhones and iPads |
| **Publish to TestFlight** | A build on TestFlight | Testers who install it with the TestFlight app |

**Publish to the App Store** shows **Coming soon**.

Everything except the Simulator app needs an Apple Developer Program membership and an
**App Store Connect account** connected to Studio.

## Connect App Store Connect

Studio signs and uploads your iOS apps with an **App Store Connect API key**. With it,
Studio registers the app's bundle ID, creates the signing certificate and provisioning
profiles, and uploads builds. You don't use Xcode or Keychain Access.

1. In [App Store Connect](https://appstoreconnect.apple.com/access/integrations/api),
   open **Users and Access › Integrations › App Store Connect API** and select
   **Team Keys**.
2. **Generate** a key with **Admin** access. Studio needs Admin to create certificates and
   profiles.
3. **Download** the key (`AuthKey_….p8`). Apple offers the file only once.
4. Note the key's **Key ID** and the **Issuer ID** shown above the list of keys. Your
   **Team ID** is in [Membership details](https://developer.apple.com/account#MembershipDetailsCard)
   on developer.apple.com.
5. In Studio, choose **Settings › Store accounts › Connect a store › App Store
   Connect**, or **Connect App Store Connect** on an iOS action screen. Upload the
   `.p8` and enter the three IDs.

Studio checks the key with Apple before saving it. It tells you if the key isn't a
Team key, lacks Admin access, or belongs to another team.

The key is stored encrypted and is only used on Studio's servers. It never reaches a
build machine. See [Signing keys and store accounts](signing-keys-and-store-accounts.md).

## Signing certificate

You don't have to create or upload a certificate. The first time an iOS build needs one,
Studio creates an **Apple Distribution** certificate for your team and keeps it, encrypted,
in **Settings › Signing keys**. Later builds and your other apps reuse it.
**Development** builds get an **Apple Development** certificate in the same way.

Apple allows only a few distribution certificates per team. If yours is at the limit,
either:

- **import** one you already have: in Keychain Access on a Mac, export the
  “Apple Distribution: …” certificate together with its private key as a `.p12`, then
  use **Settings › Signing keys › Add signing key › Apple certificate (.p12)** and
  select it under **Apple Distribution certificate** on the action screen, or
- **revoke** an unused certificate in
  [Certificates](https://developer.apple.com/account/resources/certificates/list) on
  developer.apple.com.

**⋯ › Download backup** gives you a certificate as a `.p12` with its password, to use in
Xcode. Deleting a certificate in Studio doesn't revoke it at Apple.

Provisioning profiles are made for you too, named `Flet Studio <bundle ID> …`. Studio
replaces a profile when it expires, when its certificate changes, or (for Ad hoc and
Development) when the enabled devices change.

### Bundle ID

The app's **bundle ID** (Publish › Settings › iOS) identifies it at Apple. It's made of
letters, digits, `-` and `.`, with no `_`, for example `com.example.my-app`. Studio
registers it with your team the first time you build.

## Create an iOS app (.ipa)

Pick a **Kind**:

| Kind | Installs on | For |
|---|---|---|
| **App Store** | No device directly | Uploading to App Store Connect yourself, e.g. with [Transporter](https://apps.apple.com/app/transporter/id1450874784). To get it onto phones, use [TestFlight](#testflight) |
| **Ad hoc** | The registered iPhones and iPads | Testers, through an [install link](#install-links) |
| **Development** | The registered iPhones and iPads | Debugging, e.g. attaching Xcode. Devices may need **Developer Mode** (Settings › Privacy & Security) |

The run's details show what each build was signed for under **Signed for**. For Ad hoc
and Development builds, that includes how many devices its profile lists.

To upload an App Store `.ipa` yourself, the app must first exist in App Store Connect
(**Apps › + › New App**, with the same bundle ID).

## Devices

Ad hoc and Development builds install only on devices registered with your Apple team.
Manage them in **Settings › Apple devices**, per App Store Connect account:

- **Registration link**: send it to testers. They open it in **Safari** on their iPhone
  or iPad, tap **Register this device**, then go to **Settings › Profile Downloaded ›
  Install**. The device is registered with your team, and nothing stays installed on
  it. A link works for 7 days, and you can revoke it.
- **Add device**: enter a device's name and **UDID** by hand. To find a UDID, connect the
  device to a Mac, select it in Finder, and click the line under its name.
- **On/off switch**: only enabled devices go into new builds.

Apple never deletes devices. Each kind of device (iPhone, iPad, …) has **100 slots per
membership year**, and a disabled device still uses its slot until your membership
renews. The page shows how many you've used.

A device registered after a build won't install that build. Run **Create an iOS app
(.ipa)** again: the new build's profile includes it.

## Install links

An Ad hoc or Development run has an **Install link** card in its details. **Create
install link** gives you a `get.flet.app/i/…` link, with a QR code, that you can send to
testers. On a registered iPhone or iPad, the link opens a page with an **Install**
button. On a computer it shows a QR code to scan with the phone.

A link works for **30 days**, or until you revoke it, and Studio keeps the build's `.ipa`
for as long as the link works. The card shows how many times the app was installed.

If iOS says it's **unable to install** the app, the device isn't in that build. Register
it, then make a new build.

## TestFlight

**Publish to TestFlight** builds the app for the App Store and uploads it from Studio's
servers. Apple then processes the build, which usually takes 5–15 minutes, and Studio
makes it available to your testers.

Before the first run:

1. **Create the app** in App Store Connect: **Apps › + › New App**, platform **iOS**,
   the app's bundle ID (Studio registers it, so it's already in the list), and any name
   and SKU. Until the app exists, the action screen says so and won't start a run.
2. **Create a TestFlight group** in App Store Connect › TestFlight, and add testers.
   **Internal** testers are members of your App Store Connect team. **External**
   testers are anyone, invited by email or a public link.

On the action screen's **Release** section:

- **Testers**: the groups that get the build. Internal groups set to receive every build
  get it automatically. The first build for an **external** group goes to Apple's beta
  review before testers see it. After a change in App Store Connect, click **Check
  again**.
- **What to test**: optional notes testers see in TestFlight.
- **Encryption**: leave **Uses encryption beyond HTTPS** off if the app only uses HTTPS
  and the system's own encryption, which is true of most apps. Turn it on if the app
  uses other encryption: App Store Connect then asks for export compliance information
  before testers get the build.

Testers install the build with the [TestFlight](https://apps.apple.com/app/testflight/id899247664)
app. A TestFlight build expires after 90 days.

The run's details show the build's TestFlight state, such as **Ready to test** or
**Waiting for beta review**, with a link to App Store Connect. If the upload fails,
**Retry upload** sends the same build again without a new build or charge. A build
Apple already has is never uploaded twice.

### Build numbers

Each build uploaded to App Store Connect needs a higher build number than the ones
before it. Studio starts above the highest build number App Store Connect has for the
app, including builds you uploaded yourself.

### “Missing purpose string in Info.plist”

Apple rejects a build whose code can access the camera, photos, location and similar
data unless the app explains why in its `Info.plist`. It applies even when your app
never uses that feature, as long as a library in the app could. If App Store Connect
reports **ITMS-90683**, add the purpose strings in **Publish › Settings › iOS**:
**Permissions** for camera, photo library, microphone or location, or **Info.plist
entries** for any other key Apple names. Then publish again.
