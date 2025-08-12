class Authorization:
    async def dehydrate_token(self, saved_token: str):
        raise NotImplementedError()

    async def get_token(self):
        raise NotImplementedError()

    def get_authorization_data(self) -> tuple[str, str]:
        raise NotImplementedError()

    async def request_token(self, code: str):
        raise NotImplementedError()
