---
title: "Windows"
---

# Windows

Open **Publish › Windows**. Its **Overview** has a card for each place a Windows app goes:

| Card | What it does | Needs |
|---|---|---|
| **Windows app** | **Create Windows app** builds an installer (`<app>-setup.exe`) and a portable `.zip` with the app's folder and its `.exe` | Nothing. [Signing](#sign-the-windows-app) needs an Azure Artifact Signing account |
| **Microsoft Store** | Publishes the app on the [Microsoft Store](microsoft-store/index.md) | A Microsoft Store developer account |

When the run finishes, the card shows the build with **Download › Installer** or
**Portable**. **Create new version** builds the app as it is now. Downloads are kept for
a while (see [Downloads expire](index.md#downloads-expire)); after that the card says
**Download expired** and **Create new version** builds it again.

The app's settings (its name, icon, version, …) are on the **Settings** tab, with the
defaults in **All platforms › Settings**.

{/* SCREENSHOT: /img/docs/studio/publishing/windows-card.png — Publish › Windows with the built app */}

:::note[Creator plan]
Code signing and the Microsoft Store are part of the Creator plan. On Explorer, Windows
apps are built unsigned. See [Plans](index.md#plans).
:::

## Open the app

**Download › Installer (.exe)** is what to give your users:

1. Run the installer (`<app>-setup.exe`).
2. If the app isn't [signed](#sign-the-windows-app) and **Windows protected your PC**
   (SmartScreen) appears, click **More info › Run anyway**.

That's it: Setup asks nothing, installs the app for the current user in a few seconds
(no administrator rights needed) and opens it. The app is then in the Start menu, and
in **Settings › Apps** to uninstall it. To install it for every user of the PC instead,
run `<app>-setup.exe /ALLUSERS` from an administrator's command prompt.

Running the installer of a newer build upgrades the app in place, keeping its data, as
long as the app's [bundle ID](../../publish/index.md#bundle-id) stays the same: Setup
finds the installed app by it. Running the installer of the build that's installed, or
of an older one, just opens the installed app: to go back to an older build, uninstall
the app first.

**Download › Portable (.zip)** runs without installing, e.g. from a USB stick or on a
PC where you can't install apps:

1. Unzip the download (**right-click › Extract All…**). Keep the folder together: the
   `.exe` needs the files next to it.
2. Run the app's `.exe`, and confirm SmartScreen as above.

Keep the app's **company name** and **product name** the same between releases, too:
the app keeps its data in a folder named after them.

## Sign the Windows app

Signed, Windows shows your name as the app's publisher instead of "Unknown publisher",
the app runs with Smart App Control on, and SmartScreen builds up a reputation for it.
Studio signs with your own
[Azure Artifact Signing](https://learn.microsoft.com/azure/artifact-signing/) account. The
[step-by-step guide](azure-artifact-signing.md) covers the setup in Azure; in short:

1. In the Azure portal, create an Artifact Signing account, validate your identity and
   create a certificate profile (Public Trust). Note the account's region and name, and
   the profile's name.
2. In **Microsoft Entra ID › App registrations**, register an app (e.g. *Flet Studio
   signing*). Copy its **Application (client) ID** and **Directory (tenant) ID**.
3. Under the app's **Certificates & secrets**, add a client secret. Copy its **Value**
   (Azure shows it once) and note when it expires.
4. On the Artifact Signing account, open **Access control (IAM) › Add role assignment**
   and give the app registration the **Artifact Signing Certificate Profile Signer** role.
5. In Studio, open **Publish › Windows › Settings › Code signing › Connect Azure
   Artifact Signing**, and enter all of the above.

Studio checks it by signing a test digest once, then shows who the certificate names.
From the next run, every file of the app that isn't signed yet (the `.exe`, `.dll` and
`.pyd` files) is signed and timestamped, and so are the installer and its uninstaller.
The run fails if any of them isn't validly signed. For a quick test build, **Skip
signing for this run** on the Create Windows app screen builds it unsigned once, without
changing the settings.

The client secret stays on Studio's servers: a build only gets an access token that
expires within the hour and can only sign. Studio warns on the **Code signing** card a month
before the secret expires; make a new one in the app registration and connect again.

Each signed file is one signature on your Azure bill: a typical app signs about 50 files
per build, and the Basic tier includes 5,000 signatures a month. Artifact Signing is
available to organizations in the US, Canada, the EU, the UK, Australia, New Zealand,
Japan, South Korea, Singapore, Switzerland, Norway and Israel, and to individual developers
in the US and Canada ([who can sign](azure-artifact-signing.md#before-you-start)).

## Download page

Your Windows installer can go on the app's [download page](download-page.md), the same
page and link as its Android APK and Mac and Linux builds. Each visitor sees their own
system's download first, with who signed it.

- **Add this installer to the download page** on **Create Windows app** publishes the
  build when it's done (**Replace the Windows download with this installer** once the
  page has one). It's ticked by default once the page has a release, or when you start
  the build from **Publish › Download page**.
- Only an installer [signed with Azure Artifact Signing](#sign-the-windows-app) goes on
  it.

Adding an existing build, changing the version, the link and the page's settings are on
[Download page](download-page.md).

## Questions

### Can I put the app on the Microsoft Store?

Yes: see [Microsoft Store](microsoft-store/index.md). Microsoft signs Store packages
itself, so you don't need Artifact Signing for it.

### Will SmartScreen stop asking once the app is signed?

The publisher is shown right away. SmartScreen's reputation builds up as people download
and run the app, so a brand-new publisher may still see a warning at first.

### Can I sign with my own certificate (.pfx)?

Not yet: Studio signs with Azure Artifact Signing. Certificates for code signing now have
to live in a hardware or cloud key store, which Artifact Signing is.
