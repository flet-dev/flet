---
title: "App Store and TestFlight"
---

# App Store and TestFlight

The **App Store & TestFlight** card on **Publish › iOS** sends builds to your testers with
[TestFlight](#testflight), then releases the app on the [App Store](#app-store). Studio
builds, signs and uploads every build from its servers: you don't use Xcode.

The **App Store & TestFlight** card on **Publish › macOS** works the same way for the Mac
App Store: see [Mac App Store and TestFlight](../mac-app-store.md).

:::note[Creator plan]
The App Store, TestFlight and an App Store .ipa are part of the Creator plan; the card's
**Free trial** link opens the plans, where you can start a free 7-day trial with 500
bonus credits. On Explorer you can still [test on your devices](../ios.md#test-on-your-devices)
with install links and build the [iOS Simulator app](../ios.md#ios-simulator-app). See
[Plans](../index.md#plans).
:::

:::tip[In short]
1. **[Connect App Store Connect](../ios.md#connect-app-store-connect)** with an API key.
2. **Create the app in App Store Connect**: the card gives you its name and bundle ID.
3. **Publish** on the **TestFlight** row for your testers, and on the **App Store** row
   for App Review. The App Store needs the [App Store listing](store-listing.md).
:::

## Before you start

You need an [Apple Developer Program](https://developer.apple.com/programs/) membership
and the app's App Store Connect account connected: see
[Connect App Store Connect](../ios.md#connect-app-store-connect). The same connection
builds for [your devices](../ios.md#test-on-your-devices).

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

If App Store Connect already has the app for macOS (it was on the Mac first), the card
asks once instead: **Add iOS to the app** (one purchase for both; Apple can't undo it) or
**A separate iOS app** with its own bundle ID. See
[Mac App Store and TestFlight](../mac-app-store.md).

## TestFlight

**Publish** (or **Update**) on the card's **TestFlight** row builds the app for the App
Store and uploads it from Studio's servers. Apple then processes the build, which usually
takes 5–15 minutes, and Studio makes it available to your testers.

Before the first run, **create a TestFlight group** in App Store Connect › TestFlight, and
add testers. **Internal** testers are members of your App Store Connect team.
**External** testers are anyone, invited by email or a public link.

### Test Information for external testers

Apple's beta review reads TestFlight's **Test Information** before external testers get
an app's first build: a **beta app description**, a **feedback email**, and a contact
for the reviewer (name, email and phone). Internal testers don't need it.

Add them in the [App Store listing](store-listing.md#app-review-and-testflight)
(**Update listing** on the card's Store listing row): the **TestFlight** section has the
beta description and feedback email, and **App Review contact** the contact. Studio sends them with the build. If you've already filled
them in App Store Connect › TestFlight › Test Information, that counts too.

With an external group ticked and something missing, the TestFlight screen says what,
with **Edit App Store listing**, and won't start the run until it's there.

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
**Permissions** for camera, photo library, microphone or location, or **Info.plist**
for any other key Apple names. Then publish again.

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

The App Store needs the [store listing](store-listing.md): its row says so until you
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

**Create .ipa for manual upload**, at the bottom of the App Store & TestFlight card,
builds a signed App Store `.ipa` to upload to App Store Connect yourself, e.g. with
[Transporter](https://apps.apple.com/app/transporter/id1450874784). It doesn't install on
devices: to try a build on a phone, use [TestFlight](#testflight) or
[Test on your devices](../ios.md#test-on-your-devices).
