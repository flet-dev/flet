from fastapi import HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from flet.fastapi.flet_app_manager import app_manager


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

        await session._authorize_callback_async(
            {
                "state": state_id,
                "code": request.query_params.get("code"),
                "error": request.query_params.get("error"),
                "error_description": request.query_params.get("error_description"),
            }
        )

        if state.complete_page_url:
            return RedirectResponse(state.complete_page_url)
        else:
            html_content = (
                state.complete_page_html
                if state.complete_page_html
                else f"""
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
            """
            )
            return HTMLResponse(content=html_content, status_code=200)
