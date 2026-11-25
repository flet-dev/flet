# Changelog

## 0.1.0

* Initial release: `AppAuth` service wrapping `flutter_appauth` for Android/iOS
  authorization-code + PKCE (authorize only; token exchange in Python).
* Android: prefer Chrome **Auth Tab** for authorize so custom-scheme redirects
  (`flet://…`) are returned via callback; fall back to an external browser
  (no Custom Tabs) when Auth Tab is unavailable. Fixes IdPs such as Pocket ID
  that complete login with a JS navigation Chrome Custom Tabs would otherwise
  block.
* Android Auth Tab honors `prefer_ephemeral_session` via
  `AuthTabIntent.setEphemeralBrowsingEnabled` so post-logout authorize cannot
  reuse Chrome IdP cookies (works with any provider).
* Android Auth Tab requires OAuth `state` on the redirect; peels `prompt` /
  `login_hint` into AppAuth builder methods; forces `prompt=login` when
  ephemeral reauth is requested (covers external-browser fallback).
* iOS keeps `max_age` in additional parameters and maps `login_hint` to the
  dedicated AppAuth field.
