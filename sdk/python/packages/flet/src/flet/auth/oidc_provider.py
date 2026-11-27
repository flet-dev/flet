from typing import Any, Callable, Optional

from flet.auth.oauth_provider import OAuthProvider

__all__ = ["OIDCProvider"]


class OIDCProvider(OAuthProvider):
    """
    OAuth provider configured from OpenID Connect metadata.

    Use this when the IdP exposes an OIDC discovery document
    (``/.well-known/openid-configuration``). For providers with known
    endpoints (Auth0, Google, GitHub, Azure), prefer the dedicated
    :class:`~flet.auth.providers` presets or a plain
    :class:`~flet.auth.OAuthProvider` with explicit URLs.

    Attributes:
        issuer: OIDC issuer URL from the discovery document (or the
            issuer passed to :meth:`discover`).
        jwks_uri: JWKS URL when present in the discovery document.
        end_session_endpoint: RP-initiated logout URL when present.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        authorization_endpoint: str,
        token_endpoint: str,
        redirect_url: Optional[str] = None,
        scopes: Optional[list[str]] = None,
        user_scopes: Optional[list[str]] = None,
        user_endpoint: Optional[str] = None,
        user_id_fn: Optional[Callable] = None,
        group_scopes: Optional[list[str]] = None,
        code_challenge: Optional[str] = None,
        code_challenge_method: Optional[str] = None,
        code_verifier: Optional[str] = None,
        authorization_params: Optional[dict[str, str]] = None,
        *,
        issuer: Optional[str] = None,
        jwks_uri: Optional[str] = None,
        end_session_endpoint: Optional[str] = None,
    ) -> None:
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            authorization_endpoint=authorization_endpoint,
            token_endpoint=token_endpoint,
            redirect_url=redirect_url,
            scopes=scopes,
            user_scopes=user_scopes,
            user_endpoint=user_endpoint,
            user_id_fn=user_id_fn,
            group_scopes=group_scopes,
            code_challenge=code_challenge,
            code_challenge_method=code_challenge_method,
            code_verifier=code_verifier,
            authorization_params=authorization_params,
        )
        self.issuer = issuer
        self.jwks_uri = jwks_uri
        self.end_session_endpoint = end_session_endpoint

    @classmethod
    async def discover(
        cls,
        issuer: str,
        *,
        client_id: str,
        client_secret: str = "",
        scopes: Optional[list[str]] = None,
        user_scopes: Optional[list[str]] = None,
        group_scopes: Optional[list[str]] = None,
        user_id_fn: Optional[Callable] = None,
        authorization_params: Optional[dict[str, str]] = None,
        code_challenge: Optional[str] = None,
        code_challenge_method: Optional[str] = None,
        code_verifier: Optional[str] = None,
    ) -> "OIDCProvider":
        """
        Build a provider from an OIDC issuer discovery document.

        Fetches ``{issuer}/.well-known/openid-configuration`` and populates
        authorization, token, and (when present) userinfo endpoints.
        Does **not** set ``redirect_url`` — that comes from the client /
        :class:`~flet.WebAuth` session.

        Args:
            issuer: OIDC issuer base URL (trailing slash optional).
            client_id: OAuth client ID.
            client_secret: Client secret; use ``""`` for public native clients.
            scopes: Base OAuth scopes.
            user_scopes: Extra scopes when fetching the user profile.
            group_scopes: Extra scopes when fetching groups.
            user_id_fn: Optional user id extractor for ``userinfo`` responses.
            authorization_params: Extra authorize query parameters.
            code_challenge: Optional PKCE challenge.
            code_challenge_method: Optional PKCE method (e.g. ``S256``).
            code_verifier: Optional PKCE verifier.

        Returns:
            A configured :class:`OIDCProvider` instance.

        Raises:
            ValueError: If required endpoints are missing from the document.
            httpx.HTTPStatusError: If the discovery HTTP request fails.
        """
        import httpx

        base = issuer.rstrip("/")
        discovery_url = f"{base}/.well-known/openid-configuration"

        async with httpx.AsyncClient(follow_redirects=True) as client:
            resp = await client.get(discovery_url)
            resp.raise_for_status()
            doc: dict[str, Any] = resp.json()

        authorization_endpoint = doc.get("authorization_endpoint")
        token_endpoint = doc.get("token_endpoint")
        if not authorization_endpoint:
            raise ValueError(
                "OIDC discovery document missing required "
                "'authorization_endpoint'."
            )
        if not token_endpoint:
            raise ValueError(
                "OIDC discovery document missing required 'token_endpoint'."
            )

        return cls(
            client_id=client_id,
            client_secret=client_secret,
            authorization_endpoint=authorization_endpoint,
            token_endpoint=token_endpoint,
            redirect_url=None,
            scopes=scopes,
            user_scopes=user_scopes,
            user_endpoint=doc.get("userinfo_endpoint"),
            user_id_fn=user_id_fn,
            group_scopes=group_scopes,
            code_challenge=code_challenge,
            code_challenge_method=code_challenge_method,
            code_verifier=code_verifier,
            authorization_params=authorization_params,
            issuer=doc.get("issuer") or base,
            jwks_uri=doc.get("jwks_uri"),
            end_session_endpoint=doc.get("end_session_endpoint"),
        )
