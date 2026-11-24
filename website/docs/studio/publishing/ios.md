---
title: "iOS"
---

# iOS

Open **Publish › iOS**. Its **Overview** has a card for each place an iOS app goes:

| Card | What it does | Needs |
|---|---|---|
| **App Store & TestFlight** | Sends builds to your testers with TestFlight, then releases the app on the App Store: see [App Store and TestFlight](app-store/index.md) | An Apple Developer Program membership and [App Store Connect](#connect-app-store-connect) |
| **Test on your devices** | Builds the app for your registered iPhones and iPads and gives you an [install link](#install-links) | The same |
| **iOS Simulator** | A [Simulator app](#ios-simulator-app) to try on a Mac | No Apple account |

Each card shows its next step while it isn't set up yet, then what's live, with a
button to publish a new version (**Update**, **Build new version** or **Create new
version**). **Activity** lists the platform's runs, and **Settings** has the app's
[signing certificate](#signing-certificate) and settings.

{/* SCREENSHOT: /img/docs/studio/publishing/ios-overview.png — Publish › iOS with its three cards */}

:::note[Creator plan]
The App Store, TestFlight and an App Store .ipa are part of the Creator plan. On
Explorer you can still [test on your devices](#test-on-your-devices) with install links
and build the [iOS Simulator app](#ios-simulator-app). See [Plans](index.md#plans).
:::

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
5. In Studio, click **Connect App Store Connect** on the **App Store & TestFlight** card
   (or on **Test on your devices**: connecting either connects both). Choose an account
   you connected before, or **Connect another account…**: upload the `.p8` and enter
   the three IDs.

Studio checks the key with Apple before saving it. It tells you if the key isn't a
Team key, lacks Admin access, or belongs to another team.

The key is stored encrypted and is only used on Studio's servers. It never reaches a
build machine. **Connection details** on the card shows which account the app uses,
with **Change connection…** and **Disconnect from this app**. See
[Signing keys and publishing accounts](signing-keys-and-store-accounts.md).

Next, for TestFlight and the App Store:
[create the app in App Store Connect](app-store/index.md#create-the-app-in-app-store-connect).

## Test on your devices

The **Test on your devices** card builds the app for the iPhones and iPads registered
with your Apple team (an **Ad hoc** build) and gives you an [install link](#install-links)
for it. Testers need nothing but the link: no TestFlight, no App Store review.

1. Register the devices: **View N devices** (or **Add a device**) on the card opens
   [Settings › Apple devices](#devices).
2. Click **Build for your devices**. The form shows at the top how many registered
   devices can install it (**Manage devices** opens Settings › Apple devices). When the
   run finishes, the card shows the link with **Open**, **Copy**, **QR code** and **Share**.
3. **Build new version** builds the app again for the devices registered now. The link
   stays the same: testers who have it install the new build.

Apple only installs these builds on registered devices, which is why the card needs App
Store Connect even though nothing goes to the App Store.

## Devices

Builds for your devices install only on devices registered with your Apple team.
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

A device registered after a build won't install that build. Click **Build new version**
on the **Test on your devices** card: the new build's profile includes it, and the card
says when devices were registered since the last build.

## Install links

The install link is a `get.flet.app/i/…` link. On a registered iPhone or iPad it opens a
page with an **Install** button; on a computer it shows a QR code to scan with the
phone.

A link works for **30 days** from the latest build, or until you revoke it, and Studio
keeps the build's `.ipa` for as long as the link works. The card shows how many times
the build was installed.

If iOS says it's **unable to install** the app, the device isn't in that build. Register
it, then click **Build new version** on the card.

## iOS Simulator app

**Create Simulator app** on the **iOS Simulator** card builds the app for the iOS
Simulator, which comes with Xcode on a Mac. No Apple account is needed. **Download** the
`.zip` when the run finishes, unzip it, and drag the `.app` onto a running Simulator
window (or run `xcrun simctl install booted <App>.app`). It doesn't run on an iPhone or
iPad.

## Signing certificate

You don't have to create or upload a certificate. The first time an iOS build needs one,
Studio creates an **Apple Distribution** certificate for your team and keeps it,
encrypted. Later builds and your other apps reuse it.

**Publish › iOS › Settings** shows it in the **Signing** card: **Managed by Studio**,
until when it's valid, **Download (.p12)** (with its password, to use in Xcode), and
**Use your own certificate…**. Action screens show the same card with **Manage**.

Apple allows only a few distribution certificates per team. If yours is at the limit,
either:

- **use your own**: in Keychain Access on a Mac, export the “Apple Distribution: …”
  certificate together with its private key as a `.p12`, then **Use your own
  certificate…** on the Signing card. **Use Studio's certificate** switches back; or
- **revoke** an unused certificate in
  [Certificates](https://developer.apple.com/account/resources/certificates/list) on
  developer.apple.com.

Deleting a certificate in Studio doesn't revoke it at Apple.

Provisioning profiles are made for you too, named `Flet Studio <bundle ID> …`. Studio
replaces a profile when it expires, when its certificate changes, or (for your devices)
when the enabled devices change.

### Bundle ID

The app's **bundle ID** (Publish › iOS › Settings) identifies it at Apple. It's made of
letters, digits, `-` and `.`, with no `_`, for example `com.example.my-app`. Studio
registers it with your team when it first checks App Store Connect for the app, or on
its first build.
