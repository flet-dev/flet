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
        refresh_token: Optional[str],
    ) -> None:
        self.access_token = access_token
        self.scope = scope
        self.token_type = token_type
        self.issued = time.time()
        if expires_in:
            self.expires_in = expires_in
            self.expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
        if refresh_token:
            self.refresh_token = refresh_token
