---
title: "Packaging app for macOS"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';

Instructions for packaging a Flet app into a macOS application bundle.

:::tip[Info]
This guide provides detailed macOS-specific information.
Complementary and more general information is available [here](index.md).
:::

## Prerequisites

### Rosetta 2

[Flutter](https://flutter.dev), which we use for packaging,
requires [Rosetta 2](https://support.apple.com/en-us/HT211861) on Apple Silicon:

```bash
sudo softwareupdate --install-rosetta --agree-to-license
```

### Xcode

[Xcode](https://developer.apple.com/xcode/) 15 or later is required to compile
native Swift or Objective-C code.

### CocoaPods

[CocoaPods](https://cocoapods.org/) 1.16 or later is required to install and
compile Flutter plugins.

## `flet build macos`

:::note[Note]
This command can be run on **macOS only**.
:::

Builds a macOS application bundle from your Flet app.

## Target architecture

By default, `flet build macos` creates a universal bundle that runs on both
Apple Silicon and Intel Macs. Packaging downloads Python wheels for both
`arm64` and `x86_64` architectures.

To limit packaging to a specific architecture, see [this](index.md#target-architecture).
This affects which Python wheels are bundled and, in turn, which CPU architectures the app will run on.
You will then have to provide your users with the correct build for their Macs.

## Permissions

macOS permissions are declared through [`Info.plist`](#infoplist) privacy usage strings and
app [entitlements](#entitlements). You can also use the [cross-platform permission bundles](index.md#predefined-cross-platform-permission-bundles)
to inject common entries, then override or extend them with platform-specific values.

### Info.plist

Add or override `Info.plist` entries for macOS builds.
These values are written to `macos/Runner/Info.plist` of the [build project](index.md#build-template).

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--info-plist`](../cli/flet-build.md#--info-plist)
2. `[tool.flet.macos.info]`
3. Values injected by [cross-platform permission bundles](index.md#permissions), if any.

#### Supported value forms

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
Accepts repeated `<key>=<value>` entries.
The `<value>` can be in one of the following forms:

- `true` or `false` (case-insensitive) for boolean values
- integer and real number literals, for example `32` or `0.5`
- TOML array literals, for example `["basic", "advanced"]`
- TOML inline tables, for example `{ NSAllowsArbitraryLoads = false }`
- any other value is treated as a string
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
Both simple and complex structures are supported:

- string
- boolean
- integer
- real
- dictionary (nested key-value object)
- array of strings
- array of booleans
- array of integers
- array of reals
- array of dictionaries (including dictionaries that contain arrays)
</TabItem>
</Tabs>
#### Example

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build macos \
  --info-plist LSApplicationCategoryType="public.app-category.utilities" \
  --info-plist NSSupportsSuddenTermination=true \
  --info-plist ExampleInteger=32 \
  --info-plist ExampleReal=0.5 \
  --info-plist 'SupportedModes=["basic", "advanced"]' \
  --info-plist 'FeatureFlags=[true, false]' \
  --info-plist 'RetryDelays=[1, 2, 3]' \
  --info-plist 'OpacitySteps=[0.25, 0.5, 0.75]' \
  --info-plist 'NSAppTransportSecurity={ NSAllowsArbitraryLoads = false }' \
  --info-plist 'CFBundleDocumentTypes=[{ CFBundleTypeName = "Data File", CFBundleTypeExtensions = ["dat"] }, { CFBundleTypeName = "JSON File", CFBundleTypeExtensions = ["json"] }]'
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.macos.info]
LSApplicationCategoryType = "public.app-category.utilities"
NSSupportsSuddenTermination = true
ExampleInteger = 32
ExampleReal = 0.5
SupportedModes = ["basic", "advanced"]
FeatureFlags = [true, false]
RetryDelays = [1, 2, 3]
OpacitySteps = [0.25, 0.5, 0.75]
NSAppTransportSecurity = { NSAllowsArbitraryLoads = false }
CFBundleDocumentTypes = [
  { CFBundleTypeName = "Data File", CFBundleTypeExtensions = ["dat"] },
  { CFBundleTypeName = "JSON File", CFBundleTypeExtensions = ["json"] },
]
```
</TabItem>
</Tabs>
<details>
<summary>Template translation</summary>

In the [`macos/Runner/Info.plist`](index.md#build-template), the
example above will be translated accordingly into this:

```xml
<plist version="1.0">
	<dict>

        <key>LSApplicationCategoryType</key>
        <string>public.app-category.utilities</string>

        <key>NSSupportsSuddenTermination</key>
        <true/>

        <key>ExampleInteger</key>
        <integer>32</integer>

        <key>ExampleReal</key>
        <real>0.5</real>

        <key>SupportedModes</key>
        <array>
            <string>basic</string>
            <string>advanced</string>
        </array>

        <key>FeatureFlags</key>
        <array>
            <true/>
            <false/>
        </array>

        <key>RetryDelays</key>
        <array>
            <integer>1</integer>
            <integer>2</integer>
            <integer>3</integer>
        </array>

        <key>OpacitySteps</key>
        <array>
            <real>0.25</real>
            <real>0.5</real>
            <real>0.75</real>
        </array>

        <key>NSAppTransportSecurity</key>
        <dict>
            <key>NSAllowsArbitraryLoads</key>
            <false/>
        </dict>

        <key>CFBundleDocumentTypes</key>
        <array>
            <dict>
                <key>CFBundleTypeName</key>
                <string>Data File</string>
                <key>CFBundleTypeExtensions</key>
                <array>
                    <string>dat</string>
                </array>
            </dict>
            <dict>
                <key>CFBundleTypeName</key>
                <string>JSON File</string>
                <key>CFBundleTypeExtensions</key>
                <array>
                    <string>json</string>
                </array>
            </dict>
        </array>

	</dict>
</plist>
```
</details>

### Entitlements

Entitlements are property-list key-value pairs that grant an executable permission
to use a service or technology. The supported value type depends on the entitlement
key defined in the
[Apple Developer Entitlements Reference](https://developer.apple.com/documentation/bundleresources/entitlements).

Entitlements are written to `macos/Runner/DebugProfile.entitlements` and
`macos/Runner/Release.entitlements` in the [build template](index.md#build-template).

#### Resolution order

Its value is determined in the following order of precedence:

1. [`--macos-entitlements`](../cli/flet-build.md#--macos-entitlements)
2. `[tool.flet.macos.entitlement]`
3. Values injected by [cross-platform permission bundles](index.md#permissions), if any.
4. Defaults:

    ```toml
    [tool.flet.macos.entitlement]
    "com.apple.security.app-sandbox" = false
    "com.apple.security.cs.allow-jit" = true
    "com.apple.security.cs.allow-unsigned-executable-memory" = true
    "com.apple.security.network.client" = true
    "com.apple.security.network.server" = true
    "com.apple.security.files.user-selected.read-write" = true
    ```

    :::note
    `com.apple.security.cs.allow-unsigned-executable-memory` is required for
    `ctypes`/`cffi` callbacks to work on Intel Macs when the app is signed with
    the [hardened runtime](#code-signing) (Apple's `libffi` allocates
    writable-and-executable closure memory on `x86_64`). Apple Silicon is
    unaffected. Set it to `false` if your app targets only `arm64` and you
    want the strictest hardened runtime.
    :::

#### Supported value forms

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
Accepts repeated `<key>=<value>` entries.
The `<value>` can be in one of the following forms:

- `true` or `false` (case-insensitive) for boolean values
- integer and real number literals, for example `32` or `0.5`
- TOML array literals, for example `["group.example.one", "group.example.two"]`
- TOML inline tables, for example `{ "com.apple.mail" = ["compose"] }`
- any other value is treated as a string
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
Both simple and complex structures are supported:

- string
- boolean
- integer
- real
- dictionary (nested key-value object)
- array of strings
- array of booleans
- array of integers
- array of reals
- array of dictionaries (including dictionaries that contain arrays)
</TabItem>
</Tabs>
#### Example

<Tabs groupId="flet-build--pyproject-toml">
<TabItem value="flet-build" label="flet build">
```bash
flet build macos \
  --macos-entitlements com.apple.security.network.client=true \
  --macos-entitlements com.apple.developer.ubiquity-kvstore-identifier=ABCDE12345.dev.example.myapp \
  --macos-entitlements ExampleInteger=32 \
  --macos-entitlements ExampleReal=0.5 \
  --macos-entitlements 'com.apple.security.application-groups=["group.dev.example.myapp", "group.dev.example.shared"]' \
  --macos-entitlements 'ExampleBooleanArray=[true, false]' \
  --macos-entitlements 'com.apple.security.scripting-targets={ "com.apple.mail" = ["compose", "send"] }' \
  --macos-entitlements 'ExampleArrayOfDictionaries=[{ Name = "alpha", Enabled = true }, { Name = "beta", Enabled = false }]'
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.macos.entitlement]
"com.apple.security.network.client" = true
"com.apple.developer.ubiquity-kvstore-identifier" = "ABCDE12345.dev.example.myapp"
ExampleInteger = 32
ExampleReal = 0.5
"com.apple.security.application-groups" = [
  "group.dev.example.myapp",
  "group.dev.example.shared",
]
ExampleBooleanArray = [true, false]
"com.apple.security.scripting-targets" = { "com.apple.mail" = ["compose", "send"] }
ExampleArrayOfDictionaries = [
  { Name = "alpha", Enabled = true },
  { Name = "beta", Enabled = false },
]
```
</TabItem>
</Tabs>
<details>
<summary>Template translation</summary>

In both [`macos/Runner/DebugProfile.entitlements`](index.md#build-template) and
[`macos/Runner/Release.entitlements`](index.md#build-template), the example above
will be translated accordingly into this:

```xml
<key>com.apple.security.network.client</key>
<true />
<key>com.apple.developer.ubiquity-kvstore-identifier</key>
<string>ABCDE12345.dev.example.myapp</string>
<key>ExampleInteger</key>
<integer>32</integer>
<key>ExampleReal</key>
<real>0.5</real>
<key>com.apple.security.application-groups</key>
<array>
    <string>group.dev.example.myapp</string>
    <string>group.dev.example.shared</string>
</array>
<key>ExampleBooleanArray</key>
<array>
    <true />
    <false />
</array>
<key>com.apple.security.scripting-targets</key>
<dict>
    <key>com.apple.mail</key>
    <array>
        <string>compose</string>
        <string>send</string>
    </array>
</dict>
<key>ExampleArrayOfDictionaries</key>
<array>
    <dict>
        <key>Name</key>
        <string>alpha</string>
        <key>Enabled</key>
        <true />
    </dict>
    <dict>
        <key>Name</key>
        <string>beta</string>
        <key>Enabled</key>
        <false />
    </dict>
</array>
```
</details>

## Code signing

By default, the built app bundle is **ad-hoc signed**: it runs fine on the Mac
that built it, but when other users *download* it, macOS Gatekeeper steps in.
Since macOS 15 (Sequoia), there is no Control-click bypass anymore — users must
approve every blocked item in **System Settings → Privacy & Security → Open
Anyway** with an administrator password, and a Python app can trigger this
per bundled library. For public distribution, sign your app with a
**Developer ID Application** certificate and [notarize](#notarization) it.

### Prerequisites

1. An [Apple Developer Program](https://developer.apple.com/programs/) membership.
2. A **Developer ID Application** certificate
   ([create one](https://developer.apple.com/account/resources/certificates/list),
   then install it — with its private key — into your login keychain).
   Verify with:

   ```bash
   security find-identity -v -p codesigning
   ```

### Signing the app

<Tabs groupId="flet-build--pyproject-toml--env">
<TabItem value="flet-build" label="flet build">
```bash
flet build macos --macos-signing-identity "Developer ID Application: Jane Doe (TEAM123456)"
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.macos.signing]
identity = "Developer ID Application: Jane Doe (TEAM123456)"
```
</TabItem>
<TabItem value="env" label="env var">
```dotenv
FLET_MACOS_SIGNING_IDENTITY="Developer ID Application: Jane Doe (TEAM123456)"
```
</TabItem>
</Tabs>

The identity may be the exact certificate name, its SHA-1 fingerprint, or a
unique substring (for example, just the team ID). Passing `"-"` produces an
explicit ad-hoc signature.

#### Resolution order

The signing identity is determined in the following order of precedence:

1. [`--macos-signing-identity`](../cli/flet-build.md#--macos-signing-identity)
2. `[tool.flet.macos.signing].identity`
3. [`FLET_MACOS_SIGNING_IDENTITY`](../reference/environment-variables.md#flet_macos_signing_identity)
   environment variable
4. Default: none — a plain build keeps its ad-hoc signature and no signing
   step runs, while [notarize](#notarization) and
   [App Store](#mac-app-store) builds
   [auto-discover](#identity-auto-discovery) the certificate.

When a real identity is configured, `flet build macos` will, after the build:

1. Sign every bundled binary — including the embedded Python runtime and all
   native modules from your dependencies — "inside out", as
   [Apple requires](https://developer.apple.com/documentation/xcode/creating-distribution-signed-code-for-macos),
   with the **hardened runtime** enabled and a secure timestamp (both required
   for notarization). [Entitlements](#entitlements) are applied to the app
   bundle and to helper executables and helper bundles shipped by your
   dependencies; frameworks and libraries are signed without entitlements,
   per Apple guidance.
2. Verify the result with `codesign --verify --deep --strict` and check that
   no binary was left unsigned.

The build fails with an actionable error if the identity is not found in the
keychain, if any file fails to sign, or if verification fails. An expired or
revoked certificate is called out by name and status instead of appearing
missing.

### Identity auto-discovery

An identity counts as *not configured* only when the CLI option, the
`pyproject.toml` key, **and** the environment variable are all unset — the
[resolution order](#resolution-order-2) above runs first, and any configured
value is matched as given, never silently replaced.

With no identity configured anywhere, build modes that cannot proceed
without one discover it from the keychain:

- [notarizing builds](#notarization) use your **Developer ID Application**
  certificate;
- [App Store builds](#mac-app-store) use your **Apple Distribution**
  certificate (or its legacy equivalent, `3rd Party Mac Developer
  Application`) for the app and your **installer certificate** for the
  `.pkg`.

Discovery succeeds when the keychain holds exactly one valid certificate of
the required type — the chosen identity is printed in the build output.
With several candidates (for example, certificates from two teams), the
build fails with the candidate list; configure the certificate name or
SHA-1 fingerprint explicitly. Plain builds (neither notarize nor App Store
mode) never auto-discover.

Certificate types also scope *explicit* identities in these modes: a
partial identity such as your team ID only has to be unique among
certificates of the required type, not among all your certificates.

## Notarization

A Developer-ID-signed app must also be **notarized** by Apple for Gatekeeper to
open it without warnings. Notarization uploads the app to Apple's notary
service (a malware scan, typically a few minutes), after which the resulting
"ticket" is **stapled** to the app so it validates even offline.

### Credentials

Apple's notary service accepts two kinds of credentials — get whichever
suits you:

- **App Store Connect API key** (recommended; also reusable for
  [store uploads](#uploading)) — in App Store Connect, open
  [Users and Access → Integrations](https://appstoreconnect.apple.com/access/integrations/api)
  → **App Store Connect API** → **Team Keys** → **+**. Name the key, give it
  the **Developer** role, then download the `AuthKey_<KEY_ID>.p8` file —
  possible **only once** — and note the key's **Key ID** and the **Issuer
  ID** shown at the top of the page.
- **Apple ID + app-specific password** — at
  [account.apple.com](https://account.apple.com) → **Sign-In and Security** →
  **App-Specific Passwords** → **+**, generate a
  [password](https://support.apple.com/102654) dedicated to notarization
  (your regular Apple ID password won't work with `notarytool`).

Flet can receive either kind through two channels:

- **Keychain profile** (best for local development) — a one-time setup that
  saves the credential into the macOS keychain under a name of your choice.
  With an API key:

  ```bash
  xcrun notarytool store-credentials flet-notary \
    --key ~/keys/AuthKey_ABC123DEFG.p8 --key-id ABC123DEFG \
    --issuer 12345678-90ab-cdef-1234-567890abcdef
  ```

  or with an Apple ID (prompts for the app-specific password):

  ```bash
  xcrun notarytool store-credentials flet-notary \
    --apple-id you@example.com --team-id TEAM123456
  ```

  From then on, only the profile name (here `flet-notary`) is needed; the
  secrets never appear in your shell history, environment, or `pyproject.toml`.

- **Environment variables** (best for CI) — pass an App Store Connect API key
  inline on each run by setting
  [`APPLE_API_KEY`](../reference/environment-variables.md#apple_api_key)
  (path to the `.p8` file),
  [`APPLE_API_KEY_ID`](../reference/environment-variables.md#apple_api_key_id),
  and
  [`APPLE_API_ISSUER`](../reference/environment-variables.md#apple_api_issuer).
  Nothing is stored on the machine, which suits ephemeral CI runners where
  no keychain profile exists — inject the values from your repository
  secrets.

#### Resolution order

Credentials are determined in the following order of precedence:

1. [`--macos-notary-profile`](../cli/flet-build.md#--macos-notary-profile)
2. `[tool.flet.macos.signing].notary_profile`
3. [`FLET_MACOS_NOTARY_PROFILE`](../reference/environment-variables.md#flet_macos_notary_profile)
   environment variable
4. The [`APPLE_API_KEY`](../reference/environment-variables.md#apple_api_key),
   [`APPLE_API_KEY_ID`](../reference/environment-variables.md#apple_api_key_id)
   and
   [`APPLE_API_ISSUER`](../reference/environment-variables.md#apple_api_issuer)
   environment variables (all three must be set)
5. Default: none — notarizing builds fail without credentials.

A configured profile deliberately outranks the `APPLE_API_*` variables, which
other tooling (Fastlane, CI images) may have exported for a different team.

### Notarizing the app

<Tabs groupId="flet-build--pyproject-toml--env">
<TabItem value="flet-build" label="flet build">
```bash
flet build macos \
  --macos-signing-identity "Developer ID Application: Jane Doe (TEAM123456)" \
  --macos-notarize --macos-notary-profile flet-notary
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.macos.signing]
identity = "Developer ID Application: Jane Doe (TEAM123456)"
notarize = true
notary_profile = "flet-notary"
```
</TabItem>
<TabItem value="env" label="env var">
```dotenv
FLET_MACOS_SIGNING_IDENTITY="Developer ID Application: Jane Doe (TEAM123456)"
FLET_MACOS_NOTARY_PROFILE="flet-notary"
```
Notarization must still be turned on with
[`--macos-notarize`](../cli/flet-build.md#--macos-notarize) (or
`[tool.flet.macos.signing].notarize = true`); this toggle has no environment-variable equivalent.
</TabItem>
</Tabs>

When notarizing, the signing identity may be omitted entirely —
see [Identity auto-discovery](#identity-auto-discovery).

If notarization is rejected, the build fails and prints Apple's notarization
log, which lists the exact offending files.

#### Resolution order

Whether to notarize is determined in the following order of precedence:

1. [`--macos-notarize`](../cli/flet-build.md#--macos-notarize) /
   `--no-macos-notarize`
2. `[tool.flet.macos.signing].notarize`
3. Default: `false`

### Distributing

Ship the signed, notarized, and stapled `.app` in a **DMG** (recommended) or a
zip archive created with `ditto -c -k --keepParent` (preserves the bundle
structure and staple). A simple DMG that also gets its own staple:

```bash
hdiutil create -volname "MyApp" -srcfolder build/macos/MyApp.app -ov -format UDZO MyApp.dmg
codesign -f --timestamp -s "Developer ID Application: Jane Doe (TEAM123456)" MyApp.dmg
xcrun notarytool submit MyApp.dmg --keychain-profile flet-notary --wait
xcrun stapler staple MyApp.dmg
```

### Signing and notarizing in CI

#### GitHub Actions

Export your certificate and private key as a `.p12` file, then store it
(base64-encoded) and its password as repository secrets:

```yaml
- uses: apple-actions/import-codesign-certs@v3
  with:
    p12-file-base64: ${{ secrets.MACOS_CERTIFICATE_P12 }}
    p12-password: ${{ secrets.MACOS_CERTIFICATE_PASSWORD }}

- name: Build, sign and notarize
  env:
    FLET_MACOS_SIGNING_IDENTITY: ${{ secrets.MACOS_SIGNING_IDENTITY }}
    APPLE_API_KEY: ${{ github.workspace }}/AuthKey.p8
    APPLE_API_KEY_ID: ${{ secrets.APPLE_API_KEY_ID }}
    APPLE_API_ISSUER: ${{ secrets.APPLE_API_ISSUER }}
  run: |
    echo "${{ secrets.APPLE_API_KEY_P8 }}" > AuthKey.p8
    flet build macos --macos-notarize
```

### Troubleshooting

| Symptom                                                 | Cause and fix                                                                                                                                                                                                                                                                                                                                                              |
|---------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `"MyApp" is damaged and can't be opened` on users' Macs | The bundle was modified after signing — most commonly the app writes next to its own files at runtime. Write user data to `os.getcwd()` (Flet points it at a writable location) instead of paths derived from `__file__`. Also triggered by building with [`--no-compile-app`](../cli/flet-build.md#--compile-app)/[`--no-compile-packages`](../cli/flet-build.md#--compile-packages), which lets Python create `__pycache__` inside the bundle at runtime. |
| `errSecInternalComponent` when signing in CI            | The keychain is locked — unlock it in the job, or use [`apple-actions/import-codesign-certs`](https://github.com/apple-actions/import-codesign-certs), which handles it.                                                                                                                                                                                                   |
| Notarization status `Invalid`                           | Read the printed notary log: typical causes are an unsigned binary that was added to the bundle after signing, or a certificate that is not a Developer ID Application certificate.                                                                                                                                                                                        |
| `library load disallowed by system policy`              | A native library is signed with a different Team ID than the app (or not at all). Rebuild so all binaries are re-signed together, or — if your app must load externally acquired native code at runtime — add the `com.apple.security.cs.disable-library-validation` [entitlement](#entitlements).                                                                         |
| Notarization takes very long                            | The first-ever submission for a new account can take up to an hour or more; subsequent submissions typically finish within minutes.                                                                                                                                                                                                                                        |

## Mac App Store

The signing support above targets **direct distribution** (your website,
GitHub releases, etc.). For the Mac App Store — including TestFlight —
`flet build macos` has a dedicated mode that produces a signed installer
`.pkg` ready for App Store Connect. In this mode the app is signed with
your *Apple Distribution* certificate — sandboxed, without the hardened
runtime — your provisioning profile is embedded, the store-mandated
`application-identifier`/`team-identifier` entitlements are applied (helper
executables and helper bundles get the sandbox `inherit` pair), and every
hardened-runtime
exception entitlement (`com.apple.security.cs.*`, including the defaults)
is stripped: they are meaningless without the hardened runtime and
scrutinized by App Review. Notarization does **not** apply to store
submissions and is rejected in combination with `app_store`.

### Store prerequisites

One-time setup, requiring an
[Apple Developer Program](https://developer.apple.com/programs/) membership.

#### Creating the distribution certificates

Store builds need two certificates. Create both under
[Certificates](https://developer.apple.com/account/resources/certificates/list)
→ **+** (if you don't have a certificate request file yet, see
[Generating a CSR](ios.md#generating-a-certificate-signing-request-csr) —
the process is identical for macOS):

1. **Apple Distribution** — signs the app bundle.
2. **Mac Installer Distribution** — signs the installer `.pkg`. It appears
   in your keychain as `3rd Party Mac Developer Installer`, and because it
   signs packages rather than code, `security find-identity -v -p
   codesigning` does not list it. Verify it with:

   ```bash
   security find-identity -v -p basic
   ```

Download each certificate and double-click it to install it — with its
private key — into your login keychain.

#### Registering an App ID

Under [Identifiers](https://developer.apple.com/account/resources/identifiers/list)
→ **+** → **App IDs** → type **App**, register an **explicit** App ID whose
bundle ID exactly matches your app's (by default `<org>.<project name>`
from `pyproject.toml`). No extra capabilities are needed.

#### Creating the provisioning profile

Under [Profiles](https://developer.apple.com/account/resources/profiles/list)
→ **+**, select **Mac App Store Connect** (under *Distribution*), then:

1. Select the App ID registered above.
2. Select your **Apple Distribution** certificate.
3. Name the profile and click **Generate**.
4. Download the `.provisionprofile` file and keep it with your project —
   it contains no secrets (it is a document signed *by Apple* authorizing
   your App ID and team), so it is safe to commit.

#### Creating the App Store Connect app record

In [App Store Connect](https://appstoreconnect.apple.com) → **My Apps** →
**+** → **New App**: platform **macOS**, the bundle ID from above, any name
and SKU. Then note the app's numeric **Apple ID** under **App Information →
General Information** — command-line uploads are keyed to it.

### Provisioning profile

The profile created [above](#creating-the-provisioning-profile). A relative
path resolves against the project directory (where `pyproject.toml` lives).
The build embeds it at `Contents/embedded.provisionprofile` — sealed by the
app's signature — and fails fast when the profile's App ID does not cover
the app's bundle ID, a mismatch that would otherwise surface only after
upload as `ITMS-90889`.

#### Resolution order

The provisioning profile is determined in the following order of precedence:

1. [`--macos-provisioning-profile`](../cli/flet-build.md#--macos-provisioning-profile)
2. `[tool.flet.macos.signing].provisioning_profile`
3. [`FLET_MACOS_PROVISIONING_PROFILE`](../reference/environment-variables.md#flet_macos_provisioning_profile)
   environment variable
4. Default: none — App Store builds fail without one.

### Installer identity

The certificate that signs the `.pkg` — the exact certificate name (as
listed by `security find-identity -v -p basic`), its SHA-1 fingerprint, or
a unique substring, matched only among installer certificates.

#### Resolution order

The installer identity is determined in the following order of precedence:

1. [`--macos-installer-identity`](../cli/flet-build.md#--macos-installer-identity)
2. `[tool.flet.macos.signing].installer_identity`
3. [`FLET_MACOS_INSTALLER_IDENTITY`](../reference/environment-variables.md#flet_macos_installer_identity)
   environment variable
4. Default: none — the certificate is
   [auto-discovered](#identity-auto-discovery).

### Building for the App Store

<Tabs groupId="flet-build--pyproject-toml--env">
<TabItem value="flet-build" label="flet build">
```bash
flet build macos --macos-app-store \
  --macos-provisioning-profile certs/MyApp_MacAppStore.provisionprofile \
  --info-plist LSApplicationCategoryType="public.app-category.productivity" \
    ITSAppUsesNonExemptEncryption=False
```
</TabItem>
<TabItem value="pyproject-toml" label="pyproject.toml">
```toml
[tool.flet.macos.info]
# required by App Store validation
LSApplicationCategoryType = "public.app-category.productivity"
# answers the export-compliance question per build (standard encryption only)
ITSAppUsesNonExemptEncryption = false

[tool.flet.macos.signing]
app_store = true
provisioning_profile = "certs/MyApp_MacAppStore.provisionprofile"
```
</TabItem>
<TabItem value="env" label="env var">
```dotenv
FLET_MACOS_PROVISIONING_PROFILE="certs/MyApp_MacAppStore.provisionprofile"
```
App Store mode must still be turned on with
[`--macos-app-store`](../cli/flet-build.md#--macos-app-store) (or
`[tool.flet.macos.signing].app_store = true`); this toggle has no
environment-variable equivalent.
</TabItem>
</Tabs>

[`LSApplicationCategoryType`](https://developer.apple.com/documentation/bundleresources/information-property-list/lsapplicationcategorytype)
is required — App Store validation rejects the package without it.
`ITSAppUsesNonExemptEncryption = false` is optional but answers the
export-compliance question once and for all; without it, App Store Connect
asks manually for every uploaded build. Both are ordinary
[Info.plist](#infoplist) keys.

Neither signing identity appears in the examples above: both are
[auto-discovered](#identity-auto-discovery) when not configured. To pin
them explicitly, configure the [signing identity](#signing-the-app) for
the app certificate and the [installer identity](#installer-identity) for
the `.pkg` certificate.

#### Resolution order

Whether to build for the App Store is determined in the following order of
precedence:

1. [`--macos-app-store`](../cli/flet-build.md#--macos-app-store) /
   `--no-macos-app-store`
2. `[tool.flet.macos.signing].app_store`
3. Default: `false`

### Uploading

Upload the `.pkg` with [Transporter](https://apps.apple.com/app/transporter/id1450874784)
or from the command line, authenticating with the same
[App Store Connect API key](#credentials) used for notarization — `altool`
reads the `.p8` file from `~/.appstoreconnect/private_keys/`:

```bash
xcrun altool --validate-app -f build/macos/MyApp.pkg -t macos \
    --apiKey <KEY_ID> --apiIssuer <ISSUER_ID>
xcrun altool --upload-package build/macos/MyApp.pkg -t macos \
    --apiKey <KEY_ID> --apiIssuer <ISSUER_ID> \
    --apple-id <NUMERIC_APP_ID> --bundle-id <BUNDLE_ID> \
    --bundle-version <BUILD_NUMBER> --bundle-short-version-string <VERSION>
```

`<NUMERIC_APP_ID>` is the app record's Apple ID
[noted earlier](#creating-the-app-store-connect-app-record), and every
upload needs a unique [build number](index.md#build-number).
After processing (minutes; failures arrive by email as `ITMS-xxxx` codes),
the build appears in the **TestFlight** tab of your app record — internal
testers can install it without beta review. Note that `--validate-app`
does not catch everything processing checks, so a clean upload is only
confirmed once processing completes.
