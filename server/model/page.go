package model

// Page represents a single page.
type Page struct {
	ID          int    `json:"id" redis:"id"`
	Name        string `json:"name" redis:"name"`
	AssetsDir   string `json:"assetsDir" redis:"assetsDir"`
	ClientIP    string `json:"clientIP" redis:"clientIP"`
	Permissions string `json:"permissions" redis:"permissions"`
}

// NewPage creates a new instance of Page.
func NewPage(name string, assetsDir string, permissions string, clientIP string) *Page {
	p := &Page{}
	p.Name = name
	p.AssetsDir = assetsDir
	p.ClientIP = clientIP
	p.Permissions = permissions
	return p
}
