package store

import (
	"fmt"
	"strconv"
	"time"

	log "github.com/sirupsen/logrus"

	"github.com/flet-dev/flet/server/auth"
	"github.com/flet-dev/flet/server/cache"
	"github.com/flet-dev/flet/server/config"
	"github.com/flet-dev/flet/server/model"
	"github.com/flet-dev/flet/server/utils"
)

const (
	sessionIDKey                    = "%d:%s"
	pageNextIDKey                   = "page_next_id"                    // Inc integer with the next page ID
	pagesKey                        = "pages"                           // pages hash with pageName:pageID
	pageKey                         = "page:%d"                         // page data
	pageHostClientsKey              = "page:%d:host_clients"            // a Set with client IDs
	pageWebClientsKey               = "page:%s:web_clients"             // a Set with client IDs
	pageNameRegistrationsExpiredKey = "page_name_registrations_expired" // set of pageName sorted by Unix timestamp
	pageHostClientSessionsKey       = "page:%d:%s:host_client_sessions" // a Set with sessionIDs
	pageSessionsKey                 = "page:%d:sessions"                // a Set with session IDs
	clientSessionsKey               = "client:%s:sessions"              // a Set with session IDs
	sessionsExpiredKey              = "sessions_expired"                // set of page:session IDs sorted by Unix timestamp of their expiration date
	clientsExpiredKey               = "clients_expired"                 // set of client IDs sorted by Unix timestamp of their expiration date
	sessionNextControlIDField       = "nextControlID"                   // Inc integer with the next control ID for a given session
	sessionPrincipalIDField         = "principalID"
	sessionKey                      = "session:%d:%s"              // session data
	sessionControlsKey              = "session:%d:%s:controls"     // session controls, value is JSON data
	sessionHostClientsKey           = "session:%d:%s:host_clients" // a Set with client IDs
	sessionWebClientsKey            = "session:%d:%s:web_clients"  // a Set with client IDs
	principalKey                    = "principal:%s"               // %s is principalID
)

//
// Pages
// ==============================

func GetPageByName(pageName string) *model.Page {
	spid := cache.HashGet(pagesKey, pageName)
	if spid == "" {
		return nil
	}
	pageID, _ := strconv.Atoi(spid)
	return GetPageByID(pageID)
}

func GetPageByID(pageID int) *model.Page {
	p := &model.Page{}

	j := cache.GetString(fmt.Sprintf(pageKey, pageID))
	if j == "" {
		return nil
	}

	utils.FromJSON(j, p)
	return p
}

func AddPage(page *model.Page) {

	// TODO - check if the page exists
	pageID := cache.Inc(pageNextIDKey, 1, 0)
	page.ID = pageID

	cache.SetString(fmt.Sprintf(pageKey, page.ID), utils.ToJSON(page), 0)
	cache.HashSet(pagesKey, page.Name, page.ID)
}

func UpdatePage(page *model.Page) {
	cache.SetString(fmt.Sprintf(pageKey, page.ID), utils.ToJSON(page), 0)
}

func DeletePage(pageID int) {
	page := GetPageByID(pageID)
	if page == nil {
		log.Warnln("An attempt to delete inexisting page with ID", pageID)
		return
	}

	log.Println("Deleting page:", page.Name)
	for _, sessionID := range GetPageSessions(page.ID) {
		DeleteSession(page.ID, sessionID)
	}
	cache.Remove(fmt.Sprintf(pageHostClientsKey, page.ID))
	cache.Remove(fmt.Sprintf(pageKey, pageID))
	cache.HashRemove(pagesKey, page.Name)
}

//
// Page Host Clients
// ==============================

func GetPageSessions(pageID int) []string {
	return cache.SetGet(fmt.Sprintf(pageSessionsKey, pageID))
}

func GetPageHostClients(pageID int) []string {
	return cache.SetGet(fmt.Sprintf(pageHostClientsKey, pageID))
}

func AddPageHostClient(pageID int, clientID string) {
	cache.SetAdd(fmt.Sprintf(pageHostClientsKey, pageID), clientID)
}

func RemovePageHostClient(pageID int, clientID string) {
	cache.SetRemove(fmt.Sprintf(pageHostClientsKey, pageID), clientID)
}

// Page Name Web Clients - web clients subscribed to a page name
// =============================================================
func GetExpiredPageNameRegistrations() []string {
	return cache.SortedSetPopRange(pageNameRegistrationsExpiredKey, 0, time.Now().Unix())
}

func RemovePageNameRegistration(pageName string) {
	cache.Remove(fmt.Sprintf(pageWebClientsKey, pageName))
}

func GetPageNameWebClients(pageName string) []string {
	return cache.SetGet(fmt.Sprintf(pageWebClientsKey, pageName))
}

