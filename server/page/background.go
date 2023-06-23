package page

import (
	"context"
	"time"

	log "github.com/sirupsen/logrus"

	"github.com/flet-dev/flet/server/model"
	"github.com/flet-dev/flet/server/pubsub"
	"github.com/flet-dev/flet/server/store"
)

func RunBackgroundTasks(ctx context.Context) {
	log.Println("Starting background tasks...")
	go cleanup()
}

func cleanup() {
	log.Println("Start background task to cleanup expired data")
	ticker := time.NewTicker(10 * time.Second)
	for {
		<-ticker.C

		cleanupPagesAndSessions()
		cleanupExpiredClients()
		cleanupExpiredPageNameRegistrations()
	}
}

func cleanupPagesAndSessions() {
	sessions := store.GetExpiredSessions()
	if len(sessions) > 0 {
		log.Debugln("Deleting expired sessions:", len(sessions))
		for _, fullSessionID := range sessions {
			pageID, sessionID := model.ParseSessionID(fullSessionID)

			page := store.GetPageByID(pageID)
			if page == nil {
				continue
			}

			// notify host client about expired session
			sendPageEventToSession(&model.Session{
				Page: page,
				ID:   sessionID,
			}, "close", "")

			store.DeleteSession(pageID, sessionID)

			// delete page if no more sessions
			if len(store.GetPageSessions(pageID)) == 0 && len(store.GetPageHostClients(page.ID)) == 0 {
				store.DeletePage(pageID)
			}
		}
	}
}

func cleanupExpiredClients() {
	clients := store.GetExpiredClients()
	if len(clients) > 0 {
		log.Debugln("Delete expired clients:", len(clients))
		for _, clientID := range clients {
			deleteExpiredClient(clientID, false)
		}
	}
}

func cleanupExpiredPageNameRegistrations() {
	pageNameRegs := store.GetExpiredPageNameRegistrations()
	if len(pageNameRegs) > 0 {
		log.Debugln("Delete expired pageName registrations:", len(pageNameRegs))
		for _, pageName := range pageNameRegs {
			store.RemovePageNameRegistration(pageName)
		}
	}
}

func deleteExpiredClient(clientID string, removeExpiredClient bool) {
	log.Debugln("Delete expired page name:", clientID)
	webClients := store.DeleteExpiredClient(clientID, removeExpiredClient)
	go notifyInactiveWebClients(webClients)
}

func notifyInactiveWebClients(webClients []string) {
	for _, clientID := range webClients {
		log.Debugln("Notify client which app become inactive:", clientID)

		msg := NewMessageData("", AppBecomeInactiveAction, &AppBecomeInactivePayload{
			Message: inactiveAppMessage,
		})
		pubsub.Send(ClientChannelName(clientID), msg)
	}
}
