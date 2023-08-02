package page

import (
	"encoding/json"
	"errors"
	"fmt"
	"strings"
	"time"

	log "github.com/sirupsen/logrus"

	"github.com/flet-dev/flet/server/cache"
	"github.com/flet-dev/flet/server/config"
	"github.com/flet-dev/flet/server/model"
	"github.com/flet-dev/flet/server/page/connection"
	"github.com/flet-dev/flet/server/pubsub"
	"github.com/flet-dev/flet/server/stats"
	"github.com/flet-dev/flet/server/store"
	"github.com/flet-dev/flet/server/utils"
	"github.com/google/uuid"
)

type ClientRole string

const (
	None                            ClientRole = "None"
	WebClient                       ClientRole = "Web"
	HostClient                      ClientRole = "Host"
	pageNotFoundMessage                        = "Please wait while the application is being started..."
	inactiveAppMessage                         = "The application went offline. Please wait while the application is being re-started..."
	signinRequiredMessage                      = "signin_required"
	clientRefreshIntervalSeconds               = 5
	clientExpirationSeconds                    = 20
	clientPageNameExpirationSeconds            = 60 * 60 * 24
)

type Client struct {
	id                   string
	role                 ClientRole
	conn                 connection.Conn
	clientIP             string
	clientUserAgent      string
	subscription         chan []byte
	pages                map[string]*model.Page
	pageNames            map[string]bool
	exitExtendExpiration chan bool
}

func autoID() string {
	return uuid.New().String()
}

func NewClient(conn connection.Conn, clientIP string, clientUserAgent string) *Client {

	ip := clientIP
	if ip == "::1" {
		ip = "127.0.0.1"
	}

	c := &Client{
		id:                   autoID(),
		conn:                 conn,
		clientIP:             ip,
		clientUserAgent:      clientUserAgent,
		pages:                make(map[string]*model.Page),
		pageNames:            make(map[string]bool),
		exitExtendExpiration: make(chan bool),
	}

	go func() {
		normalClosure := conn.Start(c.readHandler)
		c.unregister(normalClosure)
	}()

	log.Printf("New WebSocket client connected from %s: %s", clientIP, c.id)

	stats.ClientConnected()

	return c
}

func (c *Client) register(role ClientRole) {

	if c.role != "" {
		return
	}

	log.Printf("Registering %s client: %s", role, c.id)

	c.role = role

	// subscribe PubSub
	c.subscription = pubsub.Subscribe(ClientChannelName(c.id))
	go func() {
		for {
			msg, more := <-c.subscription
			if !more {
				log.Debugln("Exit subscribe():", c.id)
				return
			}
			c.send(msg)
		}
	}()

	// run sliding expiration
	go func() {
		ticker := time.NewTicker(time.Duration(clientRefreshIntervalSeconds) * time.Second)
		defer ticker.Stop()
		for {
			// extend client expiration
			store.SetClientExpiration(c.id, time.Now().Add(time.Duration(clientExpirationSeconds)*time.Second))

			// extend app session expiration
			if c.role == WebClient {
				for _, session := range store.GetClientSessions(c.id) {
					h := newSessionHandler(session)
					h.extendExpiration()
				}
			}

			select {
			case <-ticker.C:
			case <-c.exitExtendExpiration:
				log.Debugln("Exit extendExpiration():", c.id)
				return
			}
		}
	}()
}

func (c *Client) readHandler(message []byte) error {
	log.Debugf("Message from %s: %v\n", c.id, string(message))

	// decode message
	msg := &Message{}
	err := json.Unmarshal(message, msg)
	if err != nil {
		return err
	}

	switch msg.Action {
	case RegisterWebClientAction:
		c.registerWebClient(msg)

	case RegisterHostClientAction:
		c.registerHostClient(msg)

	case PageCommandFromHostAction:
		c.executeCommandFromHostClient(msg)

	case PageCommandsBatchFromHostAction:
		c.executeCommandsBatchFromHostClient(msg)

	case PageEventFromWebAction:
		c.processPageEventFromWebClient(msg)

	case UpdateControlPropsAction:
		c.updateControlPropsFromWebClient(msg)
	}

	return nil
}

