---
slug: user-authentication
title: User authentication
authors: feodor
tags: [release]
---

import TOCInline from '@theme/TOCInline';

User authentication in Flet is here! 🎉

Now you can implement user authentication ("Login with X" buttons) in your Flet app using 3rd-party identity providers such as GitHub, Google, Azure, Auth0, LinkedIn and others:

<img src="/img/docs/getting-started/authentication/github-oauth-authorize.png" className="screenshot-40" />

Traditionally, this release is not just about authentication, but it adds a ton of accompanying functionality and small improvements:

<TOCInline toc={toc} maxHeadingLevel={2} />

<!-- truncate -->

## Authentication

Flet authentication features:

* Works with Flet desktop, web and mobile apps.
* Using multiple authentication providers in one app.
* Built-in OAuth providers with automatic user details fetching:
  * GitHub
  * Azure
  * Google
  * Auth0
* Optional groups fetching.
* Automatic token refresh.
* Login with a saved token ("Remember me").
* Custom OAuth providers.

A simple example on how to add "Login with GitHub" button to your Flet app:

```python
import os

import flet as ft
from flet.auth.providers.github_oauth_provider import GitHubOAuthProvider

def main(page: ft.Page):

    provider = GitHubOAuthProvider(
        client_id=os.getenv("GITHUB_CLIENT_ID"),
        client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
        redirect_url="http://localhost:8550/api/oauth/redirect",
    )

    def login_click(e):
        page.login(provider)

    def on_login(e):
        print("Access token:", page.auth.token.access_token)
        print("User ID:", page.auth.user.id)

    page.on_login = on_login
    page.add(ft.ElevatedButton("Login with GitHub", on_click=login_click))

ft.run(main, port=8550, view=ft.AppView.WEB_BROWSER)
```

:::note
Before running the app set the secret environment variables in a command line:

```
$ export GITHUB_CLIENT_ID="<client_id>"
$ export GITHUB_CLIENT_SECRET="<client_secret>"
```
:::

[Read Authentication guide for more information and examples](https://docs.flet.dev/cookbook/authentication/).

## Client storage

Flet's client storage API that allows storing key-value data on a client side in a persistent storage. Flet implementation uses [`shared_preferences`](https://pub.dev/packages/shared_preferences) Flutter package.

Writing data to the storage:

```python
page.client_storage.set("key", "value")
```

Reading data:

```python
value = page.client_storage.get("key")
```

[Read Client storage guide for more information and examples](https://docs.flet.dev/cookbook/client-storage/).

## Session storage

Flet introduces an API for storing key-value data in user's session on a server side.

Writing data to the session:

```python
page.session.set("key", "value")
```

Reading data:

```python
value = page.session.get("key")
```

[Read Session storage guide for more information and examples](https://docs.flet.dev/cookbook/session-storage/)

## Encryption API

In this release Flet introduces utility methods to encrypt and decrypt sensitive text data using symmetric algorithm (where the same key is used for encryption and decryption). It uses [Fernet](https://github.com/fernet/spec/blob/master/Spec.md) implementation from [cryptography](https://pypi.org/project/cryptography/) package, which is AES 128 with some additional hardening, plus PBKDF2 to derive encryption key from a user passphrase.

Encrypting data:

```python
from flet.security import encrypt, decrypt
secret_key = "S3CreT!"
plain_text = "This is a secret message!"
encrypted_data = encrypt(plain_text, secret_key)
```

Decrypting data:

```python
from flet.security import encrypt, decrypt
secret_key = "S3CreT!"
plain_text = decrypt(encrypted_data, secret_key)
print(plain_text)
```

[Continue reading for more information and examples](https://docs.flet.dev/cookbook/encrypting-sensitive-data/).

## Other improvements

* SVG image support ([example](https://github.com/flet-dev/examples/blob/main/python/controls/image/svg-image.py)) and new images properties:
  * [`Image.color`](https://docs.flet.dev/controls/image/#flet.Image.color)
  * [`Image.color_blend_mode`](https://docs.flet.dev/controls/image/#flet.Image.color_blend_mode)
  * [`Image.semantics_label`](https://docs.flet.dev/controls/image/#flet.Image.semantics_label)
  * [`Image.gapless_playback`](https://docs.flet.dev/controls/image/#flet.Image.gapless_playback)
* [`on_animation_end` callback](https://docs.flet.dev/cookbook/animations/#animation-end-callback) to chain animations.
* [`Container.clip_behavior` property](https://docs.flet.dev/controls/container/#flet.Container.clip_behavior).
* [`page.window.bgcolor`](https://docs.flet.dev/types/window/#flet.Window.bgcolor) to make cool transparent app window:

```python
import flet as ft
def main(page: ft.Page):
    page.window_bgcolor = ft.Colors.TRANSPARENT
    page.bgcolor=ft.Colors.TRANSPARENT
    page.window_title_bar_hidden = True
    page.window_frameless = True
    page.window_left = 400
    page.window_top = 400
    page.add(ft.ElevatedButton("I'm a floating button!"))
ft.run(main)
```

* [`page.get_clipboard()`](https://docs.flet.dev/controls/page/#flet.Page.get_clipboard)
* [`page.launch_url()`](https://docs.flet.dev/controls/page/#flet.Page.launch_url) - better control with additional arguments:
    * `web_window_name` - window tab/name to open URL in: `_self` - the same tab, `_blank` - a new tab or `<your name>` - a named tab.
    * `web_popup_window` - set to `True` to display a URL in a browser popup window. Default is `False`.
    * `window_width` - optional, popup window width.
    * `window_height` - optional, popup window height.
* [`page.window.to_front()`](https://docs.flet.dev/types/window/#flet.Window.to_front)
* [`page.close_in_app_web_view()`](https://docs.flet.dev/controls/page/#flet.Page.close_in_app_web_view)


Upgrade Flet module to the latest version (`pip install flet --upgrade`), integrate auth in your app and [let us know](https://discord.gg/dzWXP8SHG8) what you think!

Enjoy!