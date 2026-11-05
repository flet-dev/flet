---
title: "Desktop apps (Windows, macOS, Linux)"
---

# Desktop apps: Windows, macOS and Linux

Open **Publish › Windows**, **macOS** or **Linux**. Each has a card with the app,
packaged for that system (Windows and macOS also have a store card):

| Platform | Card and button | What you get |
|---|---|---|
| Windows | **Windows app** › **Create Windows app** | An installer (`<app>-setup.exe`), and a portable `.zip` with the app's folder and its `.exe` |
| macOS | **Mac app** › **Create Mac app** | A disk image (`.dmg`) with the app and an Applications shortcut, [signed and notarized](#sign-and-notarize-the-mac-app) when signing is set up |
| Linux | **Linux app** › **Create Linux app** | A `.tar.gz` with the app's folder and its executable |

When the run finishes, the card shows the build with **Download** (on Windows,
**Download › Installer** or **Portable**). **Create new version** builds the app as it
is now. Downloads are kept for a while (see
[Downloads expire](index.md#downloads-expire)); after that the card says **Download
expired** and **Create new version** builds it again.

The settings for each platform (the app's name, icon, version, …) are on its
**Settings** tab, with the defaults in **All platforms › Settings**.

{/* SCREENSHOT: /img/docs/studio/publishing/windows-card.png — Publish › Windows with the built app */}

## Open the app

Unless you [sign the Windows app](#sign-the-windows-app), Studio's desktop apps aren't
signed with a code-signing certificate, so the system asks before opening them the first
time.

### Windows

**Download › Installer (.exe)** is what to give your users:

1. Run the installer (`<app>-setup.exe`).
2. If **Windows protected your PC** (SmartScreen) appears, click **More info ›
   Run anyway**.

That's it: Setup asks nothing, installs the app for the current user in a few seconds
(no administrator rights needed) and opens it. The app is then in the Start menu, and
in **Settings › Apps** to uninstall it. To install it for every user of the PC instead,
run `<app>-setup.exe /ALLUSERS` from an administrator's command prompt. Running
the installer of a newer build upgrades it in place, keeping the app's data, as
long as the app's [bundle ID](../../publish/index.md#bundle-id) stays the same: Setup
finds the installed app by it. Running the installer of the build that's installed,
or of an older one, just opens the installed app: to go back to an older build,
uninstall the app first.

**Download › Portable (.zip)** runs without installing, e.g. from a USB stick or on a
PC where you can't install apps:

1. Unzip the download (**right-click › Extract All…**). Keep the folder together: the
   `.exe` needs the files next to it.
2. Run the app's `.exe`, and confirm SmartScreen as above.

Keep the app's **company name** and **product name** the same between releases, too:
the app keeps its data in a folder named after them.

### macOS

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

### Linux

1. Extract the download: `tar -xzf <app>.tar.gz`.
2. Run the executable in the extracted folder, e.g. `./<app>/<app>`. Keep the folder
   together: the executable needs the `lib` and `data` folders next to it.

The app needs GTK 3, which desktop Linux distributions include. On a minimal system,
install it first (`sudo apt install libgtk-3-0` on Debian and Ubuntu).

:::note[Creator plan]
Code signing, notarization, the Mac App Store and the Microsoft Store are part of
the Creator plan. On Explorer, Windows and Mac apps are built unsigned. See
[Plans](index.md#plans).
:::

## Sign the Windows app

Signed, Windows shows your name as the app's publisher instead of "Unknown publisher",
the app runs with Smart App Control on, and SmartScreen builds up a reputation for it.
Studio signs with your own
[Azure Artifact Signing](https://learn.microsoft.com/azure/artifact-signing/) account:

1. In the Azure portal, create an Artifact Signing account, validate your identity and
   create a certificate profile (Public Trust). Note the account's region and name, and
   the profile's name.
2. In **Microsoft Entra ID › App registrations**, register an app (e.g. *Flet Studio
   signing*). Copy its **Application (client) ID** and **Directory (tenant) ID**.
3. Under the app's **Certificates & secrets**, add a client secret. Copy its **Value**
   (Azure shows it once) and note when it expires.
4. On the certificate profile, open **Access control (IAM) › Add role assignment** and
   give the app registration the **Artifact Signing Certificate Profile Signer** role.
5. In Studio, open **Publish › Windows › Settings › Code signing › Connect Azure
   Artifact Signing**, and enter all of the above.

Studio checks it by signing a test digest once, then shows who the certificate names.
From the next run, every file of the app that isn't signed yet (the `.exe`, `.dll` and
`.pyd` files) is signed and timestamped, and so are the installer and its uninstaller.
The run fails if any of them isn't validly signed.

The client secret stays on Studio's servers: a build only gets an access token that
expires within the hour and can only sign. Studio warns on the **Code signing** card a month
before the secret expires; make a new one in the app registration and connect again.

Each signed file is one signature on your Azure bill: a Python app has dozens to hundreds
of files. Artifact Signing is available to organizations in the US, Canada, the EU and the
UK, and to individual developers in the US and Canada.

## Mac app

**Create Mac app** on **Publish › macOS** makes a disk image: open it and drag the app
to **Applications**. Then **Download** and **Create new version**, as the other cards.

Macs open an app downloaded from the internet only when it's signed with a
**Developer ID** certificate and notarized by Apple; otherwise macOS blocks opening it
by default. Signing is the app's setting, in **Publish › macOS › Settings › Signing**:

1. **App Store Connect**: Apple notarizes with your App Store Connect account, the same
   connection as iOS (an app that has one for iOS uses it).
2. **Developer ID certificate**: your team's *Developer ID Application* certificate, as a
   `.p12`. See [Sign and notarize the Mac app](#sign-and-notarize-the-mac-app).

With both, every run signs the app, puts it in the disk image, signs that, has Apple
notarize it (usually a few minutes) and staples Apple's ticket to it, so it opens even
offline. The card says whether runs are signed. If signing or notarizing fails, the run
fails and says why (Apple's findings file by file), rather than making an unsigned app.

For a quick test build, **Skip signing for this run** on the Create Mac app screen builds
it unsigned once, without changing the settings. **Create Windows app** has the same
option.

### Sign and notarize the Mac app

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

No Developer ID certificate yet? The team's Account Holder creates one in
[Certificates, Identifiers & Profiles](https://developer.apple.com/account/resources/certificates/list)
(**+ › Developer ID Application**). It must be the same team as the App Store Connect
account: Apple notarizes only with a key of the team that signed the app.

The certificate is used during the build, in a temporary keychain that's deleted
afterwards. Notarization happens on Studio's servers: neither your App Store Connect key
nor a token made from it reaches the build machine.

## Mac App Store and TestFlight

The macOS page's **App Store & TestFlight** card puts the app on TestFlight for Mac, for
your testers, and on the Mac App Store. It uses the same App Store Connect account as iOS.

1. **App category:** Apple needs it for every Mac build. Choose it on the card. It's
   also the App Store listing's primary category. If the app's macOS Info.plist sets
   `LSApplicationCategoryType`, that one is used.
2. **Create the app in App Store Connect** (**Apps › + › New App**, platform **macOS**,
   the bundle ID from the list), then **Check setup**. If the app should be on iOS too,
   tick both platforms: one app, one purchase.
3. **Publish** on the TestFlight row builds the app for the Mac App Store and uploads it
   from Studio's servers.
4. **Publish** on the App Store row submits the macOS version for App Review: a new build,
   or one already on TestFlight (no build, no credits). It needs the App Store listing
   with **Mac screenshots**: in the Preview, pick the macOS device and add the screen to
   the App Store listing (2880 × 1800). The listing's texts are the same as iOS's; the
   card's **Update listing** sends them, with the Mac screenshots, to the macOS version.

If App Store Connect already has the app for iOS, the card asks once how the Mac app is
sold:

- **Add macOS to the app** (recommended): one app for both platforms. One purchase covers
  iPhone, iPad and Mac (Universal Purchase), with one name and price. Apple can't undo
  this, so Studio asks you to confirm.
- **A separate macOS app**: its own app and purchase in App Store Connect, with its own
  bundle ID. Set it in **macOS › Settings**, for example `com.example.app.mac`, then
  create that app in App Store Connect.

Studio makes everything the build is signed with: the app is sandboxed and signed with
your team's Apple Distribution certificate (the same one as iOS), and the package
(`.pkg`) with a Mac Installer certificate, under a Mac App Store profile. The card's
**Create .pkg for manual upload** makes the package without uploading it.

## Download page

Your Windows, Mac and Linux builds can go on the app's [download page](download-page.md),
the same page and link as its Android APK. Each visitor sees their own system's download
first, with who signed it.

- **Add this installer** (or disk image, or app) **to the download page** on **Create
  Windows app**, **Create Mac app** and **Create Linux app** publishes the build when
  it's done (**Replace the Windows download with this installer**, and so on, once the
  page has one). It's ticked by default once the page has a release, or when you start
  the build from **Publish › Download page**.
- Only signed builds go on it: the Windows installer
  [signed with Azure Artifact Signing](#sign-the-windows-app), the Mac disk image
  [signed with Developer ID and notarized](#sign-and-notarize-the-mac-app). A Linux build
  goes on next to a signed Windows or Mac one
  ([why](download-page.md#why-linux-needs-a-signed-windows-or-mac-build)).

Adding an existing build, changing the version, the link and the page's settings are on
[Download page](download-page.md).

## Questions

### Can I put the app on the Microsoft Store or the Mac App Store?

Yes: see [Microsoft Store](microsoft-store.md) and
[Mac App Store and TestFlight](#mac-app-store-and-testflight).

### Will SmartScreen stop asking once the app is signed?

The publisher is shown right away. SmartScreen's reputation builds up as people download
and run the app, so a brand-new publisher may still see a warning at first.

### Can I sign with my own certificate (.pfx)?

Not yet: Studio signs with Azure Artifact Signing. Certificates for code signing now have
to live in a hardware or cloud key store, which Artifact Signing is.
