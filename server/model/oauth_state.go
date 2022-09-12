package model

type OAuthState struct {
	PageID    int    `json:"pageID"`
	SessionID string `json:"sessionID"`
}
