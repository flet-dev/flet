class Authorization:
    async def dehydrate_token_async(self, saved_token: str):
        raise NotImplementedError()

    async def get_token_async(self):
        raise NotImplementedError()

    def get_authorization_data(self) -> tuple[str, str]:
        raise NotImplementedError()

    async def request_token_async(self, code: str):
        raise NotImplementedError()
