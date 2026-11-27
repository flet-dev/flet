from typing import Any, Callable, Optional

from flet.auth.group import Group
from flet.auth.user import User


class OAuthProvider:
    """
    Base configuration and extension point for OAuth providers in Flet.

    Instances describe OAuth endpoints, client credentials, optional PKCE
    parameters, and optional user/group retrieval behavior used by
    :class:`~flet.auth.AuthorizationService`.

    Args:
        client_id: OAuth client/application ID issued by the provider.
        client_secret: OAuth client secret issued by the provider.
        authorization_endpoint: Authorization endpoint URL used to build the
            login redirect URL.
        token_endpoint: Token endpoint URL used for authorization-code and
            refresh-token exchange.
        redirect_url: Redirect/callback URL registered with the provider.
            Optional when using :meth:`discover` with
            :class:`~flet.WebAuth` (session supplies the effective redirect).
        scopes: Base OAuth scopes always requested during login.
        user_scopes: Additional scopes requested when user profile loading
            is enabled.
        user_endpoint: Endpoint used to fetch raw user profile
            data after login.
        user_id_fn: Function extracting a stable user id from
            `user_endpoint` response data.
        group_scopes: Additional scopes requested when group loading is enabled.
        code_challenge: PKCE code challenge.
        code_challenge_method: PKCE challenge method. For example, `S256`.
        code_verifier: PKCE code verifier used during token exchange.
        authorization_params: Extra query parameters appended to authorization
            URL generation by the OAuth authorization service.
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
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorization_endpoint = authorization_endpoint
        self.token_endpoint = token_endpoint
        self.redirect_url = redirect_url
        self.scopes = scopes if scopes is not None else []
        self.user_scopes = user_scopes if user_scopes is not None else []
        self.user_endpoint = user_endpoint
        self.user_id_fn = user_id_fn
        self.group_scopes = group_scopes if group_scopes is not None else []
        self.authorization_params = (
            authorization_params if authorization_params is not None else {}
        )
        self.code_challenge = code_challenge
        self.code_challenge_method = code_challenge_method
        self.code_verifier = code_verifier
        self.jwks_uri: Optional[str] = None
        self.end_session_endpoint: Optional[str] = None
        self.issuer: Optional[str] = None

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
    ) -> "OAuthProvider":
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
            A configured :class:`OAuthProvider` instance.

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

        provider = cls(
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
        )
        provider.issuer = doc.get("issuer") or base
        provider.jwks_uri = doc.get("jwks_uri")
        provider.end_session_endpoint = doc.get("end_session_endpoint")
        return provider

    def _name(self):
        """
        Returns provider name/identifier.

        Intended as an optional subclass extension point.
        """
        raise NotImplementedError("Subclasses must implement _name()")

    async def _fetch_groups(self, access_token: str) -> list[Group]:
        """
        Fetches user groups from the provider API.

        Args:
            access_token: OAuth access token.

        Returns:
            A list of :class:`~flet.auth.Group`. The base implementation
                returns an empty list.
        """
        return []

    async def _fetch_user(self, access_token: str) -> Optional[User]:
        """
        Fetches user profile from the provider API.

        Args:
            access_token: OAuth access token.

        Returns:
            A :class:`~flet.auth.User` instance, or `None` to let authorization
                fallback logic use `user_endpoint` / `user_id_fn`.
        """
        return None
