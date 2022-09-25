package model

type OAuthState struct {
	PageID           int    `json:"pageID"`
	SessionID        string `json:"sessionID"`
	CompletePageHtml string `json:"completePageHtml"`
	CompletePageUrl  string `json:"completePageUrl"`
}
