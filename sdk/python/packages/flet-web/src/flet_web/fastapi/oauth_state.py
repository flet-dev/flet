import dataclasses
from datetime import datetime
from typing import Optional


@dataclasses.dataclass
class OAuthState:
    """
    Temporary OAuth flow state persisted between auth start and callback.

    Instances are stored by [`FletAppManager`][flet_web.fastapi.flet_app_manager.]
    and keyed by the `flet_oauth_state` cookie value.
    """

    session_id: str
    """
    Related Flet session identifier.
    """

    expires_at: datetime
    """
    UTC expiration timestamp after which this state is discarded.
    """

    complete_page_url: Optional[str] = None
    """
    URL to redirect/open after OAuth flow completion, if provided.
    """

    complete_page_html: Optional[str] = None
    """
    Optional completion HTML returned after OAuth callback handling.
    """

    code: Optional[str] = None
    """
    Authorization code returned by OAuth provider, if successful.
    """

    error: Optional[str] = None
    """
    OAuth error code returned by provider, if flow failed.
    """

    error_description: Optional[str] = None
    """
    Human-readable OAuth error description, when available.
    """
