package model

// Page represents a single page.
type Page struct {
	ID          int    `json:"id" redis:"id"`
	Name        string `json:"name" redis:"name"`
	ClientIP    string `json:"clientIP" redis:"clientIP"`
	IsApp       bool   `json:"isApp" redis:"isApp"`
	Permissions string `json:"permissions" redis:"permissions"`
}

// NewPage creates a new instance of Page.
func NewPage(name string, isApp bool, permissions string, clientIP string) *Page {
	p := &Page{}
	p.Name = name
	p.IsApp = isApp
	p.ClientIP = clientIP
	p.Permissions = permissions
	return p
}
