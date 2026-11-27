from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.exceptions import FletUnsupportedPlatformException
from flet.controls.services.service import Service
from flet.controls.types import PagePlatform

__all__ = ["WebAuth", "WebAuthSession"]


@dataclass
class WebAuthSession:
    """
    A single WebAuth browser session.

    Created by :meth:`WebAuth.start`. Holds the platform redirect URL and
    completes authentication by opening the sign-in page and capturing the
    callback URL.
    """

    redirect_url: str
    """Platform-specific OAuth redirect / callback URL for this session."""

    _web_auth: "WebAuth" = field(repr=False)
    _callback_scheme: Optional[str] = field(default=None, repr=False)
    _done: bool = field(default=False, repr=False)

    async def authenticate(
        self,
        url: str,
        *,
        ephemeral: bool = False,
        timeout: float = 300,
    ) -> str:
        """
        Open ``url`` in the system sign-in UI and return the full callback URL.

        Args:
            url: Authorization URL (built in Python with ``redirect_url``,
                state, and PKCE).
            ephemeral: Prefer an ephemeral browser session when supported
                (iOS ``ASWebAuthenticationSession``;
                Android Auth Tab ephemeral browsing).
            timeout: Seconds to wait for the redirect before failing.

        Returns:
            The full callback URL including query string
            (e.g. ``com.example.app.auth://callback?code=...&state=...``).

        Raises:
            RuntimeError: If the session was already used or authentication
                failed / was cancelled.
        """
        if self._done:
            raise RuntimeError("WebAuthSession.authenticate() can only be called once.")
        self._done = True
        raw = await self._web_auth._authenticate(
            url=url,
            redirect_url=self.redirect_url,
            callback_scheme=self._callback_scheme,
            ephemeral=ephemeral,
            timeout=timeout,
        )
        if isinstance(raw, dict):
            error = raw.get("error")
            if error:
                desc = raw.get("error_description") or error
                raise RuntimeError(str(desc))
            callback_url = raw.get("callback_url")
            if callback_url:
                return str(callback_url)
        if isinstance(raw, str) and raw:
            return raw
        raise RuntimeError("WebAuth authenticate returned no callback URL.")

    async def cancel(self) -> None:
        """Cancel an in-flight authenticate (best-effort)."""
        await self._web_auth._cancel()


@control("WebAuth")
class WebAuth(Service):
    """
    Protocol-agnostic service: open a sign-in page and capture the redirect URL.

    Knows nothing about OAuth. Used by :meth:`flet.Page.login` on Android/iOS
    (P0); desktop loopback and web flows follow in later phases.
    """

    def _ensure_mobile(self) -> None:
        page = self.page
        if page.web or page.platform not in {
            PagePlatform.ANDROID,
            PagePlatform.IOS,
            "android",
            "ios",
        }:
            raise FletUnsupportedPlatformException(
                "WebAuth is supported on Android and iOS only in this release. "
                "Desktop and web WebAuth will follow in a later phase."
            )

    async def start(
        self,
        *,
        callback_scheme: Optional[str] = None,
    ) -> WebAuthSession:
        """
        Begin a WebAuth session and return the platform redirect URL.

        Args:
            callback_scheme: Custom URI scheme for mobile redirects
                (e.g. ``com.example.myapp.auth``). Required on Android/iOS.
                Must match the scheme registered at build time (default
                ``<bundle id>.auth``).

        Returns:
            A :class:`WebAuthSession` with ``redirect_url`` set.

        Raises:
            ValueError: If ``callback_scheme`` is missing on mobile.
            FletUnsupportedPlatformException: On unsupported platforms.
        """
        self._ensure_mobile()
        scheme = (callback_scheme or "").strip().lower().rstrip(":/")
        if not scheme:
            raise ValueError(
                "callback_scheme is required on Android/iOS for WebAuth. "
                "Pass the scheme registered for this app "
                "(default: <bundle id>.auth)."
            )
        redirect_url = f"{scheme}://callback"
        return WebAuthSession(
            redirect_url=redirect_url,
            _web_auth=self,
            _callback_scheme=scheme,
        )

    async def _authenticate(
        self,
        *,
        url: str,
        redirect_url: str,
        callback_scheme: Optional[str],
        ephemeral: bool,
        timeout: float,
    ) -> dict:
        self._ensure_mobile()
        raw = await self._invoke_method(
            "authenticate",
            {
                "url": url,
                "redirect_url": redirect_url,
                "callback_scheme": callback_scheme,
                "ephemeral": ephemeral,
                "timeout": timeout,
            },
        )
        if isinstance(raw, dict):
            return raw
        return {"callback_url": raw}

    async def _cancel(self) -> None:
        try:
            await self._invoke_method("cancel", {})
        except Exception:
            pass
