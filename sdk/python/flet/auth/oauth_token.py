import time
from datetime import datetime, timedelta
from typing import List, Optional


class OAuthToken:
    def __init__(
        self,
        access_token: str,
        scope: List[str],
        token_type: str,
        expires_in: Optional[int],
        expires_at: Optional[float],
        refresh_token: Optional[str],
    ) -> None:
        self.access_token = access_token
        self.scope = scope
        self.token_type = token_type
        self.issued = time.time()
        self.expires_in = expires_in
        self.expires_at = expires_at
        self.refresh_token = refresh_token
