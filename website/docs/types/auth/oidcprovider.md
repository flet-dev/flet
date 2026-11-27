---
title: "OIDCProvider"
---

import {ClassAll} from '@site/src/components/crocodocs';

OpenID Connect provider built on [`OAuthProvider`](oauthprovider/index.md).
Use `discover` only when you supply an OIDC issuer URL and want endpoints
from `/.well-known/openid-configuration`. For Auth0, Google, GitHub, and
Azure, prefer the dedicated OAuth provider presets.

<ClassAll name="flet.auth.OIDCProvider" />