func AddPageNameWebClient(pageName string, clientID string, expires time.Time) {
	log.Debugf("Subscribe web client %s to '%s' page name", clientID, pageName)
	cache.SetAdd(fmt.Sprintf(pageWebClientsKey, pageName), clientID)
	cache.SortedSetAdd(pageNameRegistrationsExpiredKey, pageName, expires.Unix())
}

func RemovePageNameWebClient(pageName string, clientID string) {
	log.Debugf("Unsubscribe web client %s from '%s' page name", clientID, pageName)
	cache.SetRemove(fmt.Sprintf(pageWebClientsKey, pageName), clientID)
}

//
// Clients
// ==============================

func SetClientExpiration(clientID string, expires time.Time) {
	cache.SortedSetAdd(clientsExpiredKey, clientID, expires.Unix())
}

func GetExpiredClients() []string {
	return cache.SortedSetPopRange(clientsExpiredKey, 0, time.Now().Unix())
}

func GetClientSessions(clientID string) []string {
	return cache.SetGet(fmt.Sprintf(clientSessionsKey, clientID))
}

func DeleteExpiredClient(clientID string, removeExpiredClient bool) (webClients []string) {
	if removeExpiredClient {
		cache.SortedSetRemove(clientsExpiredKey, clientID)
	}
	webClients = make([]string, 0)
	for _, fullSessionID := range GetClientSessions(clientID) {
		pageID, sessionID := model.ParseSessionID(fullSessionID)
		cache.SetRemove(fmt.Sprintf(sessionHostClientsKey, pageID, sessionID), clientID)
		cache.SetRemove(fmt.Sprintf(sessionWebClientsKey, pageID, sessionID), clientID)
		cache.SetRemove(fmt.Sprintf(pageHostClientsKey, pageID), clientID)

		page := GetPageByID(pageID)
		if page != nil && page.IsApp {
			for _, sessionID := range GetPageHostClientSessions(pageID, clientID) {
				RemoveSessionHostClient(pageID, sessionID, clientID)

				sessionClients := GetSessionWebClients(pageID, sessionID)
				for _, clientID := range sessionClients {
					webClients = append(webClients, clientID)
					RemoveSessionWebClient(pageID, sessionID, clientID)
				}

				DeleteSession(pageID, sessionID)
			}
			RemovePageHostClientSessions(pageID, clientID)

			if len(GetPageHostClients(pageID)) == 0 {
				DeletePage(pageID)
			}
		}
	}
	cache.Remove(fmt.Sprintf(clientSessionsKey, clientID))
	return
}

//
// Sessions
// ==============================

func GetSession(page *model.Page, sessionID string) *model.Session {

	var session model.Session
	cache.HashGetObject(fmt.Sprintf(sessionKey, page.ID, sessionID), &session)
	if session.ID == "" {
		return nil
	}
	session.Page = page
	return &session
}

func AddSession(session *model.Session) {
	cache.HashSet(fmt.Sprintf(sessionKey, session.Page.ID, session.ID),
		"id", session.ID)
	cache.SetAdd(fmt.Sprintf(pageSessionsKey, session.Page.ID), session.ID)
}

func SetSessionExpiration(session *model.Session, expires time.Time) {
	cache.SortedSetAdd(sessionsExpiredKey, fmt.Sprintf(sessionIDKey, session.Page.ID, session.ID), expires.Unix())
}

func GetExpiredSessions() []string {
	return cache.SortedSetPopRange(sessionsExpiredKey, 0, time.Now().Unix())
}

func SetSessionPrincipalID(session *model.Session, principalID string) {
	session.PrincipalID = principalID
	cache.HashSet(fmt.Sprintf(sessionKey, session.Page.ID, session.ID), sessionPrincipalIDField, principalID)
}

func DeleteSession(pageID int, sessionID string) {
	cache.SetRemove(fmt.Sprintf(pageSessionsKey, pageID), sessionID)
	cache.SortedSetRemove(sessionsExpiredKey, fmt.Sprintf(sessionIDKey, pageID, sessionID))
	cache.Remove(fmt.Sprintf(sessionKey, pageID, sessionID))
	cache.Remove(fmt.Sprintf(sessionControlsKey, pageID, sessionID))
	cache.Remove(fmt.Sprintf(sessionHostClientsKey, pageID, sessionID))
	cache.Remove(fmt.Sprintf(sessionWebClientsKey, pageID, sessionID))
}

//
// Controls
// ==============================

func GetSessionNextControlID(session *model.Session) int {
	return cache.HashInc(fmt.Sprintf(sessionKey, session.Page.ID, session.ID), sessionNextControlIDField, 1)
}