func (c *Client) send(message []byte) {
	c.conn.Send(message)
}

func (c *Client) registerWebClient(message *Message) {
	log.Println("registerWebClient()")
	request := new(RegisterWebClientRequestPayload)
	json.Unmarshal(message.Payload, request)

	// register logic
	session, sessionCreated, response := c.registerWebClientCore(request)

	// send response message
	responseMsg := NewMessageData(message.ID, RegisterWebClientAction, response)
	c.send(responseMsg)

	if response.AppInactive {
		c.register(WebClient)
	}

	if response.Error == "" && !sessionCreated {
		sendPageEventToSession(session, "connect", "")
	}
}

func sendPageEventToSession(session *model.Session, eventName string, eventData string) {
	msg := NewMessageData("", PageEventToHostAction, &PageEventPayload{
		PageName:    session.Page.Name,
		SessionID:   session.ID,
		EventTarget: "page",
		EventName:   eventName,
		EventData:   eventData,
	})

	for _, clientID := range store.GetSessionHostClients(session.Page.ID, session.ID) {
		pubsub.Send(ClientChannelName(clientID), msg)
	}
}

func (c *Client) registerWebClientCore(request *RegisterWebClientRequestPayload) (
	session *model.Session,
	sessionCreated bool,
	response *RegisterWebClientResponsePayload) {

	response = &RegisterWebClientResponsePayload{
		Error: "",
	}

	sessionCreated = false

	pageName, err := model.ParsePageName(request.PageName)
	if err != nil {
		response.Error = err.Error()
		return
	}

	// unregister web client from a page name
	for pageName := range c.pageNames {
		store.RemovePageNameWebClient(pageName, c.id)
	}
	c.pageNames = make(map[string]bool)

	// get page
	page := store.GetPageByName(pageName.String())
	c.pageNames[pageName.String()] = true
	exp := time.Now().Add(time.Duration(clientPageNameExpirationSeconds) * time.Second)
	store.AddPageNameWebClient(pageName.String(), c.id, exp)

	if page == nil && !pageName.IsIndex {
		// fallback to index
		pageName, _ = model.ParsePageName("")
		c.pageNames[pageName.String()] = true
		store.AddPageNameWebClient(pageName.String(), c.id, exp)

		page = store.GetPageByName(pageName.String())
	}

	if page == nil {
		response.AppInactive = true
		response.Error = pageNotFoundMessage
		return
	}

	if len(store.GetPageHostClients(page.ID)) == 0 {
		response.AppInactive = true
		response.Error = inactiveAppMessage
		return
	}

	// lookup for existing session
	if request.SessionID != "" {
		if sessionID, err := c.decryptSensitiveData(request.SessionID, ""); err == nil {
			session = store.GetSession(page, sessionID)
		} else {
			response.Error = fmt.Sprintf("error decrypting session ID %s from %s: %s", request.SessionID, c.clientIP, err)
			return
		}
	}

	if session == nil {
		// create new session
		if sessionsRateLimitReached(c.clientIP) {
			response.Error = fmt.Sprintf("A limit of %d new sessions per hour has been reached", config.LimitSessionsPerHour())
			return
		}

		session = newSession(page, uuid.New().String(), c.clientIP, c.clientUserAgent,
			request.PageRoute, request.PageWidth, request.PageHeight,
			request.WindowWidth, request.WindowHeight, request.WindowTop, request.WindowLeft,
			request.IsPWA, request.IsWeb, request.IsDebug, request.Platform, request.PlatformBrightness)
		sessionCreated = true
	} else {
		log.Debugf("Existing session %s found for %s page\n", session.ID, page.Name)

		// update existing page props
		handler := newSessionHandler(session)
		handler.setInternal(&model.Command{
			Name:   "set",
			Values: []string{"page"},
			Attrs: map[string]string{
				"route": request.PageRoute,
			},
		})

		sendPageEventToSession(session, "route_change", request.PageRoute)
	}

	c.register(WebClient)

	log.Printf("Registering %v client %s to session %s:%s", c.role, c.id, session.Page.Name, session.ID)

	store.AddSessionWebClient(session.Page.ID, session.ID, c.id)
	h := newSessionHandler(session)
	h.extendExpiration()

	if sessionCreated {
		// pick connected host client from page pool and notify about new session created
		msg := NewMessageData("", SessionCreatedAction, &SessionCreatedPayload{
			PageName:  page.Name,
			SessionID: session.ID,
		})

		// TODO
		// pick first host client for now
		// in the future we will implement load distribution algorithm
		for _, clientID := range store.GetPageHostClients(page.ID) {
			store.AddSessionHostClient(session.Page.ID, session.ID, clientID)
			pubsub.Send(ClientChannelName(clientID), msg)
			break
		}

		log.Debugf("New session %s started for %s page\n", session.ID, page.Name)
	}

	sessionID, err := c.encryptSensitiveData(session.ID, "")
	if err != nil {
		response.Error = fmt.Sprintf("error encrypting session.ID: %s", err)
		return
	}

	response.Session = &SessionPayload{
		ID:       sessionID,
		Controls: store.GetAllSessionControls(session),
	}

	return
}

