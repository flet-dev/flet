import time


class OAuthToken():
    def __init__(self) -> None:
        self.token = ""
        self.created = time.time()
        self.expires_in = None
        self.refresh_token = ""
        self.scope = []
        self.token_type = None

