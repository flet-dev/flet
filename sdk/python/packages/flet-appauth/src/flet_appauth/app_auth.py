from typing import Optional

import flet as ft
from flet.controls.exceptions import FletUnsupportedPlatformException
from flet.controls.types import PagePlatform
from flet_appauth.types import AppAuthAuthorizationResult

__all__ = ["AppAuth"]


@ft.control("AppAuth")
class AppAuth(ft.Service):
    """
    Native OAuth authorization via AppAuth (Android and iOS).

    Performs the authorization-code request and redirect capture only.
    Token exchange is handled in Python by
    [`AuthorizationService`][flet.auth.authorization_service.AuthorizationService]
    / [`Page.login`][flet.Page.login].
    """

    def _ensure_mobile(self) -> None:
        if self.page is None:
            raise RuntimeError("AppAuth must be used with an active page.")
        if self.page.web or self.page.platform not in {
            PagePlatform.ANDROID,
            PagePlatform.IOS,
            "android",
            "ios",
        }:
            raise FletUnsupportedPlatformException(
                "AppAuth is supported on Android and iOS only."
            )

    async def authorize(
        self,
        *,
        client_id: str,
        redirect_url: str,
        authorization_endpoint: str,
        token_endpoint: str,
        scopes: Optional[list[str]] = None,
        additional_parameters: Optional[dict[str, str]] = None,
        prefer_ephemeral_session: bool = False,
    ) -> AppAuthAuthorizationResult:
        """
        Start a native authorization-code request (AppAuth generates PKCE).

        Args:
            client_id: OAuth client ID.
            redirect_url: Redirect URI registered with the IdP and the app.
            authorization_endpoint: Provider authorization endpoint URL.
            token_endpoint: Provider token endpoint URL (required by AppAuth
                service configuration even when Python exchanges the code).
            scopes: OAuth scopes to request.
            additional_parameters: Extra authorize query parameters.
            prefer_ephemeral_session: Use an ephemeral auth browser session
                when supported (iOS ASWebAuthenticationSession;
                Android Auth Tab via ``setEphemeralBrowsingEnabled``). The
                session does not share cookies with the user's normal browser
                profile, so IdP SSO cannot silently re-authenticate after
                sign-out.

        Returns:
            [`AppAuthAuthorizationResult`][(p).] with code + PKCE verifier,
            or error / cancellation fields.
        """
        self._ensure_mobile()
        raw = await self._invoke_method(
            "authorize",
            {
                "client_id": client_id,
                "redirect_url": redirect_url,
                "authorization_endpoint": authorization_endpoint,
                "token_endpoint": token_endpoint,
                "scopes": scopes or [],
                "additional_parameters": additional_parameters or {},
                "prefer_ephemeral_session": prefer_ephemeral_session,
            },
        )
        if isinstance(raw, AppAuthAuthorizationResult):
            return raw
        if not isinstance(raw, dict):
            return AppAuthAuthorizationResult(
                error="invalid_response",
                error_description=f"Unexpected AppAuth result type: {type(raw)!r}",
            )
        return AppAuthAuthorizationResult(
            authorization_code=raw.get("authorization_code"),
            code_verifier=raw.get("code_verifier"),
            error=raw.get("error"),
            error_description=raw.get("error_description"),
        )