func (c *Client) registerHostClient(message *Message) {

	var err error
	var page *model.Page
	var pageName *model.PageName

	log.Println("registerHostClient()")
	request := new(RegisterHostClientRequestPayload)
	json.Unmarshal(message.Payload, request)

	if request.HostClientID != "" {
		hostClientID, err := c.decryptSensitiveData(request.HostClientID, c.clientIP)
		if err != nil {
			log.Errorf("error decrypting host client ID %s from %s: %s", request.HostClientID, c.clientIP, err)
		}
		if hostClientID != "" && c.id != hostClientID {
			log.Printf("Updating host client ID to %s", hostClientID)
			c.id = hostClientID
		}
	}

	response := &RegisterHostClientResponsePayload{
		SessionID: "",
		PageName:  "",
		Error:     "",
	}

	if !config.AllowRemoteHostClients() && c.clientIP != "" && c.clientIP != "::1" && c.clientIP != "127.0.0.1" {
		err = fmt.Errorf("remote host clients are not allowed")
		goto response
	} else if config.HostClientsAuthToken() != "" && config.HostClientsAuthToken() != request.AuthToken {
		err = fmt.Errorf("invalid auth token")
		goto response
	}

	pageName, err = model.ParsePageName(request.PageName)
	if err != nil {
		goto response
	}

	response.PageName = pageName.String()

	// retrieve page and then create if not exists
	page = store.GetPageByName(response.PageName)

	if page == nil {
		if pagesRateLimitReached(c.clientIP) {
			err = fmt.Errorf("a limit of %d new pages per hour has been reached", config.LimitPagesPerHour())
			goto response
		}

		// filter page name
		if pageName.IsReserved() {
			err = fmt.Errorf("account or page name is reserved")
			goto response
		}

		// create new page
		page = model.NewPage(response.PageName, request.AssetsDir, request.Permissions, c.clientIP)
		store.AddPage(page)
	}

	// make sure unauth client has access to a given page
	if config.CheckPageIP() && page.ClientIP != c.clientIP {
		err = errors.New("page name is already taken")
		goto response
	}

	// update page permissions
	if page.Permissions != request.Permissions {
		page.Permissions = request.Permissions
		store.UpdatePage(page)
	}

	c.register(HostClient)
	c.registerPage(page)

response:

	if err != nil {
		response.Error = err.Error()
	} else {
		hostClientID, err := c.encryptSensitiveData(c.id, c.clientIP)
		if err != nil {
			log.Errorf("error encrypting c.id: %s", err)
		}
		response.HostClientID = hostClientID
	}

	go notifyPageNameWaitingWebClients(pageName.String())

	c.send(NewMessageData(message.ID, "", response))
}

func notifyPageNameWaitingWebClients(pageName string) {
	webClients := store.GetPageNameWebClients(pageName)
	for _, clientID := range webClients {
		log.Debugln("Notify client which app become active:", clientID)

		msg := NewMessageData("", AppBecomeActiveAction, &AppBecomeActivePayload{})
		pubsub.Send(ClientChannelName(clientID), msg)
	}
}

