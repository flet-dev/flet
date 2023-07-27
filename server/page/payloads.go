package page

import (
	"encoding/json"

	"github.com/flet-dev/flet/server/model"
)

type Message struct {
	ID      string          `json:"id"`
	Action  string          `json:"action"`
	Payload json.RawMessage `json:"payload"`
}

func NewMessageData(id string, action string, payload interface{}) []byte {
	msg := NewMessage(id, action, payload)
	result, _ := json.Marshal(msg)
	return result
}

func NewMessage(id string, action string, payload interface{}) *Message {
	msg := &Message{
		ID:     id,
		Action: action,
	}

	// serialize payload
	serializedPayload, _ := json.Marshal(payload)
	msg.Payload = serializedPayload

	return msg
}

type RegisterHostClientRequestPayload struct {
	HostClientID string `json:"hostClientID"`
	PageName     string `json:"pageName"`
	AssetsDir    string `json:"assetsDir"`
	AuthToken    string `json:"authToken"`
	Permissions  string `json:"permissions"`
}

type RegisterHostClientResponsePayload struct {
	HostClientID string `json:"hostClientID"`
	SessionID    string `json:"sessionID"`
	PageName     string `json:"pageName"`
	Error        string `json:"error"`
}

type RegisterWebClientRequestPayload struct {
	PageName           string `json:"pageName"`
	PageRoute          string `json:"pageRoute"`
	PageWidth          string `json:"pageWidth"`
	PageHeight         string `json:"pageHeight"`
	WindowWidth        string `json:"windowWidth"`
	WindowHeight       string `json:"windowHeight"`
	WindowTop          string `json:"windowTop"`
	WindowLeft         string `json:"windowLeft"`
	IsPWA              string `json:"isPWA"`
	IsWeb              string `json:"isWeb"`
	IsDebug            string `json:"isDebug"`
	Platform           string `json:"platform"`
	PlatformBrightness string `json:"platformBrightness"`
	SessionID          string `json:"sessionID"`
}

type RegisterWebClientResponsePayload struct {
	Session     *SessionPayload `json:"session"`
	AppInactive bool            `json:"appInactive"`
	Error       string          `json:"error"`
}

type SessionPayload struct {
	ID       string                    `json:"id"`
	Controls map[string]*model.Control `json:"controls"`
}

type SessionCreatedPayload struct {
	PageName  string `json:"pageName"`
	SessionID string `json:"sessionID"`
}

type PageCommandRequestPayload struct {
	PageName  string         `json:"pageName"`
	SessionID string         `json:"sessionID"`
	Command   *model.Command `json:"command"`
}

type PageCommandResponsePayload struct {
	Result string `json:"result"`
	Error  string `json:"error"`
}

type PageCommandsBatchRequestPayload struct {
	PageName  string           `json:"pageName"`
	SessionID string           `json:"sessionID"`
	Commands  []*model.Command `json:"commands"`
}

type PageCommandsBatchResponsePayload struct {
	Results []string `json:"results"`
	Error   string   `json:"error"`
}

type InactiveAppRequestPayload struct {
	PageName string `json:"pageName"`
}

type PageEventPayload struct {
	PageName    string `json:"pageName"`
	SessionID   string `json:"sessionID"`
	EventTarget string `json:"eventTarget"`
	EventName   string `json:"eventName"`
	EventData   string `json:"eventData"`
}

type AddPageControlsPayload struct {
	Controls []*model.Control `json:"controls"`
	TrimIDs  []string         `json:"trimIDs"`
}

type ReplacePageControlsPayload struct {
	IDs      []string         `json:"ids"`
	Remove   bool             `json:"remove"`
	Controls []*model.Control `json:"controls"`
}

type UpdateControlPropsPayload struct {
	Props []map[string]string `json:"props"`
}

type AppendControlPropsPayload struct {
	Props []map[string]string `json:"props"`
}

type RemoveControlPayload struct {
	IDs []string `json:"ids"`
}

type CleanControlPayload struct {
	IDs []string `json:"ids"`
}

type AppBecomeActivePayload struct {
}

type AppBecomeInactivePayload struct {
	Message string `json:"message"`
}

type SessionCrashedPayload struct {
	Message string `json:"message"`
}

type InvokeMethodPayload struct {
	MethodID   string            `json:"methodId"`
	MethodName string            `json:"methodName"`
	ControlID  string            `json:"controlId"`
	Arguments  map[string]string `json:"arguments"`
}
