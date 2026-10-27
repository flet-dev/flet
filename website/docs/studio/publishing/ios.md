---
title: "iOS apps"
---

# iOS apps

Open **Publish › iOS**. Its **Overview** has a card for each place an iOS app goes:

| Card | What it does | Needs |
|---|---|---|
| **App Store & TestFlight** | Sends builds to your testers with [TestFlight](#testflight), then releases the app on the [App Store](#app-store) | An Apple Developer Program membership and [App Store Connect](#connect-app-store-connect) |
| **Test on your devices** | Builds the app for your registered iPhones and iPads and gives you an [install link](#install-links) | The same |
| **iOS Simulator** | A [Simulator app](#ios-simulator-app) to try on a Mac | No Apple account |

Each card shows its next step while it isn't set up yet, then what's live, with
**Update** to publish a new version. **Activity** lists the platform's runs, and
**Settings** has the app's [signing certificate](#signing-certificate) and settings.

{/* SCREENSHOT: /img/docs/studio/publishing/ios-overview.png — Publish › iOS with its three cards */}

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
[Signing keys and store accounts](signing-keys-and-store-accounts.md).

## Create the app in App Store Connect

Once connected, the App Store & TestFlight card checks whether App Store Connect has the
app. Until it does, the card shows **Finish App Store Connect setup** with the app's
name and bundle ID to copy:

1. **Open App Store Connect** and go to **Apps › + › New App**.
2. Choose platform **iOS**, the name shown, and the **bundle ID** from the list. Studio
   registers the bundle ID with your team when it checks, so it's already in the list.
   Any SKU will do.
3. Back in Studio, click **Check setup**. The card then shows TestFlight, the App Store
   and the store listing.

Check the bundle ID before you create the app: it can't be changed later. If Studio
couldn't register it (the key needs Admin access), register it yourself in your Apple
Developer account under **Identifiers**.

## TestFlight

**Publish** (or **Update**) on the card's **TestFlight** row builds the app for the App
Store and uploads it from Studio's servers. Apple then processes the build, which usually
takes 5–15 minutes, and Studio makes it available to your testers.

Before the first run, **create a TestFlight group** in App Store Connect › TestFlight, and
add testers. **Internal** testers are members of your App Store Connect team.
**External** testers are anyone, invited by email or a public link.

On the screen's **Release** section:

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

The TestFlight row shows the build's state from App Store Connect: **Processing**,
**Ready to test**, **In beta review** or **Expired**. If the upload fails, **Retry
upload** sends the same build again without a new build or charge. A build Apple already
has is never uploaded twice.

### Build numbers

Each build uploaded to App Store Connect needs a higher build number than the ones
before it. Studio starts above the highest build number App Store Connect has for the
app, including builds you uploaded yourself.

### “Missing purpose string in Info.plist”

Apple rejects a build whose code can access the camera, photos, location and similar
data unless the app explains why in its `Info.plist`. It applies even when your app
never uses that feature, as long as a library in the app could. If App Store Connect
reports **ITMS-90683**, add the purpose strings in **Publish › iOS › Settings**:
**Permissions** for camera, photo library, microphone or location, or **Info.plist
entries** for any other key Apple names. Then publish again.

## App Store listing

Studio keeps the app's App Store listing in the app's files, in the hidden
`.store/app-store/` folder, which is never packaged into the app. Edit it with **Create
listing** or **Update listing** on the **Store listing** row of the App Store &
TestFlight card:

- **Texts**, per language: app name and subtitle (30 characters each), description
  (4000), keywords (100, comma-separated), promotional text (170), and the support,
  marketing and privacy policy URLs. **Write with AI** asks the agent to write or
  translate the texts from what the app does.
- **Screenshots**: 1 to 10 for **iPhone (6.9")** and for **iPad (13")**. Flet apps run on
  iPad too, so Apple asks for both. In the Preview, pick the **iPhone 6.9"** or
  **iPad 13"** device and add the screen to the App Store listing: it's captured at
  Apple's size (1320 × 2868 and 2064 × 2752). A language without screenshots uses the
  default language's. The app's icon comes from its build.
- **App details**: the primary and secondary category, and the copyright line.
- **App Review contact**: the name, email and phone App Review can reach, and optional
  notes for the reviewer. Don't put passwords in the notes.

**Import from App Store** replaces the files with the app's current listing in App Store
Connect.

The **Store listing** row shows where it stands: **Not created yet**, **No update
sent**, **Sent** with the date, or **Changed, not sent** when it was edited since. The
listing screen sends it from its footer.

Sending the listing sends it to the app's version that's still being
prepared: the one with the app's current version number (Publish › iOS ›
Settings › Version), which Studio creates if needed. It needs no build and costs no credits. A screenshot set is only uploaded again when
it changed. App Store Connect doesn't let you change a version that's waiting for or in
review: remove it from review there first, or wait for Apple's decision.

Some of what Apple asks for isn't part of the listing and is set only in App Store
Connect: **App Privacy** (what data the app collects), **pricing and availability**, and
the **age rating** questionnaire.

## App Store

**Publish** (or **Update**) on the card's **App Store** row opens **Publish to the App
Store**. If TestFlight has a build the App Store doesn't, **Which build** lets you
submit **that build**: what your testers had, with no new build and no credits. Or
choose a new build of the app as it is now. Then Studio:

1. finds or creates the App Store version for the version number. A version that's
   already on the App Store can't change: set a newer version number first.
2. attaches the build and sets **Release**: automatically once Apple approves the
   version, or manually, when you release it in App Store Connect.
3. sets **What's new**. Apple skips it for an app's first version.
4. sends the App Store listing too, if you choose **Also send the App Store listing**.
5. submits the version for **App Review**.

The App Store needs the [store listing](#app-store-listing): its row says so until you
create it.

If App Store Connect can't submit the version yet, for example because screenshots, App
Privacy answers or the age rating are missing, the run lists what Apple asked for. Fix
those, then **Retry upload**: the build isn't uploaded again and there's no new charge.

The App Store row shows the version's state from App Store Connect: **Waiting for
review**, **In review**, **Approved: release it in App Store Connect** (for a manual
release), **Published to the App Store**, or **Rejected by App Review** with a link to
Apple's message. Apple usually reviews a version within a day or two, and emails you
when its status changes.

### An .ipa to upload yourself

**Create IPA for manual upload**, at the bottom of the App Store & TestFlight card,
builds a signed App Store `.ipa` to upload to App Store Connect yourself, e.g. with
[Transporter](https://apps.apple.com/app/transporter/id1450874784). It doesn't install on
devices: to try a build on a phone, use [TestFlight](#testflight) or
[Test on your devices](#test-on-your-devices).

## Test on your devices

The **Test on your devices** card builds the app for the iPhones and iPads registered
with your Apple team (an **Ad hoc** build) and gives you an [install link](#install-links)
for it. Testers need nothing but the link: no TestFlight, no App Store review.

1. Register the devices: **View devices** on the card opens
   [Settings › Apple devices](#devices).
2. Click **Create install link**. When the run finishes, the card shows the link with
   **Open**, **Copy**, **QR code** and **Share**.
3. **Update** builds the app again for the devices registered now. The link stays the
   same: testers who have it install the new build.

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

A device registered after a build won't install that build. Click **Update** on the
**Test on your devices** card: the new build's profile includes it, and the card says
when devices were registered since the last build.

## Install links

The install link is a `get.flet.app/i/…` link. On a registered iPhone or iPad it opens a
page with an **Install** button; on a computer it shows a QR code to scan with the
phone.

A link works for **30 days** from the latest build, or until you revoke it, and Studio
keeps the build's `.ipa` for as long as the link works. The card shows how many times
the build was installed.

If iOS says it's **unable to install** the app, the device isn't in that build. Register
it, then click **Update** on the card.

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
