from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from flet_web.fastapi.flet_app_manager import app_manager


class FletOAuth:
    """
    HTTP handler for OAuth callback.
    """

    def __init__(self) -> None:
        pass

    async def handle(self, request: Request):
        """
        Handle OAuth callback request.

        Request must contain minimum `code` and `state` query parameters.

        Returns either redirect to a Flet page or a HTML page with further instructions.
        """
        state_id = request.query_params.get("state")

        if not state_id:
            raise HTTPException(status_code=400, detail="Invalid state")

        state = app_manager.retrieve_state(state_id)

        if not state:
            raise HTTPException(status_code=400, detail="Invalid state")

        session = await app_manager.get_session(state.session_id)
        if not session:
            raise HTTPException(status_code=500, detail="Session not found")

        state.code = request.query_params.get("code")
        state.error = request.query_params.get("error")
        state.error_description = request.query_params.get("error_description")

        if state.complete_page_url:
            app_manager.store_state(state_id, state)
            response = RedirectResponse(state.complete_page_url)
            response.set_cookie(
                "flet_oauth_state",
                state_id,
                max_age=300,
                httponly=True,
                secure=False,
                samesite="strict",
            )
            return response
        else:
            await session.page._authorize_callback(
                {
                    "state": state_id,
                    "code": state.code,
                    "error": state.error,
                    "error_description": state.error_description,
                }
            )
            html_content = (
                state.complete_page_html
                if state.complete_page_html
                else """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Signed in successfully</title>
            </head>
            <body>
                <script type="text/javascript">
                    window.close();
                </script>
                <p>You've been successfully signed in! You can close this tab or window now.</p>
            </body>
            </html>
            """  # noqa: E501
            )
            return HTMLResponse(content=html_content, status_code=200)
