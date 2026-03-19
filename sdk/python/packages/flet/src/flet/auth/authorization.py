from typing import Any

__all__ = ["Authorization"]


class Authorization:
    """
    Abstract authorization contract used by Flet authentication workflows.

    Implementations provide OAuth-style authorization URL/state generation,
    token exchange, token hydration from persisted storage, and token retrieval.
    """

    async def dehydrate_token(self, saved_token: str) -> None:
        """
        Restore token state from previously persisted token data.

        Args:
            saved_token: Serialized token payload.
        """

        raise NotImplementedError()

    async def get_token(self) -> Any:
        """
        Return the current token, refreshing it when needed.

        Returns:
            Current authorization token object.
        """

        raise NotImplementedError()

    def get_authorization_data(self) -> tuple[str, str]:
        """
        Build authorization URL and state for starting auth flow.

        Returns:
            A tuple containing authorization URL and generated state value.
        """

        raise NotImplementedError()

    async def request_token(self, code: str) -> None:
        """
        Exchange authorization code for access/refresh token data.

        Args:
            code: Authorization code returned by provider redirect.
        """

        raise NotImplementedError()
