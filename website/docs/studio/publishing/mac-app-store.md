---
title: "Mac App Store and TestFlight"
---

# Mac App Store and TestFlight

The **App Store & TestFlight** card on **Publish › macOS** puts the app on TestFlight for
Mac, for your testers, and on the Mac App Store. It works like the
[iOS card](app-store/index.md), with the same App Store Connect account and the same
[App Store listing](app-store/store-listing.md).

:::note[Creator plan]
The Mac App Store and TestFlight are part of the Creator plan. On Explorer, the card's
**Free trial** link opens the plans, where you can start a free 7-day Creator trial with
500 bonus credits. See [Plans](index.md#plans).
:::

## Before you start

You need an Apple Developer Program membership and the app's
[App Store Connect account](ios.md#connect-app-store-connect) connected: an app that has
one for iOS uses it.

## Set up the app

1. **App category:** Apple needs it for every Mac build. Choose it on the card. It's
   also the App Store listing's primary category. If the app's macOS Info.plist sets
   `LSApplicationCategoryType`, that one is used.
2. **Create the app in App Store Connect** (**Apps › + › New App**, platform **macOS**,
   the bundle ID from the list), then **Check setup**. If the app should be on iOS too,
   tick both platforms: one app, one purchase.

If App Store Connect already has the app for iOS, the card asks once how the Mac app is
sold:

- **Add macOS to the app** (recommended): one app for both platforms. One purchase covers
  iPhone, iPad and Mac (Universal Purchase), with one name and price. Apple can't undo
  this, so Studio asks you to confirm.
- **A separate macOS app**: its own app and purchase in App Store Connect, with its own
  bundle ID. Set it in **macOS › Settings**, for example `com.example.app.mac`, then
  create that app in App Store Connect.

## TestFlight

**Publish** on the card's **TestFlight** row builds the app for the Mac App Store and
uploads it from Studio's servers. Testers, groups, Test Information and the build's
states work as on iOS: see [TestFlight](app-store/index.md#testflight).

## Mac App Store

**Publish** on the card's **App Store** row submits the macOS version for App Review: a
new build, or one already on TestFlight (no build, no credits). Releasing and the
version's states work as on iOS: see [App Store](app-store/index.md#app-store).

It needs the App Store listing with **Mac screenshots**: in the Preview, pick the macOS
device and add the screen to the App Store listing (2880 × 1800). The listing's texts are
the same as iOS's; the card's **Update listing** sends them, with the Mac screenshots, to
the macOS version. See [App Store listing](app-store/store-listing.md).

## How it's signed

Studio makes everything the build is signed with: the app is sandboxed and signed with
your team's Apple Distribution certificate (the same one as iOS), and the package
(`.pkg`) with a Mac Installer certificate, under a Mac App Store profile. The card's
**Create .pkg for manual upload** makes the package without uploading it, to upload
yourself, e.g. with [Transporter](https://apps.apple.com/app/transporter/id1450874784).

Mac App Store builds aren't the Developer ID ones the [Mac app card](macos.md#sign-and-notarize-the-mac-app)
makes for downloading: each card signs its own way.