func cleanPage(session *model.Session) error {
	handler := newSessionHandler(session)
	_, err := handler.executeBatch([]*model.Command{
		{
			Name:   "clean",
			Values: []string{"page"},
		},
		{
			Name:   "set",
			Values: []string{"page"},
			Attrs: map[string]string{
				"verticalFill":         "",
				"horizontalAlign":      "",
				"verticalAlign":        "",
				"gap":                  "",
				"padding":              "",
				"bgcolor":              "",
				"theme":                "",
				"themePrimaryColor":    "",
				"themeTextColor":       "",
				"themeBackgroundColor": "",
			},
		},
	})
	return err
}

func (c *Client) encryptSensitiveData(data string, clientIP string) (string, error) {
	result, err := utils.EncryptWithMasterKey([]byte(data + "|" + clientIP))
	if err != nil {
		return "", err
	}
	return utils.EncodeBase64(result), nil
}

func (c *Client) decryptSensitiveData(encrypted string, clientIP string) (string, error) {
	bytes, err := utils.DecodeBase64(encrypted)
	if err != nil {
		return "", err
	}
	plain, err := utils.DecryptWithMasterKey(bytes)
	if err != nil {
		return "", err
	}
	pair := strings.Split(string(plain), "|")
	if pair[1] != "" && pair[1] != clientIP {
		return "", fmt.Errorf("IP address does not match (expected: %s, actual: %s)", pair[1], clientIP)
	}
	return pair[0], nil
}

func (c *Client) executeCommandFromHostClient(message *Message) {
	log.Debugln("Page command from host client")

	payload := new(PageCommandRequestPayload)
	json.Unmarshal(message.Payload, payload)

	responsePayload := &PageCommandResponsePayload{
		Result: "",
		Error:  "",
	}

	if !payload.Command.IsSupported() {
		responsePayload.Error = fmt.Sprintf("unknown command: %s", payload.Command.Name)
		c.send(NewMessageData(message.ID, "", responsePayload))
		return
	}

	// retrieve page and session
	page := store.GetPageByName(payload.PageName)
	if page != nil {
		session := store.GetSession(page, payload.SessionID)
		if session != nil {
			// process command
			handler := newSessionHandler(session)
			result, err := handler.execute(payload.Command)
			responsePayload.Result = result

			if payload.Command.Name == model.ErrorCommand {
				// session crashed on the client
				store.DeleteSession(page.ID, session.ID)
			} else if err != nil {
				handler.extendExpiration()
				responsePayload.Error = fmt.Sprint(err)
			}
		} else {
			responsePayload.Error = "Session not found or access denied"
		}
	} else {
		responsePayload.Error = "Page not found or access denied"
	}

	if payload.Command.ShouldReturn() {

		// send response
		c.send(NewMessageData(message.ID, "", responsePayload))
	}
}

func (c *Client) executeCommandsBatchFromHostClient(message *Message) {
	log.Debugln("Page commands batch from host client")

	payload := new(PageCommandsBatchRequestPayload)
	json.Unmarshal(message.Payload, payload)

	responsePayload := &PageCommandsBatchResponsePayload{
		Results: make([]string, 0),
		Error:   "",
	}

	for _, command := range payload.Commands {
		if !command.IsSupported() {
			responsePayload.Error = fmt.Sprintf("unknown command: %s", command.Name)
			c.send(NewMessageData(message.ID, "", responsePayload))
			return
		}
	}

	// retrieve page and session
	page := store.GetPageByName(payload.PageName)
	if page != nil {
		session := store.GetSession(page, payload.SessionID)
		if session != nil {
			// process command
			handler := newSessionHandler(session)
			results, err := handler.executeBatch(payload.Commands)
			responsePayload.Results = results
			if err != nil {
				handler.extendExpiration()
				responsePayload.Error = fmt.Sprint(err)
			}
		} else {
			responsePayload.Error = "Session not found or access denied"
		}
	} else {
		responsePayload.Error = "Page not found or access denied"
	}

	// send response
	c.send(NewMessageData(message.ID, "", responsePayload))

	log.Debugf("Page commands batch response to %s - %v\n", c.id, responsePayload)
}

