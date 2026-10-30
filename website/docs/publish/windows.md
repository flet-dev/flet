---
title: "Packaging app for Windows"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';

Instructions for packaging a Flet app into a Windows application.

:::tip[Info]
This guide provides detailed Windows-specific information.
Complementary and more general information is available [here](index.md).
:::

:::info[Alternative: flet pack]
For a PyInstaller-based way to package desktop apps — no Visual
Studio or Flutter toolchain required — see [`flet pack`](using-pyinstaller.md).
:::

## Prerequisites

### Visual Studio

Visual Studio ([2022](https://learn.microsoft.com/en-us/visualstudio/install/install-visual-studio?view=vs-2022)
or [2026](https://learn.microsoft.com/en-us/visualstudio/install/install-visual-studio?view=visualstudio))
is required with the **Desktop development with C++** workload installed.

Follow this [guide](https://medium.com/@teamcode20233/a-guide-to-install-desktop-development-with-c-workload-542bb92cfe90)
for instructions on downloading and installing correct Visual Studio
components for Flutter desktop development.

## `flet build windows`

:::note[Note]
This command can be run on **Windows only**.
:::

Builds a Windows application.

### Windows on ARM

On an ARM64 PC, such as a Snapdragon laptop, `flet build windows` builds an x64
app, which runs there through Windows' built-in x64 emulation. Flet's Python
runtime for Windows is x64-only, so Flet builds with its own Flutter SDK, which
is x64 as well, even when an ARM64 Flutter SDK is on `PATH`. The first start of
the app takes noticeably longer under emulation.

## App termination

Closing the window terminates the app immediately, without running Python `atexit`
handlers, C++ static destructors, or flushing writes that have not yet reached the
operating system. See [How a built app terminates](index.md#how-a-built-app-terminates).

## Distributing

`flet build windows` leaves a **self-contained folder** in `build\windows`: your
app's `.exe` next to the DLLs it loads and the `data`, `DLLs`, `Lib`,
`site-packages` and `app` folders. The PCs your app runs on need no Python, and
Flet itself needs no Visual C++ Redistributable, because `msvcp140.dll`,
`vcruntime140.dll` and `vcruntime140_1.dll` ship in the folder. A package with
native code that needs other Visual C++ DLLs, such as `msvcp140_1.dll` or
`vcomp140.dll`, and doesn't bundle them needs the Redistributable on the user's
PC. A folder of DLLs isn't something an end user can download and double-click,
though, so wrap it in one of the formats below, or publish it in the
[Microsoft Store](#microsoft-store).

Two rules apply to every format:

- **Keep the folder together:** The `.exe` loads its DLLs, `data` and Python
  runtime from its own folder, so copied on its own it fails with
  `The code execution cannot proceed because battery_plus_plugin.dll was not found`.
  The folder itself can live anywhere, including `C:\Program Files`, where the
  running app has no write access, since Flet writes nothing into its own
  folder. Make sure your code doesn't either: save files in
  [`FLET_APP_STORAGE_DATA`](../reference/environment-variables.md#flet_app_storage_data),
  which is also the app's working directory, and never next to `__file__`,
  which points into the folder.
- **Keep the [company](index.md#company-name) and [product](index.md#product-name)
  names stable:** The app keeps its data in `%APPDATA%\<company>\<product>` and
  its console log in `%LOCALAPPDATA%\<company>\<product>`. Rename either between
  releases and the upgraded app starts with empty storage, while the old data
  stays behind in the previous folder. Set the company name before your first
  release: without one, it is *Your Company*.

<Tabs groupId="windows-packaging">
<TabItem value="inno-setup" label="Installer (Inno Setup)">

[Inno Setup](https://jrsoftware.org/isinfo.php) turns the folder into a single
`setup.exe` that installs the app, adds it to the Start menu, registers an
uninstaller under **Settings → Apps**, and upgrades an existing installation in
place.

:::note[License]
Inno Setup is free to use, commercially too. Since version 6.5, commercial users
are asked, though not required, to [buy a license](https://jrsoftware.org/isorder.php).
:::

Install Inno Setup 6.6 or later, from its
[download page](https://jrsoftware.org/isdl.php) or with winget:

```powershell
winget install --id JRSoftware.InnoSetup -e
```

This installs it for your user only, in `%LOCALAPPDATA%\Programs\Inno Setup 6`,
even from an administrator terminal. Add `--scope machine` to install it for all
users, in `C:\Program Files (x86)\Inno Setup 6`. Neither adds it to `PATH`.
Inno Setup 7 (`JRSoftware.InnoSetup.7`) compiles the script below unchanged, and
installs into an `Inno Setup 7` folder instead.

**Save** the script below as `installer.iss` in your project's root directory,
next to `pyproject.toml`, since its paths are relative to that directory. Then
**edit** the two values at the top (`AppId` and `AppExe`), and **compile** it from
that directory after each `flet build windows`:

```powershell
& "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe" installer.iss
```

Adjust the path for an all-users install or for Inno Setup 7. You can also open
the script in the Inno Setup Compiler and choose **Build → Compile**. Either way
the installer lands in `build\installer`, named after your artifact name and
version, for example `my_app-1.0.0-setup.exe`.

```iss title="installer.iss"
#define AppId "com.example.my_app" # (1)!
#define AppExe "my_app.exe" # (2)!
#define BuildDir "build\windows" # (3)!

#define AppExePath AddBackslash(SourcePath) + BuildDir + "\" + AppExe
#define ArtifactName Copy(AppExe, 1, Len(AppExe) - 4)
#if !FileExists(AppExePath) # (4)!
  #error AppExe is not in BuildDir: run "flet build windows" first, or fix the values above.
#endif
#define AppName GetStringFileInfo(AppExePath, "ProductName") # (5)!
#define AppPublisher GetStringFileInfo(AppExePath, "CompanyName")
#define FullVersion GetStringFileInfo(AppExePath, "ProductVersion")
#define AppVersion Copy(FullVersion, 1, Pos("+", FullVersion + "+") - 1) # (6)!

[Setup]
AppId={#AppId}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
VersionInfoVersion={#GetVersionNumbersString(AppExePath)} # (7)!
UninstallDisplayName={#AppName} # (8)!
UninstallDisplayIcon={app}\{#AppExe}
DefaultDirName={autopf}\{code:SafeAppName} # (9)!
DisableProgramGroupPage=yes
PrivilegesRequired=lowest # (10)!
PrivilegesRequiredOverridesAllowed=dialog
ArchitecturesAllowed=x64compatible # (11)!
ArchitecturesInstallIn64BitMode=x64compatible
WizardStyle=modern dynamic # (12)!
SetupIconFile=build\flutter\windows\runner\resources\app_icon.ico # (13)!
OutputDir=build\installer # (14)!
OutputBaseFilename={#StringChange(ArtifactName, " ", "-")}-{#AppVersion}-setup
SolidCompression=yes # (15)!

[Tasks]
Name: desktopicon; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked # (16)!

[InstallDelete]
Type: filesandordirs; Name: "{app}\app"; Check: IsUpgrade # (17)!
Type: filesandordirs; Name: "{app}\data"; Check: IsUpgrade
Type: filesandordirs; Name: "{app}\DLLs"; Check: IsUpgrade
Type: filesandordirs; Name: "{app}\Lib"; Check: IsUpgrade
Type: filesandordirs; Name: "{app}\site-packages"; Check: IsUpgrade
Type: files; Name: "{app}\*.dll"; Check: IsUpgrade

[Files]
Source: "{#BuildDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs # (18)!

[Icons]
Name: "{autoprograms}\{code:SafeAppName}"; Filename: "{app}\{#AppExe}" # (19)!
Name: "{autodesktop}\{code:SafeAppName}"; Filename: "{app}\{#AppExe}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExe}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent # (20)!

[Code]
function SafeAppName(Param: String): String; # (21)!
var
  I: Integer;
begin
  Result := '{#StringChange(AppName, "'", "''")}';
  for I := Length(Result) downto 1 do
    if Pos(Result[I], '\/:*?"<>|') > 0 then
      Delete(Result, I, 1);
end;

function IsUpgrade: Boolean; # (22)!
begin
  Result := CompareText(RemoveBackslash(WizardForm.PrevAppDir), RemoveBackslash(WizardDirValue)) = 0;
end;

function NextButtonClick(CurPageID: Integer): Boolean; # (23)!
var
  Rec: TFindRec;
begin
  Result := True;
  if (CurPageID = wpSelectDir) and not IsUpgrade and FindFirst(AddBackslash(WizardDirValue) + '*', Rec) then
  try
    repeat
      if (Rec.Name <> '.') and (Rec.Name <> '..') then
      begin
        SuppressibleMsgBox(WizardDirValue + ' already contains files. Choose an empty or new folder.', mbError, MB_OK, IDOK);
        Result := False;
        Break;
      end;
    until not FindNext(Rec);
  finally
    FindClose(Rec);
  end;
end;
```

1. **Edit this.** Identifies your app to Inno Setup: Setup uses it to find an
   existing installation to upgrade, and names the app's uninstall registry key
   after it. Any string unique to your app works, and your
   [bundle ID](index.md#bundle-id) is a natural choice. Never change it between
   releases, or the next installer registers as a separate app in
   **Settings → Apps** instead of upgrading the existing one.
2. **Edit this.** The executable's *filename* in `build\windows`: your
   [artifact name](index.md#artifact-name) plus `.exe`; `dir build\windows\*.exe`
   shows it. Set the artifact name explicitly in `pyproject.toml`, so that the
   file this script points at keeps its name.
3. Where `flet build windows` put the app, as a path relative to the script's
   own folder (`SourcePath`). Change it only if you set a different
   [output directory](index.md#output-directory).
4. Stops the compile with a clear message when the `.exe` isn't there: when
   `AppExe` is wrong, `BuildDir` isn't a relative path, or the app hasn't been
   built yet.
5. The app's name, publisher and version are read from the `.exe`, where
   `flet build` stored your [product name](index.md#product-name),
   [company name](index.md#company-name) and [build version](index.md#build-version).
   After changing them in `pyproject.toml`, run `flet build windows` again before
   compiling. Keep the names stable, though (see the rules above).
6. The `.exe` carries the version together with the build number, as
   `1.2.3+45`. This keeps the `1.2.3` that users see.
7. The numeric version, build number included (`1.2.3.45`), that Windows shows
   under **Properties → Details** of `setup.exe`.
8. The name and icon of the entry in **Settings → Apps**. Without
   `UninstallDisplayName`, Inno Setup appends the version to the name, which
   Windows already lists separately.
9. `{autopf}` is `%LOCALAPPDATA%\Programs` when installing for the current user,
   and `C:\Program Files` when installing for all users. The folder, like the
   shortcuts, is named after your product name (see 21).
10. Lets the user choose: **Install for me only** needs no administrator rights,
    while **Install for all users** asks for them. An upgrade reuses the choice
    made the first time without asking again.
11. The app is 64-bit (x64). `x64compatible` accepts x64 Windows and Windows 11
    on ARM, which runs the app under emulation (see [Windows on ARM](#windows-on-arm)).
    Without `ArchitecturesInstallIn64BitMode`, Setup runs in 32-bit mode, and an
    all-users install goes to `C:\Program Files (x86)`.
12. A modern wizard that follows Windows' light or dark mode. `dynamic` needs
    Inno Setup 6.6 or later.
13. Gives `setup.exe` your app's [icon](index.md#icons), taken from the `.ico`
    that `flet build` generates in its Flutter project. Remove the line to keep
    Inno Setup's default icon, for example when compiling where only
    `build\windows` exists.
14. Writes the installer to `build\installer`, as
    `<artifact>-<version>-setup.exe` with spaces turned into hyphens. The
    artifact name is always a valid file name, since it names the `.exe`.
15. Compresses all files as a single stream, which suits the thousands of small
    files in `Lib` and `site-packages`. A 206 MB test app compiled to a 55 MB
    installer with it, and to 61 MB without.
16. An unticked **Create a desktop shortcut** box.
17. An upgrade overwrites files, but never deletes the ones the new version no
    longer ships, so a dependency you dropped would linger: in `site-packages`,
    still importable, or as a Flutter plugin's DLL next to the `.exe`. These
    lines empty the folders that `flet build` regenerates and remove the DLLs
    next to the `.exe`, along with anything the app wrote there, before the new
    files go in. They run only when Setup installs over the app's own earlier
    installation (see 22 and 23). Don't widen them to `{app}\*`.
18. Copies the whole folder. `ignoreversion` replaces every file on upgrade;
    without it, Setup keeps an installed DLL whose version number didn't change,
    even when its contents did.
19. A Start menu shortcut, plus a desktop one when its box was ticked.
    `{autoprograms}` and `{autodesktop}` follow the install mode: the current
    user's Start menu and desktop, or every user's.
20. Adds a ticked **Launch My App** box, with your product name, to the last
    page of the wizard. The app starts as the user who ran Setup, even after an
    all-users install, and it doesn't start during an unattended install.
21. Your product name without the characters Windows doesn't allow in file
    names (`\ / : * ? " < > |`), for the install folder and the shortcuts. The
    product name is for display and may contain them: `Notes: Pro` becomes
    `Notes Pro`.
22. True when the destination is the folder of the app's earlier installation,
    as recorded by Setup, so the `[InstallDelete]` lines run only on an upgrade.
23. Keeps a first install out of a folder that already holds files, such as
    an existing folder the user picked, where the `[InstallDelete]` lines would
    later delete that folder's own `data` or `Lib`. Setup shows a message and
    stays on the folder page; an unattended install with `/DIR=` exits instead.

Your users get a familiar wizard. It installs into `%LOCALAPPDATA%\Programs` or
`C:\Program Files`, depending on their choice. Running a newer installer
upgrades in place: Setup closes the app if it is running, then replaces its
files. Uninstalling from **Settings → Apps** removes the folder and the
shortcuts, but leaves the app's data in `%APPDATA%` and `%LOCALAPPDATA%`, as
Windows apps conventionally do.

For unattended installs, for example by an IT department, Setup takes
[command-line parameters](https://jrsoftware.org/ishelp/topic_setupcmdline.htm):

```powershell
.\my_app-1.0.0-setup.exe /VERYSILENT /SUPPRESSMSGBOXES /CURRENTUSER
```

Use `/ALLUSERS`, from an administrator terminal, to install for all users.

</TabItem>
<TabItem value="zip" label="zip archive">

The simplest option is a zip file that users extract and run. There is nothing
to install, so there is no Start menu entry or uninstaller either: users delete
the folder when they are done.

```powershell
Compress-Archive -Path build\windows\* -DestinationPath build\My-App-1.0.0.zip -Force
```

This zips the folder's *contents*, so **Extract all** creates a folder named
after the zip, with the `.exe` at its top. `-Force` replaces the zip from an
earlier run, and writing it into `build` keeps it out of your next build.

Tell your users to **extract the zip before running the app**. Double-clicking
the `.exe` inside the zip makes Windows warn that the application may depend on
other compressed files. Choosing **Run** anyway copies only the `.exe` to a
temporary folder, where it fails with a `... .dll was not found` error.

Deleting the extracted folder doesn't remove the app's data, which lives in
`%APPDATA%` and `%LOCALAPPDATA%`, as for an installed app.

</TabItem>
</Tabs>

### Code signing

`flet build` doesn't sign Windows apps. Microsoft Defender SmartScreen can stop
users from running an unsigned installer or app they downloaded: it shows
**Windows protected your PC**, names an *Unknown publisher*, and runs the file
only after **More info** → **Run anyway**. A self-signed certificate changes
nothing here. A certificate from a trusted certificate authority replaces
*Unknown publisher* with your name, but the warning keeps showing until the file
or your certificate has built up reputation through downloads. EV certificates
no longer skip this. On Windows 11 PCs where Smart App Control is on, unsigned
apps can be blocked outright. See Microsoft's
[SmartScreen reputation](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation)
guide. Apps from the [Microsoft Store](#microsoft-store) are signed by Microsoft
instead.

Certificate authorities deliver code-signing certificates on a hardware token or
through a cloud signing service, not as a file. With your certificate in the
Windows certificate store, sign the app with
[`signtool`](https://learn.microsoft.com/en-us/windows/win32/seccrypto/signtool)
after each `flet build windows`, which replaces `build\windows`, and before you
compile the installer or create the zip. In PowerShell, from your project
directory:

```powershell
$signtool = (Get-ChildItem "${env:ProgramFiles(x86)}\Windows Kits\10\bin\*\x64\signtool.exe" | Select-Object -Last 1).FullName # (1)!
if (-not $signtool) { throw "signtool.exe not found: install the Windows SDK" }
$thumbprint = "<your certificate's thumbprint>" # (2)!
$unsigned = @(Get-ChildItem build\windows -Recurse -Include *.exe, *.dll, *.pyd |
    Where-Object { (Get-AuthenticodeSignature $_.FullName).Status -eq "NotSigned" }) # (3)!
for ($i = 0; $i -lt $unsigned.Count; $i += 50) { # (4)!
    & $signtool sign /fd sha256 /sha1 $thumbprint /tr http://timestamp.digicert.com /td sha256 $unsigned[$i..($i + 49)].FullName # (5)!
    if ($LASTEXITCODE -ne 0) { throw "signtool failed with exit code $LASTEXITCODE" } # (6)!
}
```

1. `signtool` is part of the Windows SDK, which the **Desktop development with
   C++** workload from [Prerequisites](#visual-studio) installs. This picks its
   newest version, and the next line stops if there is none.
2. **Edit this.** Your certificate's thumbprint.
   `Get-ChildItem Cert:\CurrentUser\My -CodeSigningCert` lists the code-signing
   certificates in your store, with their thumbprints.
3. Every `.exe`, `.dll` and `.pyd` (Python's own DLLs) that isn't signed yet.
   Smart App Control checks DLLs too, so signing the `.exe` alone isn't enough.
   The few DLLs that come signed by Microsoft, Google or the Python Software
   Foundation keep their signatures; in a test app, 104 of 116 files needed
   signing.
4. Signs 50 files per call, which keeps the command line within Windows' length
   limit when your dependencies bring hundreds of DLLs.
5. Signs with SHA-256 and adds a timestamp from DigiCert's public timestamp
   server, so the signatures stay valid after the certificate expires.
6. Stops at the first failure, such as a token that isn't plugged in, a wrong
   thumbprint or an unreachable timestamp server. `signtool` leaves the failed
   files unsigned, so fix the cause and run the block again: it picks up the
   files that are still unsigned.

To have Inno Setup sign `setup.exe` and its uninstaller too, add
`SignTool=mysign` to the script's `[Setup]` section, and define `mysign` when
you compile, in the same PowerShell session:

```powershell
& "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe" "/Smysign=`$q$signtool`$q sign /fd sha256 /sha1 $thumbprint /tr http://timestamp.digicert.com /td sha256 `$f" installer.iss
```

Inno Setup replaces `$q` with a quote and `$f` with the file to sign; the
backticks keep PowerShell from expanding them. To rehearse all of this before
you have a certificate, create a self-signed one with
`New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=My App Test" -CertStoreLocation Cert:\CurrentUser\My`.

In CI, where you can't plug in a token,
[Artifact Signing](https://learn.microsoft.com/en-us/azure/artifact-signing/overview),
Microsoft's cloud signing service, works with the same `signtool` command:
replace `/sha1 $thumbprint` with the `/dlib` and `/dmdf` options from its
[signtool guide](https://learn.microsoft.com/en-us/azure/artifact-signing/how-to-signing-integrations).

### Building the installer in CI

GitHub-hosted Windows runners come with Inno Setup 6 installed and `iscc` on
`PATH`. In a workflow like the one under [GitHub Actions](index.md#github-actions),
add these steps after the step that builds the app:

```yaml
- name: Build installer
  if: runner.os == 'Windows' # (1)!
  run: iscc installer.iss

- name: Upload installer
  if: runner.os == 'Windows'
  uses: actions/upload-artifact@v7
  with:
    name: windows-installer
    path: build/installer/*.exe
    if-no-files-found: error
```

1. Skips both steps in the jobs that build for other platforms.

## Microsoft Store

The [Microsoft Store](https://apps.microsoft.com) installs desktop apps packaged
as [MSIX](https://learn.microsoft.com/en-us/windows/msix/overview): your
`build\windows` folder plus a manifest that describes the app to Windows.
Microsoft signs the package once it passes certification, so you need no
code-signing certificate, and the Store keeps installed copies up to date. The
Store also accepts EXE and MSI installers, such as one made with Inno Setup, but
only when they are signed with a certificate from a trusted certificate
authority, install silently, and are hosted by you at a fixed URL per version (see
[MSI/EXE requirements](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msi/app-package-requirements)).

`flet build` doesn't create MSIX packages yet. You create one from
`build\windows` with the manifest and the packing script below, which runs
MakeAppx from the Windows SDK that the **Desktop development with C++** workload
from [Prerequisites](#visual-studio) installs.

### Store prerequisites

One-time setup, requiring a Microsoft Store developer account.

#### Creating a developer account

Registration is free. Start it at
[storedeveloper.microsoft.com](https://storedeveloper.microsoft.com): other
ways into Partner Center, Microsoft's publishing portal, lead to an older
sign-up flow. Choose the account type carefully, because an individual account
can't be converted to a company account later:

- **Individual:** for publishing under your own name. You sign in with a
  personal Microsoft account and verify your identity with a government-issued
  photo ID and a selfie.
- **Company:** required for an organization, when you publish as part of your
  trade or profession, and when your app's or publisher's name would read as a
  business's (Store policy
  [10.14](https://learn.microsoft.com/en-us/windows/apps/publish/store-policies#1014-account-type)).
  You sign up with a work email address on your organization's domain, and
  verify the company with a D-U-N-S number, usually within minutes, or with
  business documents, which take a few business days.

See [Open a developer account](https://learn.microsoft.com/en-us/windows/apps/publish/partner-center/open-a-developer-account)
for the details.

#### Reserving the app's name

In [Partner Center](https://partner.microsoft.com/dashboard/apps-and-games),
go to **Apps and games** → **+ New product** → **MSIX or PWA app**, enter your
app's name, then **Check availability** → **Reserve product name**. The name is
reserved for three months; submit the app within that time to keep it.

Then open **Product management** → **Product identity**. Three of its values go
into the [manifest](#creating-the-package) exactly as shown, matching case,
spaces and punctuation:

- `Package/Identity/Name`
- `Package/Identity/Publisher`, a `CN=...` value
- `Package/Properties/PublisherDisplayName`

### Creating the package

Two files describe and build the package: a manifest and a packing script. Save
both in an `msix` folder in your project's root directory, next to
`pyproject.toml`. In the standard [project structure](index.md#project-structure),
where your app's code lives in `src`, `flet build` leaves that folder out of the
app. If your code sits in the root directory instead, add `"msix"` to your
[excluded files](index.md#excluding-files-and-directories).

**Save** the manifest below as `msix\AppxManifest.xml`, then **edit** the values
marked in the annotations. In XML, write a `&` in any of them as `&amp;`.

```xml title="msix\AppxManifest.xml"
<?xml version="1.0" encoding="utf-8"?>
<Package
  xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10"
  xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10"
  xmlns:rescap="http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities"
  IgnorableNamespaces="uap rescap">
  <Identity
    Name="YourPublisher.MyApp" # (1)!
    Publisher="CN=00000000-0000-0000-0000-000000000000"
    Version="1.0.0.0" # (2)!
    ProcessorArchitecture="x64" /> # (3)!
  <Properties>
    <DisplayName>My App</DisplayName> # (4)!
    <PublisherDisplayName>Your Name</PublisherDisplayName>
    <Logo>Images\StoreLogo.png</Logo>
  </Properties>
  <Dependencies>
    <TargetDeviceFamily Name="Windows.Desktop" MinVersion="10.0.17763.0" MaxVersionTested="10.0.26100.0" /> # (5)!
  </Dependencies>
  <Resources>
    <Resource Language="en-us" /> # (6)!
  </Resources>
  <Capabilities>
    <rescap:Capability Name="runFullTrust" /> # (7)!
  </Capabilities>
  <Applications>
    <Application Id="App" Executable="my_app.exe" EntryPoint="Windows.FullTrustApplication"> # (8)!
      <uap:VisualElements
        DisplayName="My App" # (9)!
        Description="My App"
        BackgroundColor="transparent"
        Square150x150Logo="Images\Square150x150Logo.png"
        Square44x44Logo="Images\Square44x44Logo.png" /> # (10)!
    </Application>
  </Applications>
</Package>
```

1. **Edit this and the next line.** `Package/Identity/Name` and
   `Package/Identity/Publisher` from your app's
   [Product identity](#reserving-the-apps-name) page, copied exactly. Together
   they identify the package: the Store accepts uploads only when they match.
2. A placeholder: the [packing script](#creating-the-package) replaces it with
   your app's [build version](index.md#build-version) followed by `.0`. MSIX
   versions have four numbers, the Store reserves the fourth, and the first
   can't be `0`, so use a build version such as `1.0.0`: `flet create` starts
   new projects at `0.1.0`. Raise it for every submission, since a version can't
   be uploaded twice and users only receive a higher version as an update.
3. `flet build windows` builds an x64 app, which Windows 11 on ARM runs under
   emulation (see [Windows on ARM](#windows-on-arm)).
4. **Edit this and the next line.** The name you reserved, which the Store
   checks, and `Package/Properties/PublisherDisplayName` from the Product
   identity page.
5. Windows 10 version 1809 or later. `MaxVersionTested` is the newest Windows
   version you tested the app on; Windows 11 version 24H2 here.
6. The language of the package. Partner Center starts your Store listing in it;
   you can add listings in other languages.
7. Lets the app run as a regular desktop app, like the unpackaged
   `build\windows` folder does. It is a *restricted* capability: you explain
   why the app needs it when you [submit](#submitting-the-app) it.
8. **Edit this.** Your executable's filename in `build\windows`, your
   [artifact name](index.md#artifact-name) plus `.exe`; `dir build\windows\*.exe`
   shows it. `Windows.FullTrustApplication` starts it as a desktop app.
9. **Edit this.** The name shown in the Start menu, normally the name you
   reserved, and a short description of the app.
10. The app's tiles and icons in the Start menu, taskbar and **Settings → Apps**,
    from the images the packing script creates in `Images`. `transparent` shows
    them without a colored plate.

If your app records audio or uses the device's location, for example with
`flet-audio-recorder` or `flet-geolocator`, also declare
`<DeviceCapability Name="microphone" />` or `<DeviceCapability Name="location" />`
after the `runFullTrust` line, so that Windows lists your app on the matching
**Settings → Privacy & security** page from the start. See
[App capability declarations](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/app-capability-declarations).

**Save** the script below as `msix\pack.ps1`:

```powershell title="msix\pack.ps1"
$ErrorActionPreference = "Stop" # (1)!
Set-Location (Split-Path $PSScriptRoot) # (2)!

$manifest = New-Object xml
$manifest.Load("$PWD\msix\AppxManifest.xml")
$exe = Get-Item "build\windows\$($manifest.Package.Applications.Application.Executable)" # (3)!
$version = ($exe.VersionInfo.ProductVersion -split "\+")[0] + ".0" # (4)!
if ($version -notmatch "^[1-9]\d*\.\d+\.\d+\.0$") { throw "Version $version isn't valid for the Store: use a build version such as 1.0.0" }
$manifest.Package.Identity.Version = $version

$makeappx = (Get-ChildItem "${env:ProgramFiles(x86)}\Windows Kits\10\bin\*\x64\makeappx.exe" | Select-Object -Last 1).FullName # (5)!
if (-not $makeappx) { throw "makeappx.exe not found: install the Windows SDK" }

if (Test-Path build\msix) { Remove-Item build\msix -Recurse -Force } # (6)!
Copy-Item build\windows build\msix -Recurse
$manifest.Save("$PWD\build\msix\AppxManifest.xml")

Add-Type -AssemblyName System.Drawing
$ico = [IO.File]::ReadAllBytes("$PWD\build\flutter\windows\runner\resources\app_icon.ico") # (7)!
$entry = 0..($ico[4] - 1) | ForEach-Object { 6 + 16 * $_ } | Sort-Object { if ($ico[$_]) { $ico[$_] } else { 256 } } | Select-Object -Last 1
$icon = [System.Drawing.Image]::FromStream([IO.MemoryStream]::new($ico, [BitConverter]::ToInt32($ico, $entry + 12), [BitConverter]::ToInt32($ico, $entry + 8)))
New-Item build\msix\Images -ItemType Directory | Out-Null
foreach ($image in @{ Square44x44Logo = 44; Square150x150Logo = 150; StoreLogo = 50 }.GetEnumerator()) { # (8)!
    $bitmap = New-Object System.Drawing.Bitmap $image.Value, $image.Value
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.InterpolationMode = "HighQualityBicubic"
    $graphics.DrawImage($icon, 0, 0, $image.Value, $image.Value)
    $bitmap.Save("$PWD\build\msix\Images\$($image.Key).png", [System.Drawing.Imaging.ImageFormat]::Png)
    $graphics.Dispose(); $bitmap.Dispose()
}
$icon.Dispose()

& $makeappx pack /d build\msix /p "build\$($exe.BaseName)-$version.msix" /o # (9)!
if ($LASTEXITCODE -ne 0) { throw "makeappx failed with exit code $LASTEXITCODE" }
```

1. Stops the script at the first error, so that the steps after a failed one
   can't produce a broken package.
2. Works in your project's root directory, the folder that contains `msix`,
   wherever you start the script from.
3. The executable named in the manifest. The script stops here when the name is
   wrong or the app isn't built yet.
4. The [build version](index.md#build-version) that `flet build` stored in the
   `.exe`, without the build number: `1.2.3+45` becomes `1.2.3.0`. The next line
   stops on a version the Store doesn't accept (see the manifest's `Version`).
5. MakeAppx is part of the Windows SDK. This picks its newest version, and the
   next line stops if there is none.
6. Assembles the package's contents in `build\msix`: a fresh copy of
   `build\windows` and the manifest with the version filled in. The script stops
   if a file in an earlier `build\msix` is in use, for example by the app you
   registered from it for [testing](#testing-the-package-locally).
7. Your app's [icon](index.md#icons), whatever its source format: the largest
   image, 256 × 256 pixels, in the `.ico` file that `flet build` generated for
   the `.exe`.
8. The three images the manifest names, in `build\msix\Images`.
9. Packs `build\msix` into `build\<artifact>-<version>.msix`, for example
   `build\my_app-1.0.0.0.msix`, replacing an earlier one. The package is
   unsigned, which is what the Store expects.

After each `flet build windows`, run the script from your project's root
directory:

```powershell
powershell -ExecutionPolicy Bypass -File msix\pack.ps1
```

`-ExecutionPolicy Bypass` lets Windows PowerShell run the script without
changing your PC's [execution policy](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies),
which blocks scripts by default.

### Testing the package locally

Windows installs only signed `.msix` files, so double-clicking yours fails.
Instead, with [Developer Mode](https://learn.microsoft.com/en-us/windows/apps/get-started/enable-your-device-for-development)
on, which `flet build windows` normally needs too, register the contents of
`build\msix` as a packaged app, from Windows PowerShell:

```powershell
Add-AppxPackage -Register build\msix\AppxManifest.xml
```

Start the app from the Start menu, where it appears under its display name. It
runs from `build\msix` with the package's identity, so its data goes where a
Store install's does (see [below](#how-the-store-app-behaves)), but unlike a
Store install's folder, `build\msix` stays writable. Close the app before you
pack again. To test a changed manifest, and before installing the app from the
Store, unregister it first, using your `Package/Identity/Name`:

```powershell
Get-AppxPackage YourPublisher.MyApp | Remove-AppxPackage
```

To catch technical problems before certification does, run Microsoft's
technical tests yourself with the
[Windows App Certification Kit](https://learn.microsoft.com/en-us/windows/uwp/debug-test-perf/windows-app-certification-kit)
(WACK). It isn't part of the C++ workload: install it with the
[Windows SDK](https://developer.microsoft.com/windows/downloads/windows-sdk/)
installer by selecting **Windows App Certification Kit**. Then, from an
administrator PowerShell in your project's root directory:

```powershell
$appcert = "${env:ProgramFiles(x86)}\Windows Kits\10\App Certification Kit\appcert.exe"
$package = Get-ChildItem build\*.msix | Sort-Object LastWriteTime | Select-Object -Last 1 # (1)!
Remove-Item build\wack-report.xml -ErrorAction SilentlyContinue # (2)!
& $appcert reset # (3)!
& $appcert test -appxpackagepath $package.FullName -reportoutputpath "$PWD\build\wack-report.xml"
```

1. The package you packed last.
2. WACK doesn't overwrite an earlier report: it stops instead, and the old
   report stays.
3. Clears the state of an earlier test run.

The report's `OVERALL_RESULT` should be `PASS`. A Flet app also fails three
optional tests, which don't change that result: **Debug configuration** (the
Python runtime ships debug builds of some modules), **Archive files usage**
(compressed files, such as Flutter's license notices) and **Blocked
executables** (references to `cmd` or `powershell` inside Python and Flutter).
Certification also reviews your app and its listing by hand, which WACK can't.

### How the Store app behaves

Installed from the Store, the app differs from the `build\windows` folder in a
few ways:

- **Its folder is read-only.** Windows installs it under
  `C:\Program Files\WindowsApps`, in a new folder for each version. Flet writes
  nothing there; make sure your code doesn't either (see the
  [rules](#distributing) for every format).
- **Its data is private to the package.** Windows redirects the files and
  folders the app creates under `%APPDATA%` and `%LOCALAPPDATA%`, such as its
  storage and console log, to
  `%LOCALAPPDATA%\Packages\<package family name>\LocalCache`. The app reads and
  writes the usual paths, but other programs, including File Explorer, find
  these files only in that folder: for example the console log in
  `LocalCache\Local\<company>\<product>\console.log`. Uninstalling the app
  deletes them. Files that already existed in the real folders, for example from
  running `build\windows` on the same PC, are used in place instead, and stay
  after uninstalling. `Get-AppxPackage YourPublisher.MyApp` shows the package
  family name.
- **Its name and icons come from the manifest,** not from the `.exe`.

### Submitting the app

Upload the `.msix` in a submission, in Partner Center: on your app's overview
page, select **Start submission**, then complete each section. The sections
most specific to a Flet app are:

- **Pricing and availability:** to try the whole process before your app is
  public, set **Visibility** → **Audience** to **Private audience**, with a
  group of testers' personal Microsoft accounts; work and school accounts can't
  install the app. Testers install it from the private link shown there. The
  audience defaults to public, and once you have submitted with the public
  audience, the app can't be made private again. See
  [Visibility options](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/visibility-options).
- **Properties:** a privacy policy is required for desktop apps (Store policy
  [10.5.1](https://learn.microsoft.com/en-us/windows/apps/publish/store-policies#105-personal-information)),
  even when your app collects nothing. Enter its URL, or paste its text.
- **Packages:** upload the `.msix`. Partner Center validates it right away, and
  rejects a package whose identity or name doesn't match your
  [reservation](#reserving-the-apps-name).
- **Store listings:** a description, at least one screenshot (PNG, 1366 × 768
  pixels or larger) and, recommended, a 300 × 300 pixel PNG of your icon as the
  1:1 app tile icon.
- **Submission options:** under **Restricted capabilities**, explain why the
  app needs `runFullTrust`, for example:

  ```text
  This is a desktop app built with Flet: a Flutter user interface with an
  embedded Python runtime, packaged as a full-trust Win32 app. Its executable
  is a regular Win32 process that can't run in an AppContainer, so it needs
  runFullTrust to start. The app doesn't request elevation, install services
  or drivers, or change system settings.
  ```

  Under **Notes for certification**, tell the testers how to use your app,
  including test credentials if it needs an account.

Select **Submit for certification**. Certification takes up to three business
days; if your app fails, its report says why. Microsoft's list of
[common certification failures](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msix/resolve-submission-errors#avoid-common-certification-failures)
is worth reading before you submit, and the
[Store policies](https://learn.microsoft.com/en-us/windows/apps/publish/store-policies)
are what your app is checked against.

### Updating the app

To release an update, raise your [build version](index.md#build-version), run
`flet build windows` and the [packing script](#creating-the-package), and upload
the new `.msix` in a new submission. The Store then delivers it to your users.
Once your first submission is published, the
[Microsoft Store Developer CLI](https://learn.microsoft.com/en-us/windows/apps/publish/msstore-dev-cli/overview)
can upload new versions from CI; it signs in with a Microsoft Entra ID
application linked to your Partner Center account.

## Troubleshooting

| Symptom                                           | Cause and fix                                                                                                                                                    |
|---------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Building with plugins requires symlink support`  | Windows **Developer Mode** is off — run `start ms-settings:developers`, enable it (see [this guide](https://stackoverflow.com/a/70994092/1435891)), and rebuild. |
| `Unable to find suitable Visual Studio toolchain` | The **Desktop development with C++** workload is missing — install it with the Visual Studio Installer (see [Prerequisites](#visual-studio)).                    |
| The app window never appears, stays blank, or renders slowly | Impeller, the default renderer, misbehaves with some GPUs, drivers and virtual machines — set [`FLET_NO_IMPELLER=1`](../reference/environment-variables.md#flet_no_impeller) or build with `--no-impeller` to render with Skia. See [Renderer](index.md#renderer). |
| Setup stops with `DeleteFile failed; code 5. Access is denied.` while upgrading | The app is still running and Setup couldn't close it — close the app and click **Try again**. Setup normally closes it for you, but not when installing for the current user on [Windows on ARM](#windows-on-arm), where Windows' x64 emulation service holds the app's files too. |
| **Windows protected your PC** when users run your installer | The installer is unsigned, or signed with a certificate that hasn't earned SmartScreen reputation yet — see [Code signing](#code-signing). |
| `Value of [Setup] section directive "SignTool" is invalid` | The script names a sign tool that the compile command doesn't define — pass `/S<name>=...` to `ISCC.exe`, or remove the `SignTool` line for unsigned builds. See [Code signing](#code-signing). |
| The packing script stops with `Access to the path '<file>' is denied.` | The app you registered for [testing](#testing-the-package-locally) is still running from `build\msix` — close it and pack again. |
| `Add-AppxPackage -Register` fails with `0x80073CFB` and `reinstallation of the package was blocked` | The registered package has the same version but a different manifest — unregister it with `Get-AppxPackage <Package/Identity/Name> \| Remove-AppxPackage`, then register it again. |
| Partner Center rejects the package: `The name found in the package is not one of your reserved app names` | The manifest's `<DisplayName>` under `<Properties>` isn't a name you reserved — set it, and the `DisplayName` of `uap:VisualElements`, to your reserved name, pack again and upload the new `.msix`. See [Creating the package](#creating-the-package). |
