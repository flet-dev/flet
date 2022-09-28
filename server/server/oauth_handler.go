package server

import (
	"errors"
	"net/http"

	"github.com/flet-dev/flet/server/page"
	"github.com/flet-dev/flet/server/pubsub"
	"github.com/flet-dev/flet/server/store"
	"github.com/flet-dev/flet/server/utils"
	log "github.com/sirupsen/logrus"

	"github.com/gin-gonic/gin"
)

func oauthCallbackHandler(c *gin.Context) {
	state := c.Query("state")
	if state == "" {
		c.AbortWithError(http.StatusBadRequest, errors.New("invalid state"))
		return
	}

	oauthState := store.GetOAuthState(state)
	if oauthState == nil {
		c.AbortWithError(http.StatusInternalServerError, errors.New("invalid state or state expired"))
		return
	}

	store.RemoveOAuthState(state)

	p := store.GetPageByID(oauthState.PageID)
	if p == nil {
		c.AbortWithError(http.StatusInternalServerError, errors.New("page not found"))
		return
	}

	session := store.GetSession(p, oauthState.SessionID)
	if session == nil {
		c.AbortWithError(http.StatusInternalServerError, errors.New("session not found"))
		return
	}

	payload := &page.PageEventPayload{
		PageName:    session.Page.Name,
		SessionID:   session.ID,
		EventTarget: "page",
		EventName:   "authorize",
		EventData: utils.ToJSON(map[string]string{
			"code":              c.Query("code"),
			"error":             c.Query("error"),
			"error_description": c.Query("error_description"),
			"state":             state,
		}),
	}

	log.Debugln("OAuth callback handler", payload)

	msg := page.NewMessageData("", page.PageEventToHostAction, payload)

	// send events to all connected host clients
	for _, clientID := range store.GetSessionHostClients(session.Page.ID, session.ID) {
		pubsub.Send(page.ClientChannelName(clientID), msg)
	}

	if oauthState.CompletePageUrl != "" {
		c.Redirect(302, oauthState.CompletePageUrl)
	} else {
		pd := oauthState.CompletePageHtml
		if pd == "" {
			pd = `<!DOCTYPE html>
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
			</html>`
		}
		c.Data(http.StatusOK, "text/html; charset=utf-8", []byte(pd))
	}
}