func (c *Client) processPageEventFromWebClient(message *Message) {

	// web client can have only one session assigned
	var session *model.Session
	for _, s := range store.GetClientSessions(c.id) {
		session = s
		break
	}

	if session == nil {
		return
	}

	log.Debugln("Page event from browser:", string(message.Payload),
		"PageName:", session.Page.Name, "SessionID:", session.ID)

	payload := new(PageEventPayload)
	json.Unmarshal(message.Payload, payload)

	// add page/session information to payload
	payload.PageName = session.Page.Name
	payload.SessionID = session.ID

	msg := NewMessageData("", PageEventToHostAction, payload)

	// re-send events to all connected host clients
	for _, clientID := range store.GetSessionHostClients(session.Page.ID, session.ID) {
		pubsub.Send(ClientChannelName(clientID), msg)
	}
}

func (c *Client) updateControlPropsFromWebClient(message *Message) error {

	// web client can have only one session assigned
	var session *model.Session
	for _, s := range store.GetClientSessions(c.id) {
		session = s
		break
	}

	payload := new(UpdateControlPropsPayload)
	json.Unmarshal(message.Payload, payload)

	log.Debugln("Update control props from web browser:", string(message.Payload),
		"PageName:", session.Page.Name, "SessionID:", session.ID, "Props:", payload.Props)

	// update control tree
	handler := newSessionHandler(session)
	err := handler.updateControlProps(payload.Props)
	if err != nil {
		log.Errorln(err)
		return err
	}

	// update page props
	data, _ := json.Marshal(payload.Props)
	sendPageEventToSession(session, "change", string(data))

	// re-send the message to all connected web clients
	go func() {
		msg, _ := json.Marshal(message)

		for _, clientID := range store.GetSessionWebClients(session.Page.ID, session.ID) {
			if clientID != c.id {
				pubsub.Send(ClientChannelName(clientID), msg)
			}
		}
	}()
	return nil
}

func (c *Client) registerPage(page *model.Page) {

	log.Printf("Registering host client %s to handle '%s' sessions", c.id, page.Name)

	store.AddPageHostClient(page.ID, c.id)
	c.pages[page.Name] = page
}

func (c *Client) unregisterPage(page *model.Page) {
	log.Printf("Unregistering host client %s from '%s' page", c.id, page.Name)

	store.RemovePageHostClient(page.ID, c.id)
	delete(c.pages, page.Name)
}

func (c *Client) unregister(normalClosure bool) {

	log.Debugf("WebSocket client disconnected (normal closure=%t) from %s: %s", normalClosure, c.clientIP, c.id)

	stats.ClientDisconnected()

	if c.role == "" {
		return
	}

	// unsubscribe from pubsub
	pubsub.Unsubscribe(c.subscription)

	c.exitExtendExpiration <- true

	// unregister from all sessions
	if c.role == WebClient {
		for _, session := range store.GetClientSessions(c.id) {
			log.Printf("Unregistering web client %s from session %s:%s", c.id, session.Page.Name, session.ID)
			store.RemoveSessionWebClient(session.Page.ID, session.ID, c.id)
			sendPageEventToSession(session, "disconnect", "")
		}
	}

	// unregister host client from all pages
	if c.role == HostClient {
		for _, page := range c.pages {
			c.unregisterPage(page)
		}
	}

	// unregister web client from a page name
	if c.role == WebClient {
		for pageName := range c.pageNames {
			store.RemovePageNameWebClient(pageName, c.id)
		}
	}

	// expire client immediately
	if normalClosure {
		deleteExpiredClient(c.id, true)
	}
}

func pagesRateLimitReached(clientIP string) bool {
	limit := config.LimitPagesPerHour()
	if clientIP == "" || limit == 0 {
		return false
	}
	if cache.Inc(fmt.Sprintf("pages_limit:%s:%d", clientIP, time.Now().Hour()), 1, 1*time.Hour) > limit {
		return true
	}
	return false
}

func sessionsRateLimitReached(clientIP string) bool {
	limit := config.LimitSessionsPerHour()
	if clientIP == "" || limit == 0 {
		return false
	}
	if cache.Inc(fmt.Sprintf("sessions_limit:%s:%d", clientIP, time.Now().Hour()), 1, 1*time.Hour) > limit {
		return true
	}
	return false
}

func ClientChannelName(clientID string) string {
	return fmt.Sprintf("client-%s", clientID)
}
