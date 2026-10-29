---
title: "Desktop apps (Windows, macOS, Linux)"
---

# Desktop apps: Windows, macOS and Linux

Open **Publish › Windows**, **macOS** or **Linux**. Each has one card with the app,
packaged for that system:

| Platform | Card | What you get |
|---|---|---|
| Windows | **Create Windows app** | An installer (`setup.exe`), and a portable `.zip` with the app's folder and its `.exe` |
| macOS | **Create Mac app (.dmg)** | A disk image with the app, [signed and notarized](#sign-and-notarize-the-mac-app): it opens on any Mac. Or, on the **Unsigned Mac app** card, the `.app` zipped, for your own Mac |
| Linux | **Create Linux app** | A `.tar.gz` with the app's folder and its executable |

When the run finishes, the card shows the build with **Download** (on Windows,
**Download › Installer** or **Portable**). **Update** builds
the app as it is now. Downloads are kept for a while (see
[Downloads expire](index.md#downloads-expire)); after that the card says **Download
expired** and **Update** builds it again.

The settings for each platform (the app's name, icon, version, …) are on its
**Settings** tab, with the defaults in **All platforms › Settings**.

{/* SCREENSHOT: /img/docs/studio/publishing/windows-card.png — Publish › Windows with the built app */}

## Open the app

Unless you [sign the Windows app](#sign-the-windows-app), Studio's desktop apps aren't
signed with a code-signing certificate, so the system asks before opening them the first
time.

### Windows

**Download › Installer (setup.exe)** is what to give your users:

1. Run the `setup.exe`.
2. If **Windows protected your PC** (SmartScreen) appears, click **More info ›
   Run anyway**.

That's it: Setup asks nothing, installs the app for the current user in a few seconds
(no administrator rights needed) and opens it. The app is then in the Start menu, and
in **Settings › Apps** to uninstall it. To install it for every user of the PC instead,
run `setup.exe /ALLUSERS` from an administrator's command prompt. Running
the `setup.exe` of a newer build upgrades it in place, keeping the app's data, as
long as the app's [bundle ID](../../publish/index.md#bundle-id) stays the same: Setup
finds the installed app by it. Running the `setup.exe` of the build that's installed,
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

The **Mac app (.dmg)** opens like any app from the internet: open the `.dmg`, drag the
app onto the **Applications** shortcut, and open it from there. macOS asks once whether
to open an app downloaded from the internet, and shows that Apple checked it.

The **unsigned** app asks more:

1. Unzip the download (double-click it) and move the `.app` to **Applications** if you
   like.
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
expires within the hour and can only sign. Studio warns on the card a month before the
secret expires; make a new one in the app registration and connect again.

Each signed file is one signature on your Azure bill: a Python app has dozens to hundreds
of files. Artifact Signing is available to organizations in the US, Canada, the EU and the
UK, and to individual developers in the US and Canada.

## Mac app

Macs open an app downloaded from the internet without a warning only when it's signed
with a **Developer ID** certificate and notarized by Apple. The **Mac app** card on
**Publish › macOS** does both:

1. **Connect App Store Connect**: Apple notarizes with your App Store Connect account,
   the same connection as iOS (an app that has one for iOS uses it).
2. **Add Developer ID certificate**: your team's *Developer ID Application* certificate,
   as a `.p12`. See [Sign and notarize the Mac app](#sign-and-notarize-the-mac-app).
3. **Create Mac app (.dmg)**. The run signs the app, puts it in a disk image with an
   Applications shortcut, signs that, has Apple notarize it (usually a few minutes) and
   staples Apple's ticket to it, so it opens even offline. Then **Download** and
   **Update**, as the other cards.

If Apple doesn't notarize the app, the run fails and its log lists what Apple found,
file by file.

### Sign and notarize the Mac app

The Developer ID certificate is in the keychain of the Mac it was made on (or where
you imported it):

1. Open **Keychain Access**, choose the **login** keychain and the **My Certificates**
   tab.
2. Find **Developer ID Application: *your team* (*team ID*)**. It must have a private key
   under it (the arrow next to it): a certificate without its key can't sign.
3. Right-click it › **Export…**, choose **Personal Information Exchange (.p12)** and set
   a password.
4. In Studio, select **Add Developer ID certificate** on the card (or **Publish › macOS ›
   Settings › Signing**), choose the `.p12` and enter its password.

No Developer ID certificate yet? The team's Account Holder creates one in
[Certificates, Identifiers & Profiles](https://developer.apple.com/account/resources/certificates/list)
(**+ › Developer ID Application**). It must be the same team as the App Store Connect
account: Apple notarizes only with a key of the team that signed the app.

The certificate is used during the build, in a temporary keychain that's deleted
afterwards. Notarization happens on Studio's servers: neither your App Store Connect key
nor a token made from it reaches the build machine.

## Questions

### Can I put the app on the Microsoft Store or the Mac App Store?

The Microsoft Store, yes: see [Microsoft Store](microsoft-store.md). The Mac App Store,
not from Studio yet: build the app on your own computer with
[`flet build`](../../publish/index.md). Until then, the [Mac app](#mac-app) opens on any
Mac, signed and notarized.

### Will SmartScreen stop asking once the app is signed?

The publisher is shown right away. SmartScreen's reputation builds up as people download
and run the app, so a brand-new publisher may still see a warning at first.

### Can I sign with my own certificate (.pfx)?

Not yet: Studio signs with Azure Artifact Signing. Certificates for code signing now have
to live in a hardware or cloud key store, which Artifact Signing is.