func GetSessionControl(session *model.Session, ctrlID string) *model.Control {
	cj := cache.HashGet(fmt.Sprintf(sessionControlsKey, session.Page.ID, session.ID), ctrlID)
	if cj == "" {
		return nil
	}
	ctrl, err := model.NewControlFromJSON(cj)
	if err != nil {
		log.Error(err)
		return nil
	}
	return ctrl
}

func GetAllSessionControls(session *model.Session) map[string]*model.Control {
	fields := cache.HashGetAll(fmt.Sprintf(sessionControlsKey, session.Page.ID, session.ID))
	controls := make(map[string]*model.Control, len(fields))
	for k, v := range fields {
		ctrl, _ := model.NewControlFromJSON(v)
		controls[k] = ctrl
	}
	return controls
}

func SetSessionControl(session *model.Session, ctrl *model.Control) error {
	cj := utils.ToJSON(ctrl)
	success := cache.SetSessionControl(
		fmt.Sprintf(sessionKey, session.Page.ID, session.ID),
		fmt.Sprintf(sessionControlsKey, session.Page.ID, session.ID), ctrl.ID(), cj, config.LimitSessionSizeBytes())
	if !success {
		return fmt.Errorf("session %d:%s size exceeds the maximum of %d bytes", session.Page.ID, session.ID, config.LimitSessionSizeBytes())
	}
	return nil
}

func DeleteSessionControl(session *model.Session, ctrlID string) {
	cache.RemoveSessionControl(
		fmt.Sprintf(sessionKey, session.Page.ID, session.ID),
		fmt.Sprintf(sessionControlsKey, session.Page.ID, session.ID), ctrlID)
}

//
// Session Host Clients
// ==============================

func GetSessionHostClients(pageID int, sessionID string) []string {
	return cache.SetGet(fmt.Sprintf(sessionHostClientsKey, pageID, sessionID))
}

func GetPageHostClientSessions(pageID int, clientID string) []string {
	return cache.SetGet(fmt.Sprintf(pageHostClientSessionsKey, pageID, clientID))
}

func AddSessionHostClient(pageID int, sessionID string, clientID string) {
	cache.SetAdd(fmt.Sprintf(sessionHostClientsKey, pageID, sessionID), clientID)
	cache.SetAdd(fmt.Sprintf(pageHostClientSessionsKey, pageID, clientID), sessionID)
	cache.SetAdd(fmt.Sprintf(clientSessionsKey, clientID), fmt.Sprintf(sessionIDKey, pageID, sessionID))
}

func RemoveSessionHostClient(pageID int, sessionID string, clientID string) {
	cache.SetRemove(fmt.Sprintf(sessionHostClientsKey, pageID, sessionID), clientID)
	cache.SetRemove(fmt.Sprintf(pageHostClientSessionsKey, pageID, clientID), sessionID)
	cache.SetRemove(fmt.Sprintf(clientSessionsKey, clientID), fmt.Sprintf(sessionIDKey, pageID, sessionID))
}

func RemovePageHostClientSessions(pageID int, clientID string) {
	cache.Remove(fmt.Sprintf(pageHostClientSessionsKey, pageID, clientID))
}

//
// Session Web Clients
// ==============================

func GetSessionWebClients(pageID int, sessionID string) []string {
	return cache.SetGet(fmt.Sprintf(sessionWebClientsKey, pageID, sessionID))
}

func AddSessionWebClient(pageID int, sessionID string, clientID string) {
	cache.SetAdd(fmt.Sprintf(sessionWebClientsKey, pageID, sessionID), clientID)
	cache.SetAdd(fmt.Sprintf(clientSessionsKey, clientID), fmt.Sprintf(sessionIDKey, pageID, sessionID))
}

func RemoveSessionWebClient(pageID int, sessionID string, clientID string) {
	cache.SetRemove(fmt.Sprintf(sessionWebClientsKey, pageID, sessionID), clientID)
	cache.SetRemove(fmt.Sprintf(clientSessionsKey, clientID), fmt.Sprintf(sessionIDKey, pageID, sessionID))
}

//
// Security principals
// ==============================

func GetSecurityPrincipal(principalID string) *auth.SecurityPrincipal {
	j := cache.GetString(fmt.Sprintf(principalKey, principalID))
	if j == "" {
		return nil
	}

	p := &auth.SecurityPrincipal{}
	utils.FromJSON(j, p)
	return p
}

func SetSecurityPrincipal(p *auth.SecurityPrincipal, expires time.Duration) {
	cache.SetString(fmt.Sprintf(principalKey, p.UID), utils.ToJSON(p), expires)
}

func DeleteSecurityPrincipal(principalID string) {
	cache.Remove(fmt.Sprintf(principalKey, principalID))
}
