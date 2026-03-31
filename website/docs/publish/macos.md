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
    "com.apple.security.network.client" = true
    "com.apple.security.network.server" = true
    "com.apple.security.files.user-selected.read-write" = true
    ```

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
