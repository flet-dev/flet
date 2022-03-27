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
	go cleanupPagesAndSessions()
	go cleanupExpiredClients()
}

func cleanupPagesAndSessions() {
	log.Println("Start background task to cleanup old pages and sessions")

	ticker := time.NewTicker(10 * time.Second)
	for {
		<-ticker.C

		sessions := store.GetExpiredSessions()
		if len(sessions) > 0 {
			log.Debugln("Deleting old sessions:", len(sessions))
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
				if !page.IsApp && len(store.GetPageSessions(pageID)) == 0 && len(store.GetPageHostClients(page.ID)) == 0 {
					store.DeletePage(pageID)
				}
			}
		}
	}
}

func cleanupExpiredClients() {
	log.Println("Start background task to cleanup expired clients")

	ticker := time.NewTicker(20 * time.Second)
	for {
		<-ticker.C

		clients := store.GetExpiredClients()
		for _, clientID := range clients {
			deleteExpiredClient(clientID, false)
		}
	}
}

func deleteExpiredClient(clientID string, removeExpiredClient bool) {
	log.Debugln("Delete expired client:", clientID)
	webClients := store.DeleteExpiredClient(clientID, removeExpiredClient)
	go notifyInactiveWebClients(webClients)
}

func notifyInactiveWebClients(webClients []string) {
	for _, clientID := range webClients {
		log.Debugln("Notify client which app become inactive:", clientID)

		msg := NewMessageData("", AppBecomeInactiveAction, &AppBecomeInactivePayload{
			Message: inactiveAppMessage,
		})
		pubsub.Send(clientChannelName(clientID), msg)
	}
}
