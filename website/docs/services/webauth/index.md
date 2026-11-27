---
class_name: "flet.WebAuth"
title: "WebAuth"
---

import {ClassAll, CodeExample, Image} from '@site/src/components/crocodocs';

Protocol-agnostic service that opens a system sign-in page and returns the
redirect callback URL. Used by [`page.login`](../../cookbook/authentication.md)
on Android and iOS.

`WebAuth` knows nothing about OAuth. URL building, CSRF `state`, PKCE, and
token exchange stay in Python (`AuthorizationService` /
[`OAuthProvider`](../../types/auth/oauthprovider.md)).

On **Android**, authenticate prefers Chrome
[Auth Tab](https://developer.chrome.com/docs/android/custom-tabs/guide-auth-tab)
so custom-scheme redirects return to the app. On **iOS**, it uses
`ASWebAuthenticationSession`.

Desktop and web WebAuth are planned for later releases; until then
`page.login` on those platforms keeps the existing web callback flow or
raises a clear unsupported error.

## Platform Support

| Platform  | Windows | macOS | Linux | iOS | Android | Web |
|-----------|---------|-------|-------|-----|---------|-----|
| Supported | ❌       | ❌     | ❌     | ✅   | ✅       | ❌   |

## Usage

`WebAuth` ships in core `flet` — no extra package.

```python
session = await ft.WebAuth().start(callback_scheme="com.example.myapp.auth")
# session.redirect_url == "com.example.myapp.auth://callback"
callback_url = await session.authenticate(auth_url, ephemeral=False)
```

Or use [`page.login`](../../cookbook/authentication.md) with
`callback_scheme=...`.

### Build callback scheme

`flet build` / `flet debug` auto-registers a default Android callback scheme
of **`<bundle id>.auth`** (separate from
[`deep_linking`](../../publish/index.md#deep-linking)).

Override when needed:

```toml
[tool.flet.web_auth]
callback_scheme = "com.example.myapp.auth"
```

```bash
flet build apk --web-auth-callback-scheme com.example.myapp.auth
```

Pass the **same** scheme to `page.login(callback_scheme=...)` or
`WebAuth().start(callback_scheme=...)`. Register
`<scheme>://callback` with your IdP.

See [Publishing — WebAuth callback scheme](../../publish/index.md#webauth-callback-scheme).

PKCE and `state` are generated in Python for the mobile path. Web-only
`page.login` parameters (`on_open_authorization_url`, `complete_page_html`,
`redirect_to_page`) are ignored on mobile.

## Auth0 native (PKCE) on Android / iOS

Use an Auth0 **Native** application (public client). Do **not** put a
client secret in a packaged APK/IPA.

### 1. Create a Native application

In Auth0: **Applications → Create Application**. Choose **Native**, then
**Create**.

<Image src="/docs/assets/services/webauth/auth0-create-native.png" width="85%" caption="Create a Native Auth0 application" />

### 2. Copy Domain and Client ID

Open the app **Settings** tab. Copy **Domain** and **Client ID** into your
app env. Leave the client secret unused.

<Image src="/docs/assets/services/webauth/auth0-settings-credentials.png" width="85%" caption="Domain and Client ID on the Settings tab" />

### 3. Register callback URLs (URLs tab)

Open the **URLs** tab. Add the same URI to **Allowed Callback URLs** and
**Allowed Logout URLs**. It must match `session.redirect_url` /
`<callback_scheme>://callback`.

Example:

```text
com.example.myapp.auth://callback
```

<Image src="/docs/assets/services/webauth/auth0-urls-callbacks.png" width="85%" caption="Allowed Callback / Logout URLs on the URLs tab" />

### 4. Configure the Flet app

```text
AUTH0_DOMAIN=your-tenant.us.auth0.com
AUTH0_CLIENT_ID=your-native-app-client-id
WEBAUTH_CALLBACK_SCHEME=com.example.myapp.auth
```

Prefer [`Auth0OAuthProvider`](../../types/auth/auth0oauthprovider.md) for
Auth0 (fixed endpoints). Use
[`OIDCProvider.discover`](../../types/auth/oidcprovider.md) only when you
have an OIDC issuer discovery URL and no preset.

Package `.env` with `include` or `--include` if you use one (dotfiles are
excluded by default — [Publishing](../../publish/index.md#default-exclusions)).

Packaged example: `sdk/python/examples/apps/webauth`.

<CodeExample path="services/webauth/main.py" language="python" />

## Description

<ClassAll name="flet.WebAuth" separateSignature={true} />
