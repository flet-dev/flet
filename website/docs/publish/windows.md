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
though, so wrap it in one of the formats below.

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
the installer lands in `build\installer`, named after your product and version,
for example `My-App-1.0.0-setup.exe`.

```iss title="installer.iss"
#define AppId "com.example.my_app" # (1)!
#define AppExe "my_app.exe" # (2)!
#define BuildDir "build\windows" # (3)!

#define AppExePath AddBackslash(SourcePath) + BuildDir + "\" + AppExe
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
DefaultDirName={autopf}\{#AppName} # (9)!
DisableProgramGroupPage=yes
PrivilegesRequired=lowest # (10)!
PrivilegesRequiredOverridesAllowed=dialog
ArchitecturesAllowed=x64compatible # (11)!
ArchitecturesInstallIn64BitMode=x64compatible
WizardStyle=modern dynamic # (12)!
SetupIconFile=build\flutter\windows\runner\resources\app_icon.ico # (13)!
OutputDir=build\installer # (14)!
OutputBaseFilename={#StringChange(AppName, " ", "-")}-{#AppVersion}-setup
SolidCompression=yes # (15)!

[Tasks]
Name: desktopicon; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked # (16)!

[InstallDelete]
Type: filesandordirs; Name: "{app}\app"; Check: IsUpgrade # (17)!
Type: filesandordirs; Name: "{app}\data"; Check: IsUpgrade
Type: filesandordirs; Name: "{app}\DLLs"; Check: IsUpgrade
Type: filesandordirs; Name: "{app}\Lib"; Check: IsUpgrade
Type: filesandordirs; Name: "{app}\site-packages"; Check: IsUpgrade

[Files]
Source: "{#BuildDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs # (18)!

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppExe}" # (19)!
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExe}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExe}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent # (20)!

[Code]
function IsUpgrade: Boolean; # (21)!
begin
  Result := CompareText(RemoveBackslash(WizardForm.PrevAppDir), RemoveBackslash(WizardDirValue)) = 0;
end;

function NextButtonClick(CurPageID: Integer): Boolean; # (22)!
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
   and `C:\Program Files` when installing for all users.
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
    `<product>-<version>-setup.exe` with spaces turned into hyphens.
15. Compresses all files as a single stream, which suits the thousands of small
    files in `Lib` and `site-packages`. A 206 MB test app compiled to a 55 MB
    installer with it, and to 61 MB without.
16. An unticked **Create a desktop shortcut** box.
17. An upgrade overwrites files, but never deletes the ones the new version no
    longer ships, so a dependency you dropped would linger in `site-packages`,
    still importable. These lines empty the folders that `flet build`
    regenerates, before the new files go in, along with anything the app wrote
    there. They run only when Setup installs over the app's own earlier
    installation (see 21 and 22). Don't widen them to `{app}\*`.
18. Copies the whole folder. `ignoreversion` replaces every file on upgrade;
    without it, Setup keeps an installed DLL whose version number didn't change,
    even when its contents did.
19. A Start menu shortcut, plus a desktop one when its box was ticked.
    `{autoprograms}` and `{autodesktop}` follow the install mode: the current
    user's Start menu and desktop, or every user's.
20. Adds a ticked **Launch My App** box, with your product name, to the last
    page of the wizard. The app starts as the user who ran Setup, even after an
    all-users install, and it doesn't start during an unattended install.
21. True when the destination is the folder of the app's earlier installation,
    as recorded by Setup, so the `[InstallDelete]` lines run only on an upgrade.
22. Keeps a first install out of a folder that already holds files, such as
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
.\My-App-1.0.0-setup.exe /VERYSILENT /SUPPRESSMSGBOXES /CURRENTUSER
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
guide.

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

## Troubleshooting

| Symptom                                           | Cause and fix                                                                                                                                                    |
|---------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Building with plugins requires symlink support`  | Windows **Developer Mode** is off — run `start ms-settings:developers`, enable it (see [this guide](https://stackoverflow.com/a/70994092/1435891)), and rebuild. |
| `Unable to find suitable Visual Studio toolchain` | The **Desktop development with C++** workload is missing — install it with the Visual Studio Installer (see [Prerequisites](#visual-studio)).                    |
| The app window never appears, stays blank, or renders slowly | Impeller, the default renderer, misbehaves with some GPUs, drivers and virtual machines — set [`FLET_NO_IMPELLER=1`](../reference/environment-variables.md#flet_no_impeller) or build with `--no-impeller` to render with Skia. See [Renderer](index.md#renderer). |
| Setup stops with `DeleteFile failed; code 5. Access is denied.` while upgrading | The app is still running and Setup couldn't close it — close the app and click **Try again**. Setup normally closes it for you, but not when installing for the current user on [Windows on ARM](#windows-on-arm), where Windows' x64 emulation service holds the app's files too. |
| **Windows protected your PC** when users run your installer | The installer is unsigned, or signed with a certificate that hasn't earned SmartScreen reputation yet — see [Code signing](#code-signing). |
| `Value of [Setup] section directive "SignTool" is invalid` | The script names a sign tool that the compile command doesn't define — pass `/S<name>=...` to `ISCC.exe`, or remove the `SignTool` line for unsigned builds. See [Code signing](#code-signing). |
