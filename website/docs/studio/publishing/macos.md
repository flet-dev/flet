---
title: "macOS"
---

# macOS

Open **Publish › macOS**. Its **Overview** has a card for each place a Mac app goes:

| Card | What it does | Needs |
|---|---|---|
| **Mac app** | **Create Mac app** builds a disk image (`.dmg`) with the app and an Applications shortcut, [signed and notarized](#sign-and-notarize-the-mac-app) when signing is set up | Nothing. Signing needs a Developer ID certificate and App Store Connect |
| **App Store & TestFlight** | Sends builds to your testers with TestFlight, then releases the app on the [Mac App Store](mac-app-store.md) | An Apple Developer Program membership and [App Store Connect](ios.md#connect-app-store-connect) |

When the run finishes, the card shows the build with **Download**. **Create new
version** builds the app as it is now. Downloads are kept for a while (see
[Downloads expire](index.md#downloads-expire)); after that the card says **Download
expired** and **Create new version** builds it again.

The app's settings (its name, icon, version, …) are on the **Settings** tab, with the
defaults in **All platforms › Settings**.

:::note[Creator plan]
Signing, notarization and the Mac App Store are part of the Creator plan. On Explorer,
Mac apps are built unsigned. See [Plans](index.md#plans).
:::

## Open the app

A **signed** Mac app opens like any app from the internet: open the `.dmg`, drag the
app onto the **Applications** shortcut, and open it from there. macOS asks once whether
to open an app downloaded from the internet, and shows that Apple checked it.

An **unsigned** one asks more:

1. Open the `.dmg` and drag the app to **Applications**.
2. Open it. macOS says it can't verify the app, because it isn't notarized by Apple.
   Click **Done** (not **Move to Trash**).
3. Open **System Settings › Privacy & Security**, scroll to the message about the app,
   and click **Open Anyway**, then confirm with your password. macOS remembers it for
   that app.

On macOS 14 and earlier, **right-click the app › Open** and confirm instead.

## Sign and notarize the Mac app

Macs open an app downloaded from the internet only when it's signed with a
**Developer ID** certificate and notarized by Apple; otherwise macOS blocks opening it
by default. Signing is the app's setting, in **Publish › macOS › Settings › Signing**:

1. **App Store Connect**: Apple notarizes with your App Store Connect account, the same
   connection as iOS (an app that has one for iOS uses it). See
   [Connect App Store Connect](ios.md#connect-app-store-connect).
2. **Developer ID certificate**: your team's *Developer ID Application* certificate. Add
   the one on your Mac ([export it](#export-the-developer-id-certificate) as a `.p12`), or
   [create one with Studio](#create-a-developer-id-certificate-with-studio): no Mac needed.

With both, every run signs the app, puts it in the disk image, signs that, has Apple
notarize it (usually a few minutes) and staples Apple's ticket to it, so it opens even
offline. The card says whether runs are signed. If signing or notarizing fails, the run
fails and says why (Apple's findings file by file), rather than making an unsigned app.

For a quick test build, **Skip signing for this run** on the Create Mac app screen builds
it unsigned once, without changing the settings.

The certificate is used during the build, in a temporary keychain that's deleted
afterwards. Notarization happens on Studio's servers: neither your App Store Connect key
nor a token made from it reaches the build machine.

### Export the Developer ID certificate

The Developer ID certificate is in the keychain of the Mac it was made on (or where
you imported it):

1. Open **Keychain Access**, choose the **login** keychain and the **My Certificates**
   tab.
2. Find **Developer ID Application: *your team* (*team ID*)**. It must have a private key
   under it (the arrow next to it): a certificate without its key can't sign.
3. Right-click it › **Export…**, choose **Personal Information Exchange (.p12)** and set
   a password.
4. In Studio, click **Set up signing** on the **Mac app** card (it opens **Publish › macOS ›
   Settings › Signing**), then **Add Developer ID certificate…**, choose the `.p12` and
   enter its password.

It must be the same team as the App Store Connect account: Apple notarizes only with a
key of the team that signed the app.

### Create a Developer ID certificate with Studio

No Developer ID certificate yet, or it isn't on a Mac you have? Studio makes one with you,
from any computer. Studio makes the certificate's private key and a request for Apple;
your team's **Account Holder** turns the request into a certificate on developer.apple.com
(Apple lets no one else make a Developer ID certificate).

1. Click **Set up signing** on the **Mac app** card, then **Add Developer ID
   certificate…** › **Create one with Studio**.
2. **Download request (.certSigningRequest)**.
3. In [Certificates, Identifiers & Profiles](https://developer.apple.com/account/resources/certificates/add),
   choose **Developer ID Application** and **Continue**, keep **G2 Sub-CA**, choose the
   request file, then **Continue** and **Download**. You get a `.cer` file.
4. Back in Studio, **Choose .cer**, select it, and **Add certificate**.

Studio checks that Apple made the certificate from its request, then signs your Mac apps
with it. You can close the dialog between the steps: it opens where you left off, with the
same request. **Start over…** makes a new key and request; a certificate Apple already
made from the old request can't be used after that.

Studio keeps the only copy of the private key. Download a backup with **Download (.p12)**
on the certificate (in **Publish › macOS › Settings › Signing**), and keep it somewhere
safe: with it you can also sign in Xcode, and without it a lost key means a new
certificate.

Apple allows only a few Developer ID certificates per team. If one already exists but its
private key is lost (it was made on a Mac you no longer have), create a new one as above
rather than revoking the old one: revoking a Developer ID certificate can stop apps
already signed with it from opening.

## Download page

Your Mac disk image can go on the app's [download page](download-page.md), the same page
and link as its Android APK and Windows and Linux builds. Each visitor sees their own
system's download first, with who signed it.

- **Add this disk image to the download page** on **Create Mac app** publishes the build
  when it's done (**Replace the Mac download with this disk image** once the page has
  one). It's ticked by default once the page has a release, or when you start the build
  from **Publish › Download page**.
- Only a disk image [signed with Developer ID and notarized](#sign-and-notarize-the-mac-app)
  goes on it.

Adding an existing build, changing the version, the link and the page's settings are on
[Download page](download-page.md).

## Questions

### Can I put the app on the Mac App Store?

Yes: see [Mac App Store and TestFlight](mac-app-store.md). It uses the same App Store
Connect account as iOS, and Studio makes the certificates the Mac App Store needs.
